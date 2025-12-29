import requests
import json

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
NO text.
NO explanation.

{{"question":"Ask a viva question about {concepts[0]}","difficulty":"{difficulty}"}}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Return ONLY JSON. No extra text."},
            {"role": "user", "content": primary_prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 60
    }

    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers=HEADERS,
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]

        if content:
            try:
                data = extract_json_from_text(content)
                return {
                    "question": data["question"].strip(),
                    "difficulty": data["difficulty"]
                }
            except:
                pass  # go to fallback

        # 🔁 FALLBACK ATTEMPT (STRICT)
        payload["messages"][1]["content"] = fallback_prompt

        response = requests.post(
            LM_STUDIO_URL,
            headers=HEADERS,
            json=payload,
            timeout=300
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        data = extract_json_from_text(content)

        return {
            "question": data["question"].strip(),
            "difficulty": data["difficulty"]
        }

    except Exception as e:
        print(f"[LLM FINAL FAIL] {difficulty} | {concepts[0][:40]}... : {e}")
        return None

    
    
import json
import re

def extract_json_from_text(text):
    """
    Extracts the FIRST valid JSON object from LLM output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")

    json_str = match.group(0)
    return json.loads(json_str)

    return {
        "question": data["question"].strip(),
        "difficulty": data["difficulty"]
    }
