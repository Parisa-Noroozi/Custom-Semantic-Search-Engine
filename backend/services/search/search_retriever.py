from backend.services.search.search import search


class SearchRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.search_function = search

    def retrieve(self, tokens):
        return self.search_function(
            tokens,
            self.documents
        )