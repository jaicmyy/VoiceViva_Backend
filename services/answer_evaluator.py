import re
import logging
from typing import Optional

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    if not text: return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def evaluate_answer_tfidf(transcript: str, max_score: float, concepts_text: Optional[str] = None) -> float:
    try:
        if not transcript or not transcript.strip(): return 0.0
        transcript = clean_text(transcript)
        if concepts_text and concepts_text.strip() and SKLEARN_AVAILABLE:
            concepts_text = clean_text(concepts_text)
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([concepts_text, transcript])
            similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
            return min(round(similarity * max_score, 2), max_score)
        
        # Fallback to length
        word_count = len(transcript.split())
        if word_count < 5: return 0.0
        elif word_count < 20: return round(max_score * 0.4, 2)
        else: return float(max_score)
    except Exception:
        return 0.0

def evaluate_answer(transcript: str, max_marks: int):
    # This is the old signature wrapper
    return evaluate_answer_tfidf(transcript, float(max_marks))
