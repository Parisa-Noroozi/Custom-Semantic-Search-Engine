class RankingEngine:

    def calculate_score(
        self,
        bm25_score,
        semantic_score,
        expansion_bonus,
        intent_bonus,
        exact_bonus=0,
        relation_bonus=0,
        category_bonus=0,
        weights=None,
    ):
        if weights is None:
            weights = {
                "bm25": 0.6,
                "semantic": 1.5,
                "expansion": 0.2,
                "intent": 0.1,
            }

        final_score = (
            bm25_score * weights["bm25"]
            + semantic_score * weights["semantic"]
            + expansion_bonus * weights["expansion"]
            + intent_bonus * weights["intent"]
            + exact_bonus
            + relation_bonus
            + category_bonus
        )

        return final_score

    def relation_bonus(
        self,
        query_concepts,
        document_tokens,
        knowledge,
    ):
        bonus = 0

        for concept in query_concepts:
            if concept not in knowledge:
                continue

            relations = knowledge[concept].get("relations", [])

            for relation in relations:
                relation_tokens = relation.lower().split()

                if all(token in document_tokens for token in relation_tokens):
                    bonus += 0.25

        return bonus