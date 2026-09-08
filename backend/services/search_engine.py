from backend.pipelines.search_pipeline import SearchPipeline


class SearchEngine:
    def __init__(self, documents):
        self.pipeline = SearchPipeline(documents)

    def search(self, query):
        return self.pipeline.search(query)