class RankingStrategy:

    DEFAULT_WEIGHTS = {
        "bm25": 0.6,
        "semantic": 1.5,
        "intent": 0.1,
        "expansion": 0.2,
    }

    INTENT_PROFILES = {
        "Learning": {
            "bm25": 1.0,
            "intent": 1.6,
            "expansion": 1.3,
        },
        "PDF": {
            "bm25": 1.0,
            "intent": 2.0,
            "expansion": 1.1,
        },
    }

    LONG_QUERY_PROFILE = {
        "bm25": 1.5,
        "intent": 0.8,
        "expansion": 1.2,
    }

    def get_weights(self, intents, tokens):
        weights = self.DEFAULT_WEIGHTS.copy()
        reasons = []

        intent_names = [intent for intent, _ in intents]

        for intent_name in intent_names:
            profile = self.INTENT_PROFILES.get(intent_name)

            if profile is None:
                continue

            self._merge_profile(weights, profile)
            reasons.append(f"{intent_name} query detected")

        if len(tokens) >= 4:
            self._merge_profile(weights, self.LONG_QUERY_PROFILE)
            reasons.append("Long technical query")

        weights["reason"] = (
            " + ".join(reasons)
            if reasons
            else "Default strategy"
        )

        return weights

    @staticmethod
    def _merge_profile(weights, profile):
        for key, value in profile.items():
            weights[key] = max(weights[key], value)