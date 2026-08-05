class RankingEngine:

    def __init__(
        self,
        bm25_weight=0.6,
        semantic_weight=1.5,
        expansion_weight=0.2,
        intent_weight=0.1
    ):
        self.bm25_weight = bm25_weight
        self.semantic_weight = semantic_weight
        self.expansion_weight = expansion_weight
        self.intent_weight = intent_weight



    def calculate_score(
        self,
        bm25_score,
        semantic_score,
        expansion_bonus,
        intent_bonus,
        exact_bonus=0
    ):
        final_score = (
            bm25_score * self.bm25_weight
            +
            semantic_score * self.semantic_weight
            +
            expansion_bonus
            +
            intent_bonus 
            +
            exact_bonus
        )
        return final_score
    
    
    def relation_bonus(
            self,
            query_concepts,
            document_tokens,
            knowledge
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