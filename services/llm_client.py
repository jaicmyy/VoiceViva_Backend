import requests
import json
import re

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "phi-3-mini-4k-instruct"

HEADERS = {
    "Content-Type": "application/json"
}


def generate_single_question(subject_name, concept, context, difficulty):
    rules = {
        "easy": "Focus on basic definitions and simple concepts.",
        "medium": "Focus on conceptual and explanation-based questions.",
        "hard": "Focus on analytical, reasoning, and in-depth questions."
    }
    rule = rules.get(difficulty.lower(), "")

    primary_prompt = f"""
You are a university viva examiner. You must generate a question ONLY based on the provided syllabus context.

Subject: {subject_name}
Difficulty: {difficulty}
Rule: {rule}

Syllabus Context (Source of Truth):
{context}

Concept to Target:
{concept}

Instructions:
1. Analyze the provided "Syllabus Context".
2. Ask ONE oral viva question that directly tests the student's knowledge of "{concept}" EXACTLY as it is described in the provided context.
3. DO NOT use external knowledge. Use only the provided context.
4. Output ONLY valid JSON.

Output Format:
{{"question":"string","difficulty":"{difficulty}"}}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Return ONLY JSON. No extra text."},
            {"role": "user", "content": primary_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 80
    }

    try:
        # =========================
        # PRIMARY ATTEMPT
        # =========================
        response = requests.post(
            LM_STUDIO_URL,
            headers=HEADERS,
            json=payload,
            timeout=30 
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        data = extract_json_from_text(content)

        normalized = normalize_llm_output(data, difficulty)
        return normalized

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return None


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
