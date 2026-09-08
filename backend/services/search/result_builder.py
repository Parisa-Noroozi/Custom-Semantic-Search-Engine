class ResultBuilder:
    def __init__(self, intent_keywords):
        self.intent_keywords = intent_keywords

    def get_matched_intents(self, document_token_set, intents):
        matched_intents = []

        for intent, percentage in intents:
            keywords = self.intent_keywords.get(intent, set())

            if document_token_set.intersection(keywords):
                matched_intents.append(intent)

        return matched_intents

    def build_reason(
        self,
        query,
        document_tokens,
        matched_intents,
        score,
        semantic_score,
        intent_bonus,
        expansion_bonus,
        exact_bonus,
        relation_bonus,
        category_bonus
    ):
        reason = []

        if relation_bonus > 0:
            reason.append(
                f"Relation Bonus: +{round(relation_bonus, 2)}"
            )

        if category_bonus > 0:
            reason.append(
                f"Category Bonus: +{round(category_bonus, 2)}"
            )

        for token in query.tokens:
            if token in document_tokens:
                reason.append(
                    f"Contains keyword: {token}"
                )

        for intent in matched_intents:
            reason.append(
                f"Matched Intent: {intent}"
            )

        reason.append(
            f"BM25 Score: {round(score, 2)}"
        )

        reason.append(
            f"Intent Bonus: +{round(intent_bonus, 2)}"
        )

        reason.append(
            f"Expansion Bonus: +{round(expansion_bonus, 2)}"
        )

        reason.append(
            f"Exact Match Bonus: +{round(exact_bonus, 2)}"
        )

        reason.append(
            f"Semantic Score: {round(semantic_score, 3)}"
        )

        return reason

    def build_result(
        self,
        document,
        score,
        weights,
        score_data,
        query
    ):
        document_tokens = score_data["document_tokens"]
        document_token_set = score_data["document_token_set"]
        semantic_score = score_data["semantic_score"]
        intent_bonus = score_data["intent_bonus"]
        expansion_bonus = score_data["expansion_bonus"]
        exact_bonus = score_data["exact_bonus"]
        relation_bonus = score_data["relation_bonus"]
        category_bonus = score_data["category_bonus"]
        final_score = score_data["final_score"]
        query_concepts = score_data["query_concepts"]

        matched_intents = self.get_matched_intents(
            document_token_set,
            query.intents
        )

        reason = self.build_reason(
            query=query,
            document_tokens=document_tokens,
            matched_intents=matched_intents,
            score=score,
            semantic_score=semantic_score,
            intent_bonus=intent_bonus,
            expansion_bonus=expansion_bonus,
            exact_bonus=exact_bonus,
            relation_bonus=relation_bonus,
            category_bonus=category_bonus
        )

        return {
            "text": document,
            "bm25_score": round(score, 2),
            "intent_bonus": round(intent_bonus, 2),
            "expansion_bonus": round(expansion_bonus, 2),
            "final_score": round(final_score, 2),
            "bm25_weight": weights["bm25"],
            "intent_weight": weights["intent"],
            "expansion_weight": weights["expansion"],
            "semantic_score": round(semantic_score, 3),
            "semantic_weight": weights["semantic"],
            "ranking_reason": weights["reason"],
            "matched_intents": matched_intents,
            "reason": reason,
            "exact_bonus": round(exact_bonus, 2),
            "relation_bonus": round(relation_bonus, 2),
            "category_bonus": round(category_bonus, 2),
            "query_concepts": query_concepts
        }