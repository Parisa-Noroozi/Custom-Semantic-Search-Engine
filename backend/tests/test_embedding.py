from backend.services.embeddings.embedding_engine import EmbeddingEngine
from backend.services.embeddings.similarity import cosine_similarity
from backend.services.search.semantic_ranker import SemanticRanker

engine = EmbeddingEngine()

print("====== TEST 1 ======")
print(engine.get_vector("python"))

print("\n====== TEST 2 ======")
print(engine.get_query_vector([
    "python",
    "machine",
    "learning"
]))

print("\n====== TEST 3 ======")
print(engine.get_vector("banana"))

print("\n====== TEST 4 ======")
print(engine.get_query_vector([
    "banana",
    "orange"
]))

print("\n====== TEST 5 ======")

print(
    engine.get_query_vector(
        [
            "python",
            "banana",
            "learning"
        ]
    )
)

print("\n====== TEST 6 ======")

print(
    engine.get_document_vector(
        "Python programming tutorial"
    )
)

print("\n====== TEST 7 ======")

query = engine.get_query_vector(

    [

        "python",

        "learning"

    ]

)

doc = engine.get_document_vector(

    "Python programming tutorial"

)

print(

    cosine_similarity(

        query,

        doc

    )

)



ranker = SemanticRanker()

print("\n====== TEST 8 ======")

print(

    ranker.semantic_score(

        ["python", "learning"],

        "Python programming tutorial"

    )

)


engine = EmbeddingEngine()

print(engine.normalize_token("coding"))
print(engine.normalize_token("programming"))
print(engine.normalize_token("script"))
print(engine.normalize_token("py"))
print(engine.normalize_token("python"))

print(engine.get_query_vector(["coding"]))
print(engine.get_query_vector(["script"]))
print(engine.get_query_vector(["programming"]))
