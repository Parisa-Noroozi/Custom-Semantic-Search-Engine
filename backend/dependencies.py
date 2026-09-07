from backend.data.documents import DOCUMENTS
from backend.services.query.autocomplete import autocomplete
from backend.services.search.index import build_index
from backend.services.search_engine import SearchEngine


index = build_index(DOCUMENTS)

search_engine = SearchEngine(DOCUMENTS)


def get_suggestions(query):
    return autocomplete(query, index)