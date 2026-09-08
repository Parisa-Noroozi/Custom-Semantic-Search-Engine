from backend.services.query.tokenizer import tokenize
from backend.services.intent_detector import IntentDetector
from backend.services.search.search import search
from backend.services.query_expander import QueryExpander
from backend.services.ranking_strategy import RankingStrategy
from backend.services.search.semantic_ranker import SemanticRanker
from backend.services.embeddings.document_embeddings import DocumentEmbeddings
from backend.services.search.result_scorer import ResultScorer
from backend.services.search.result_builder import ResultBuilder


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
        self.result_builder = ResultBuilder(self.intent_keywords)

    

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

            result = self.result_builder.build_result(
                document=document,
                score=score,
                weights=weights,
                score_data=score_data,
                query=query
            )

            new_results.append(result)
            
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