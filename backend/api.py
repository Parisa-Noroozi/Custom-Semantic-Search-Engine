from fastapi import FastAPI
from backend.models.query import Query
from backend.services.query.autocomplete import autocomplete
from backend.services.search.index import build_index
from fastapi.middleware.cors import CORSMiddleware
from backend.services.search_engine import SearchEngine
from backend.data.documents import DOCUMENTS


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

index = build_index(DOCUMENTS)
engine=SearchEngine(DOCUMENTS,index)

@app.get("/search")
def search_api(q: str):
    query = Query(q)
    query, results = engine.search(query)

    return {
        "query":query.original_query,
        "tokens":query.tokens,
        "expanded_tokens": query.expanded_tokens,
        "expansion_reason":query.expansion_reason,
        "intents": query.intents,
        "results":results,
        "stats":{

    "documents_scanned": len(DOCUMENTS),
    "returned_results": len(results),
    "original_tokens": len(query.tokens),
    "expanded_tokens": len(query.expanded_tokens),
    "added_terms": len(query.expanded_tokens)-len(query.tokens)

}
    }


@app.get("/suggest")
def suggest(q: str):
    return autocomplete(q, index)


@app.get("/")
def home():
    return {"message": "Smart Search Engine"}


