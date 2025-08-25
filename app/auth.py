import bcrypt
from dotenv import load_dotenv
load_dotenv()
import jwt
import os
from datetime import datetime, timedelta

# ------------------ CONFIG ------------------
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "lemmewoo12345")  # change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


# ------------------ PASSWORD UTILS ------------------
def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# ------------------ TOKEN UTILS ------------------
def create_access_token(username: str) -> str:
    """
    Generate JWT token for given username.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str) -> str | None:
    """
    Decode JWT token, return username or None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None