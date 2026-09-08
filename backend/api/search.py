from fastapi import APIRouter
from backend.data.documents import DOCUMENTS
from backend.dependencies import search_engine
from backend.models.query import Query


router = APIRouter()


@router.get("/search")
def search_api(q: str):
    query = Query(q)

    query, results = search_engine.search(query)

    return {
        "query": query.original_query,
        "tokens": query.tokens,
        "expanded_tokens": query.expanded_tokens,
        "expansion_reason": query.expansion_reason,
        "intents": query.intents,
        "results": results,
        "stats": {
            "documents_scanned": len(DOCUMENTS),
            "returned_results": len(results),
            "original_tokens": len(query.tokens),
            "expanded_tokens": len(query.expanded_tokens),
            "added_terms": (
                len(query.expanded_tokens)
                - len(query.tokens)
            ),
        },
    }