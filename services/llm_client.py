import requests
import json
import re

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "phi-3-mini-4k-instruct"

HEADERS = {
    "Content-Type": "application/json"
}


def generate_single_question(subject_name, concepts, difficulty):
    primary_prompt = f"""
You are a university viva examiner.

Subject: {subject_name}
Difficulty: {difficulty}

Concept:
{concepts[0]}

Ask ONE oral viva question.

Output ONLY valid JSON:
{{"question":"string","difficulty":"{difficulty}"}}
"""

    fallback_prompt = f"""
Return ONLY valid JSON.
NO explanation.
NO extra text.

{{"question":"Ask a viva question about {concepts[0]}","difficulty":"{difficulty}"}}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Return ONLY JSON. No extra text."},
            {"role": "user", "content": primary_prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 80
    }

    try:
        # =========================
        # PRIMARY ATTEMPT (Shortened Timeout)
        # =========================
        response = requests.post(
            LM_STUDIO_URL,
            headers=HEADERS,
            json=payload,
            timeout=5 # Reduced for better UX
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        data = extract_json_from_text(content)

        normalized = normalize_llm_output(data, difficulty)
        return normalized

    except Exception as e:
        print(f"[LLM ERROR] {e}. Falling back to hardcoded question.")
        # =========================
        # HARDCODED FALLBACK (Immediate)
        # =========================
        return {
            "question": f"Explain the concept of {concepts[0]} in the context of {subject_name}.",
            "difficulty": difficulty
        }


# ----------------------------------
# JSON EXTRACTION (UNCHANGED LOGIC)
# ----------------------------------
def extract_json_from_text(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    return json.loads(match.group(0))


# ----------------------------------
# SAFE NORMALIZATION (NEW, REQUIRED)
# ----------------------------------
def normalize_llm_output(data, fallback_difficulty):
    question = data.get("question")

    # Handle nested question
    if isinstance(question, dict):
        question = question.get("text")

    if not isinstance(question, str):
        raise ValueError("Invalid question format from LLM")

    difficulty = data.get("difficulty", fallback_difficulty)

    return {
        "question": question.strip(),
        "difficulty": difficulty
    }
