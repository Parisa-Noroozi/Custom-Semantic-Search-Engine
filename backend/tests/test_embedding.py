from backend.services.embeddings.embedding_engine import EmbeddingEngine
from backend.services.embeddings.similarity import cosine_similarity
from backend.services.search.semantic_ranker import SemanticRanker


engine = EmbeddingEngine()


python_vector = engine.get_vector("python")

assert python_vector is not None
assert len(python_vector) == len(engine.topic_space)


query_vector = engine.get_query_vector([
    "python",
    "machine",
    "learning",
])

assert query_vector is not None
assert len(query_vector) == len(engine.topic_space)


unknown_vector = engine.get_vector("banana")

assert unknown_vector is None


unknown_query_vector = engine.get_query_vector([
    "banana",
    "orange",
])

assert unknown_query_vector is None


mixed_query_vector = engine.get_query_vector([
    "python",
    "banana",
    "learning",
])

assert mixed_query_vector is not None
assert len(mixed_query_vector) == len(engine.topic_space)


document_vector = engine.get_document_vector(
    "Python programming tutorial"
)

assert document_vector is not None
assert len(document_vector) == len(engine.topic_space)


query_vector = engine.get_query_vector([
    "python",
    "learning",
])

document_vector = engine.get_document_vector(
    "Python programming tutorial"
)

similarity = cosine_similarity(
    query_vector,
    document_vector,
)

assert similarity > 0
assert similarity <= 1


ranker = SemanticRanker()

query_vector = ranker.get_query_vector([
    "python",
    "learning",
])

document_vector = engine.get_document_vector(
    "Python programming tutorial"
)

score = ranker.semantic_score_from_vector(
    query_vector,
    document_vector,
)

assert score > 0
assert score <= 1


assert engine.normalize_token("coding") == "coding"
assert engine.normalize_token("programming") == "programming"
assert engine.normalize_token("script") == "script"
assert engine.normalize_token("py") == "python"
assert engine.normalize_token("python") == "python"


assert engine.get_query_vector(["coding"]) is None
assert engine.get_query_vector(["script"]) is None
assert engine.get_query_vector(["programming"]) is None