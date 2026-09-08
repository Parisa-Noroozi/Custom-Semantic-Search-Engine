from backend.services.query.query_processor import QueryProcessor
from backend.services.search.search_retriever import SearchRetriever
from backend.services.search.semantic_ranker import SemanticRanker
from backend.services.embeddings.document_embeddings import DocumentEmbeddings
from backend.services.search.result_scorer import ResultScorer
from backend.services.search.result_builder import ResultBuilder


class SearchPipeline:
    def __init__(self, documents):
        self.documents = documents
        self.query_processor = QueryProcessor()
        self.retriever = SearchRetriever(self.documents)
        self.semantic_ranker = SemanticRanker()
        self.document_embedding = DocumentEmbeddings(self.documents)
        

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
        query, weights = self.query_processor.process(query)

        query_vector = self.semantic_ranker.get_query_vector(query.expanded_tokens )
        results = self.retriever.retrieve(query.expanded_tokens)

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