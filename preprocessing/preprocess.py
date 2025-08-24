# preprocessing/preprocess.py
import re
import spacy
import nltk
from nltk.corpus import stopwords

# ensure nlp model loaded (run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
nltk.download('stopwords', quiet=True)
STOPWORDS = set(stopwords.words("english"))

def clean_html(html: str) -> str:
    # remove code blocks and HTML tags conservatively (you might want to keep code separately)
    text = re.sub(r"<pre.*?>.*?</pre>", " ", html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r"<code.*?>.*?</code>", " ", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+", " ", text)
    return text

def normalize_text(text: str) -> str:
    text = text or ""
    text = clean_html(text)
    text = text.lower()
    # keep alphnumeric and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    # spaCy lemmatization + remove stopwords and single letters
    doc = nlp(text)
    tokens = []
    for tok in doc:
        lemma = tok.lemma_.strip()
        if not lemma or len(lemma) <= 1:
            continue
        if lemma in STOPWORDS:
            continue
        if not lemma.isalpha():
            continue
        tokens.append(lemma)
    return " ".join(tokens)

# quick test
if __name__ == "__main__":
    sample = "<p>This is a sample problem: given an array, find sum.</p><pre><code>int main(){}</code></pre>"
    print(normalize_text(sample))
