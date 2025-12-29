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

    concepts = []
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
        concepts.append(part)

        if len(concepts) >= max_concepts:
            break

    return concepts
