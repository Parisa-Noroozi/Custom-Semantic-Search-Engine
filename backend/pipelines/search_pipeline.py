from backend.services.query.tokenizer import tokenize
from backend.services.intent_detector import IntentDetector
from backend.services.search.search import search
from backend.services.query_expander import QueryExpander
from backend.services.ranking_strategy import RankingStrategy
from backend.services.search.semantic_ranker import SemanticRanker
from backend.services.embeddings.document_embeddings import DocumentEmbeddings
from backend.services.search.result_scorer import ResultScorer


class SearchPipeline:
    def __init__(self, documents):
        self.documents = documents
        self.intent_detector = IntentDetector()
        self.query_expander = QueryExpander()
        self.ranking_strategy = RankingStrategy()
        self.semantic_ranker = SemanticRanker()
        self.document_embedding = DocumentEmbeddings(self.documents)
        self.search_function = search

        self.intent_keywords = {
            "Learning": {
                "learn",
                "learning",
                "tutorial",
                "course",
                "guide",
                "education"
            },
            "PDF": {
                "pdf",
                "ebook",
                "book",
                "document"
            }
        }
        self.result_scorer = ResultScorer(
            self.semantic_ranker,
            self.document_embedding,
            self.intent_keywords
        )

    

    def search(self, query):
        tokens = tokenize(query.original_query)
        query.set_tokens(tokens)

        intents = self.intent_detector.detect_intent(tokens)
        query.set_intents(intents)

        expanded_tokens, expansion_reason, expansion_weights = (
            self.query_expander.expand_query(tokens)
        )

        query.set_expanded_tokens(expanded_tokens)
        query.set_expansion_reason(expansion_reason)
        query.set_expansion_weights(expansion_weights)

        weights = self.ranking_strategy.get_weights(
            query.intents,
            query.tokens
        )

        query_vector = self.semantic_ranker.get_query_vector(
            query.expanded_tokens
        )

        results = self.search_function(
            query.expanded_tokens,
            self.documents
        )

        new_results = []

        for score, document in results:
            score_data = self.result_scorer.score(
                bm25_score=score,
                document=document,
                query=query,
                query_vector=query_vector,
                weights=weights
            )

            document_tokens = score_data["document_tokens"]
            document_token_set = score_data["document_token_set"]
            semantic_score = score_data["semantic_score"]
            intent_bonus = score_data["intent_bonus"]
            exact_bonus = score_data["exact_bonus"]
            expansion_bonus = score_data["expansion_bonus"]
            query_concepts = score_data["query_concepts"]
            relation_bonus = score_data["relation_bonus"]
            category_bonus = score_data["category_bonus"]
            final_score = score_data["final_score"]
            matched_intents = []

            for intent, percentage in query.intents:
                keywords = self.intent_keywords.get(intent, set())

                if document_token_set.intersection(keywords):
                    matched_intents.append(intent)

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

            new_results.append({
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
            })

        new_results = [
            result
            for result in new_results
            if result["final_score"] > 0
        ]

        new_results.sort(
            key=lambda item: item["final_score"],
            reverse=True
        )

        new_results = new_results[:5]

        return query, new_results