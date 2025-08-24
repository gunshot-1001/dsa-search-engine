import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import numpy as np
from scipy import sparse
import sys

# Make sure preprocessing is importable
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from preprocessing.preprocess import normalize_text

# Define paths relative to project root
DATA_DIR = BASE_DIR / "scrapers" / "data"
MODELS_DIR = BASE_DIR / "models"

leetcode_file = DATA_DIR / "leetcode_problems.json"
hackerrank_file = DATA_DIR / "hackerrank_all_domains.json"
processed_file = DATA_DIR / "problems_processed.json"

tfidf_vectorizer_file = MODELS_DIR / "tfidf_vectorizer.joblib"
tfidf_matrix_file = MODELS_DIR / "tfidf_matrix.npz"
index_map_file = MODELS_DIR / "index_map.json"


def preprocess_file(file_path):
    """Load a JSON problems file and normalize text."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    processed = []
    for entry in data:
        # Concatenate Title, Domain, Tag for context
        raw_text = f"{entry.get('Title', '')} {entry.get('Domain', '')} {entry.get('Tag', '')}"
        clean_text = normalize_text(raw_text)

        processed.append({
            "title": entry.get("Title", ""),
            "domain": entry.get("Domain", ""),
            "tag": entry.get("Tag", ""),
            "url": entry.get("URL", ""),
            "processed_text": clean_text
        })
    return processed


if __name__ == "__main__":
    MODELS_DIR.mkdir(exist_ok=True)

    # Load and preprocess both datasets
    leetcode_data = preprocess_file(leetcode_file)
    hackerrank_data = preprocess_file(hackerrank_file)

    combined = leetcode_data + hackerrank_data

    # Save processed JSON
    with open(processed_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed {len(combined)} problems saved to {processed_file}")

    # Build TF-IDF index
    texts = [item["processed_text"] for item in combined]
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Save vectorizer, matrix, and index map
    joblib.dump(vectorizer, tfidf_vectorizer_file)
    sparse.save_npz(tfidf_matrix_file, tfidf_matrix)

    with open(index_map_file, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"✅ TF-IDF vectorizer, matrix, and index map saved to {MODELS_DIR}")
