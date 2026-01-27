import re


def extract_concepts(text, max_concepts=20):
    """
    Final, syllabus-safe concept extractor.
    Filters headers, objectives, outcomes, and metadata.
    """

    text = text.replace("\n", " ")
    text = text.replace("–", "-")
    text = re.sub(r"\s+", " ", text)

    raw_parts = re.split(r"-|;", text)

    # Capture context: for each part, find where it is in the original text
    # and grab a window of text around it.
    results = []
    seen = set()

    BLOCKLIST = (
        "l t p c",
        "prerequisite",
        "course objective",
        "course outcome",
        "on successful completion",
        "ability to",
        "understand the",
        "discuss the",
        "recognize the",
        "design the",
        "csa",
        "unit"
    )
    
    # Pre-process text for easier searching
    clean_text = re.sub(r"\s+", " ", text)
    
    for part in raw_parts:
        part = part.strip()
        if len(part.split()) < 3:
            continue

        lower = part.lower()
        if any(bad in lower for bad in BLOCKLIST):
            continue
        if lower in seen:
            continue

        seen.add(lower)
        
        # 🔹 Find context (the sentence or block it belongs to)
        # We search for the part in the clean_text
        match = re.search(re.escape(part), clean_text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 200)
            end = min(len(clean_text), match.end() + 200)
            context = clean_text[start:end].strip()
        else:
            context = part # Fallback to just the part

        results.append({
            "concept": part,
            "context": context
        })

        if len(results) >= max_concepts:
            break

    return results
