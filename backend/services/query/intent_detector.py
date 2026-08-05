from collections import defaultdict
from backend.services.query.tokenizer import tokenize

INTENT_MAP = {
    "Learning": ["learn", "tutorial", "course", "study"],
    "Information": ["what", "is", "explain", "definition"],
    "Resources": ["pdf", "ebook", "notes", "slides"],
    "Career": ["job", "interview", "salary"],
    "Installation": ["install", "setup"],
    "Troubleshooting": ["error", "fix", "problem"],
    "Comparison": ["vs", "compare", "difference"]
}

def detect_intent(query):
    tokens = tokenize(query.lower())
    scores = defaultdict(int)

    for token in tokens:
        for intent, keywords in INTENT_MAP.items():
            if token in keywords:
                scores[intent] += 1

    if not scores:
        return {
            "Primary": "Unknown",
            "Scores": {}
        }

    sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_intents[0][0]

    return { "Primary": primary, "Scores": dict(sorted_intents)}