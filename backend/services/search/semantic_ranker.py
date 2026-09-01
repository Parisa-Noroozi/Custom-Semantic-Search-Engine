from backend.services.embeddings.embedding_engine import EmbeddingEngine
from backend.services.embeddings.similarity import cosine_similarity



class SemanticRanker:

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()

    def get_query_vector(self, query_tokens):
        return self.embedding_engine.get_query_vector(query_tokens)


    def semantic_score_from_vector(
            self,
            query_vector,
            document_vector,
    ):
        if query_vector is None or document_vector is None:
            return 0

        return cosine_similarity(query_vector, document_vector)


    def semantic_score(
            self,
            query_tokens,
            document_vector,
    ):
        query_vector = self.get_query_vector(query_tokens)

        return self.semantic_score_from_vector(
            query_vector,
            document_vector,
        )
        
        
        
    def category_similarity(
                self,
                query_concepts,
                document_concepts
        ):
            score = 0
            for qc in query_concepts:
                if qc not in self.embedding_engine.knowledge:
                    continue
                query_category = self.embedding_engine.knowledge[qc].get( "category")

                for dc in document_concepts:
                    if dc not in self.embedding_engine.knowledge:
                        continue
                    document_category = self.embedding_engine.knowledge[dc].get( "category" )
                    if query_category == document_category:
                        score += 0.15

            return score
        
       