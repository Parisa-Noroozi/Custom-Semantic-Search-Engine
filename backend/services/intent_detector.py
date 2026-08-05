from collections import defaultdict


class IntentDetector:
    def __init__(self):
        self.intent_keywords = {

            "Learning": {
                "learn",
                "learning",
                "tutorial",
                "course",
                "education"
            },

            "PDF": {
                "pdf",
                "ebook",
                "book",
                "document"
            }
        }

    def detect_intent(self, tokens):
        scores = defaultdict(int)

        for token in tokens:
            for intent, keywords in self.intent_keywords.items():
                if token in keywords:
                    scores[intent] += 1
        intents = []

        for intent, count in scores.items():
            percentage = round((count / len(tokens)) * 100)
            if percentage > 0:
                intents.append((intent, percentage))
        intents.sort( key=lambda item: item[1], reverse=True)

        return intents
    
   