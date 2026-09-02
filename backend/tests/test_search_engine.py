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
index,  document_frequency = build_index(documents)

engine = SearchEngine(
    documents,
    index,
)

query = Query("python tutorial pdf")

result = engine.search(query)

print(result.tokens)

print(result.status)


