import requests
import json
import re
import logging
from typing import Tuple

# Standard imports assuming they are in the same folder
try:
    from services.answer_evaluator import evaluate_answer_tfidf
except ImportError:
    # If called from within services folder during testing
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from answer_evaluator import evaluate_answer_tfidf

logger = logging.getLogger(__name__)

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "phi-3-mini-4k-instruct"
HEADERS = {"Content-Type": "application/json"}

def extract_json_from_text(text: str) -> dict:
    match = re.search(r"\{[\s\S]*?\}", text)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group(0))

def evaluate_answer_llm(
    transcript: str,
    question: str,
    concepts: str,
    max_score: float
):
    """
    STRICT UNIVERSITY VIVA EVALUATOR
    """
    words = transcript.strip().split()
    if len(words) < 4:
        return 0.0, "Answer too short to evaluate."

    alpha_ratio = sum(c.isalpha() for c in transcript) / max(len(transcript), 1)
    if alpha_ratio < 0.5:
        return 0.0, "Answer is not meaningful language."

    tfidf_score = evaluate_answer_tfidf(
        transcript=transcript,
        max_score=max_score,
        concepts_text=concepts
    )

    combined_prompt = f"""
You are a strict university viva examiner.
Question: {question}
Expected concepts: {concepts}
Student answer: {transcript}

Evaluate the student's answer and return ONLY JSON in this format:
{{
  "relevance": "YES" | "PARTIAL" | "NO",
  "explains": true | false,
  "score": number, 
  "feedback": "short feedback"
}}
Rules:
1. If relevance is NO, score must be 0.
2. Score must be between 0 and {max_score}.
3. Be strict.
"""

    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers=HEADERS,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": combined_prompt}
                ],
                "temperature": 0.0,
                "max_tokens": 150
            },
            timeout=20
        )
        data = extract_json_from_text(response.json()["choices"][0]["message"]["content"])
        relevance = data.get("relevance", "NO")
        explains = data.get("explains", False)
        llm_score = min(float(data.get("score", 0)), max_score)
        feedback = data.get("feedback", "Evaluated.")

        if relevance == "NO":
            return 0.0, "Answer is not relevant."
        
        if not explains and llm_score > (max_score * 0.4):
             llm_score = max_score * 0.3 # Penalize for lack of explanation

        if relevance == "PARTIAL":
             llm_score = min(llm_score, max_score * 0.5)

        final_score = round((0.3 * tfidf_score) + (0.7 * llm_score), 2)
        return min(final_score, max_score), feedback

    except Exception:
        return min(tfidf_score, max_score * 0.4), "Auto-evaluated (fallback)."
