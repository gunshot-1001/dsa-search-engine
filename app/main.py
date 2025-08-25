import os, json
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
from scipy import sparse
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware   # <-- ADD THIS

# ---- Local imports with safe paths ----
import sys
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from preprocessing.preprocess import normalize_text
from app.db import SessionLocal, User, Progress
from app.auth import hash_password, verify_password, create_access_token, decode_token
from app.ai_client import generate_learning_path, explain_code

# ---- Load models at startup ----
MODELS_DIR = BASE_DIR / "models"
VEC_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
MAT_PATH = MODELS_DIR / "tfidf_matrix.npz"
INDEX_MAP_PATH = MODELS_DIR / "index_map.json"

vectorizer = joblib.load(VEC_PATH)
tfidf_matrix = sparse.load_npz(MAT_PATH)
with open(INDEX_MAP_PATH, "r", encoding="utf-8") as f:
    index_map = json.load(f)

app = FastAPI(title="DSA Search Engine")
security = HTTPBearer()

# ✅ Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Schemas ----------
class SignupIn(BaseModel):
    username: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

class SearchResult(BaseModel):
    title: str
    domain: str
    tag: str
    url: str
    score: float
    snippet: Optional[str]

# ---------- DB dependencies ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = creds.credentials
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ---------- Auth endpoints ----------
@app.post("/signup")
def signup(data: SignupIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username exists")
    hashed = hash_password(data.password)
    u = User(username=data.username, hashed_password=hashed)
    db.add(u); db.commit(); db.refresh(u)
    token = create_access_token(u.username)
    return {"access_token": token}

@app.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.username)
    return {"access_token": token}

# ---------- Search endpoint (public) ----------
@app.get("/search", response_model=List[SearchResult])
def search(q: str, top_k: int = 10):
    q_proc = normalize_text(q)
    q_vec = vectorizer.transform([q_proc])
    scores = linear_kernel(q_vec, tfidf_matrix).flatten()
    top_idx = scores.argsort()[::-1][:top_k]

    results = []
    for i in top_idx:
        meta = index_map[i]
        snippet = meta.get("processed_text", "")[:200]  # small preview
        results.append({
            "title": meta.get("title"),
            "domain": meta.get("domain", ""),
            "tag": meta.get("tag", ""),
            "url": meta.get("url"),
            "score": float(scores[i]),
            "snippet": snippet
        })
    return results

# ---------- Progress endpoints ----------
class ProgressIn(BaseModel):
    problem_url: str
    status: str  # solved/in-progress/unsolved

@app.post("/progress")
def set_progress(data: ProgressIn, user = Depends(get_current_user), db: Session = Depends(get_db)):
    p = Progress(user_id=user.id, problem_id=data.problem_url, status=data.status)
    db.add(p); db.commit(); db.refresh(p)
    return {"ok": True, "progress_id": p.id}

@app.get("/progress")
def get_progress(user = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(Progress).filter(Progress.user_id == user.id).all()
    return [{"problem_url": r.problem_id, "status": r.status} for r in rows]

# ---------- AI endpoints ----------
class PathRequest(BaseModel):
    profile_text: str
    length: Optional[int] = 8

@app.post("/ai/generate_path")
def ai_generate_path(req: PathRequest, user = Depends(get_current_user)):
    out = generate_learning_path(req.profile_text, length=req.length)
    return {"path": out}

class ExplainRequest(BaseModel):
    problem_description: str
    code: str
    language: Optional[str] = "python"

@app.post("/ai/explain")
def ai_explain(req: ExplainRequest, user = Depends(get_current_user)):
    out = explain_code(req.code, req.language, req.problem_description)
    return {"explanation": out}