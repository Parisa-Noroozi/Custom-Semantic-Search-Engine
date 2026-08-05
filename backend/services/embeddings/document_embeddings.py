from backend.services.embeddings.embedding_engine import EmbeddingEngine


class DocumentEmbeddings:

    def __init__(self, documents):
        self.engine = EmbeddingEngine()
        self.cache = {}

        for document in documents:
            self.cache[document] = self.engine.get_document_vector(document)

    def get(self, document):
        return self.cache.get(document)