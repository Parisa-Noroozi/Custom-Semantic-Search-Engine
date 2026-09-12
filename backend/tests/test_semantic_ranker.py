from backend.services.search.semantic_ranker import SemanticRanker


def test_semantic_score_returns_zero_without_query_vector():
    ranker=SemanticRanker()

    score=ranker.semantic_score_from_vector(
        None,
        [1, 0],
    )
    assert score == 0


def test_semantic_score_returns_zero_without_document_vector():
    ranker = SemanticRanker()
    score = ranker.semantic_score_from_vector(
        [1, 0],
        None,
    )
    assert score == 0


def test_identical_vectors_have_maximum_similarity():
    ranker=SemanticRanker()
    score=ranker.semantic_score_from_vector(
        [1, 0],
        [1, 0],
    )
    assert score == 1.0


def test_category_similarity_ignores_unknown_concepts():
    ranker=SemanticRanker()
    score= ranker.category_similarity(
        ["unknown-query-concept"],
        ["unknown-document-concept"],
    )
    assert score == 0