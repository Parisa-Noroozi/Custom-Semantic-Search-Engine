from backend.services.query.tokenizer import tokenize
from backend.services.search.ranking_engine import RankingEngine
from backend.services.embeddings.knowledge_base import KNOWLEDGE_BASE


class ResultScorer:
    def __init__(self, semantic_ranker, document_embedding, intent_keywords):
        self.semantic_ranker = semantic_ranker
        self.document_embedding = document_embedding
        self.intent_keywords = intent_keywords
        self.ranker = RankingEngine()

    def apply_intent_bonus(self, score, document, intents):
        document_tokens = set(tokenize(document))
        bonus = 0

        for intent, percentage in intents:
            keywords = self.intent_keywords.get(intent, set())

            if document_tokens.intersection(keywords):
                bonus += percentage / 100

        return score + bonus

    @staticmethod
    def contains_term(document_tokens, term):
        term_tokens = term.split()

        if len(term_tokens) == 1:
            return term in document_tokens

        term_length = len(term_tokens)

        for i in range(len(document_tokens) - term_length + 1):
            if document_tokens[i:i + term_length] == term_tokens:
                return True

        return False

    def score(
        self,
        bm25_score,
        document,
        query,
        query_vector,
        weights
    ):
        document_tokens = tokenize(document)
        document_token_set = set(document_tokens)

        document_concepts = []
        document_vector = self.document_embedding.get(document)

        for token in document_tokens:
            normalized_token = (
                self.semantic_ranker.embedding_engine.normalize_token(token)
            )

            if (
                normalized_token
                in self.semantic_ranker.embedding_engine.knowledge
            ):
                document_concepts.append(normalized_token)

        semantic_score = (
            self.semantic_ranker.semantic_score_from_vector(
                query_vector,
                document_vector
            )
        )

        intent_score = self.apply_intent_bonus(
            bm25_score,
            document,
            query.intents
        )

        intent_bonus = intent_score - bm25_score

        exact_bonus = 0

        for token in query.tokens:
            if token in document_token_set:
                exact_bonus += 2

        expansion_bonus = 0

        for token in query.expanded_tokens:
            if token in query.tokens:
                continue

            if self.contains_term(document_tokens, token):
                expansion_bonus += query.expansion_weights.get(
                    token,
                    0
                )

        query_concepts = (
            self.semantic_ranker.embedding_engine.extract_concepts(
                query.expanded_tokens
            )
        )

        relation_bonus = self.ranker.relation_bonus(
            query_concepts,
            document_token_set,
            KNOWLEDGE_BASE
        )

        category_bonus = self.semantic_ranker.category_similarity(
            query_concepts,
            document_concepts
        )

        final_score = self.ranker.calculate_score(
            bm25_score=bm25_score,
            semantic_score=semantic_score,
            expansion_bonus=expansion_bonus,
            intent_bonus=intent_bonus,
            exact_bonus=exact_bonus,
            relation_bonus=relation_bonus,
            category_bonus=category_bonus,
            weights=weights
        )

        return {
            "document_tokens": document_tokens,
            "document_token_set": document_token_set,
            "semantic_score": semantic_score,
            "intent_bonus": intent_bonus,
            "exact_bonus": exact_bonus,
            "expansion_bonus": expansion_bonus,
            "query_concepts": query_concepts,
            "relation_bonus": relation_bonus,
            "category_bonus": category_bonus,
            "final_score": final_score
        }