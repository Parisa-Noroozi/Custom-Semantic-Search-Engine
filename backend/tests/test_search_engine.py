from backend.models.query import Query
from backend.services.search_engine import SearchEngine
from backend.services.search.index import build_index

documents = [

    "Python is a programming language",

    "Machine learning uses data",

    "PyTorch is used for deep learning",

    "Python and machine learning are powerful",

    "Data science uses Python"

]
index = build_index(documents)

engine = SearchEngine(
    documents,
    index,
)

query = Query("python tutorial pdf")

processed_query, results = engine.search(query)

assert processed_query.tokens
assert isinstance(results, list)
assert len(results) > 0
assert "python" in processed_query.tokens

