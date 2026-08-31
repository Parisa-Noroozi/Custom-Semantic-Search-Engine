class RankingStrategy:

    def get_weights(self, intents, tokens):
        weights = {
            "bm25": 0.6,
            "semantic": 1.5,
            "intent": 0.1,
            "expansion": 0.2,
            "reason": "Default strategy",
        }

        intent_names = [intent for intent, _ in intents]

        if "Learning" in intent_names:
            weights = {
                "bm25": 1.0,
                "semantic": 1.5,
                "intent": 1.6,
                "expansion": 1.3,
                "reason": "Learning query detected",
            }

        elif "PDF" in intent_names:
            weights = {
                "bm25": 1.0,
                "semantic": 1.5,
                "intent": 2.0,
                "expansion": 1.1,
                "reason": "PDF query detected",
            }

        elif len(tokens) >= 4:
            weights = {
                "bm25": 1.5,
                "semantic": 1.5,
                "intent": 0.8,
                "expansion": 1.2,
                "reason": "Long technical query",
            }

        return weights