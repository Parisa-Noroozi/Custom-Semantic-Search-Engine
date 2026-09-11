from backend.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_precision_at_k_counts_relevant_results():
    retrieved =["doc1", "doc2", "doc3"]
    relevant = ["doc1", "doc3"]

    score=precision_at_k(
        retrieved,
        relevant,
        k=3,
    )
    assert score == 2 / 3



def test_precision_at_k_respects_k():
    retrieved=["doc1", "doc2", "doc3"]
    relevant=["doc3"]

    score=precision_at_k(
        retrieved,
        relevant,
        k=2,
    )
    assert score == 0


def test_precision_at_k_handles_empty_results():
    score= precision_at_k(
        [],
        ["doc1"],
        k=5,
    )
    assert score == 0.0


def test_recall_at_k_counts_retrieved_relevant_documents():
    retrieved=["doc1", "doc2", "doc3"]
    relevant=["doc1", "doc3", "doc4", "doc5"]

    score=recall_at_k(
        retrieved,
        relevant,
        k=3,
    )
    assert score == 0.5


def test_recall_at_k_returns_zero_without_relevant_documents():
    score=recall_at_k(
        ["doc1"],
        [],
        k=5,
    )
    assert score == 0.0


def test_reciprocal_rank_returns_one_for_first_result():
    score = reciprocal_rank(
        ["doc1", "doc2"],
        ["doc1"],
    )
    assert score == 1.0


def test_reciprocal_rank_uses_first_relevant_position():
    score=reciprocal_rank(
        ["doc1", "doc2", "doc3"],
        ["doc3"],
    )

    assert score == 1 / 3


def test_reciprocal_rank_returns_zero_without_match():
    score=reciprocal_rank(
        ["doc1", "doc2"],
        ["doc3"],
    )
    assert score == 0.0