from backend.services.query.tokenizer import tokenize
from backend.services.search.search_retriever import SearchRetriever

class BM25Baseline:
    def __init__(self , documents) :
        self.retriever=SearchRetriever(documents)
        
        
        
    def search(self , query) :
        tokens=tokenize(query.original_query)

        retrieved=self.retriever.retrieve(tokens)
        results=[
            {
                "text": document,
                "bm25_score": score,
            }
            for score, document in retrieved
            if score > 0]
        
        results=results[:5]
        return query , results