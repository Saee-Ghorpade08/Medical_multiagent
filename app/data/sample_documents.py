"""Small educational sample library; not intended for clinical decision-making."""

SAMPLE_DOCUMENTS = [
    {
        "title": "HbA1c overview",
        "content": (
            "HbA1c (glycated hemoglobin) reflects average blood glucose over roughly "
            "the previous two to three months. Interpretation depends on clinical context "
            "and laboratory standards; a healthcare professional should explain personal results."
        ),
        "keywords": ["hba1c", "a1c", "glycated hemoglobin", "glucose", "diabetes"],
    },
    {
        "title": "Blood pressure overview",
        "content": (
            "Blood pressure describes the force of blood against artery walls and is usually "
            "reported as systolic over diastolic pressure. A single measurement may not represent "
            "a person's usual blood pressure; measurement technique and clinical context matter."
        ),
        "keywords": ["blood pressure", "systolic", "diastolic", "hypertension"],
    },
    {
        "title": "Hemoglobin overview",
        "content": (
            "Hemoglobin is a protein in red blood cells that carries oxygen. Hemoglobin results "
            "are interpreted using the laboratory's reference interval and factors such as age, "
            "pregnancy status, altitude, and medical history."
        ),
        "keywords": ["hemoglobin", "haemoglobin", "cbc", "red blood cells", "oxygen"],
    },
    {
        "title": "Reference ranges and research",
        "content": (
            "Laboratory reference intervals can vary with the method, laboratory, and population. "
            "Researchers should document data sources, sample characteristics, measurement methods, "
            "limitations, and uncertainty. Reference intervals alone do not establish a diagnosis."
        ),
        "keywords": ["reference range", "reference interval", "research", "laboratory", "study"],
    },
]


def search_library(query: str, limit: int = 3) -> list[dict[str, str]]:
    """Return sample notes ranked by simple keyword overlap."""
    words = set(query.lower().replace("?", " ").replace(",", " ").split())
    scored = []
    for doc in SAMPLE_DOCUMENTS:
        searchable = set(doc["keywords"])
        searchable.update(doc["title"].lower().split())
        searchable.update(doc["content"].lower().split())
        score = sum(1 for word in words if len(word) > 2 and any(word in term or term in word for term in searchable))
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [{"title": doc["title"], "content": doc["content"]} for _, doc in scored[:limit]]
