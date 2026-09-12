from backend.data.documents import DOCUMENTS
from backend.evaluation.dataset import EVALUATION_DATASET
from backend.evaluation.runner import evaluate_search_engine
from backend.services.search.search_engine import SearchEngine


def test_evaluation_runner_processes_all_queries():
    search_engine=SearchEngine(DOCUMENTS)

    evaluation=evaluate_search_engine(
        search_engine,
        EVALUATION_DATASET,
        k=5,
    )

    assert evaluation["summary"]["query_count"] == len(
        EVALUATION_DATASET
    )


def test_evaluation_runner_returns_query_results():
    search_engine=SearchEngine(DOCUMENTS)

    evaluation=evaluate_search_engine(
        search_engine,
        EVALUATION_DATASET,
        k=5,
    )

    assert len(evaluation["queries"]) == len(
        EVALUATION_DATASET
    )


def test_evaluation_scores_are_between_zero_and_one():
    search_engine=SearchEngine(DOCUMENTS)

    evaluation=evaluate_search_engine(
        search_engine,
        EVALUATION_DATASET,
        k=5,
    )

    summary=evaluation["summary"]

    assert 0 <= summary["mean_precision_at_k"] <= 1
    assert 0 <= summary["mean_recall_at_k"] <= 1
    assert 0 <= summary["mrr"] <= 1


def test_each_query_result_contains_metrics():
    search_engine=SearchEngine(DOCUMENTS)
    evaluation=evaluate_search_engine(
        search_engine,
        EVALUATION_DATASET,
        k=5,
    )
    for result in evaluation["queries"]:
        assert"query" in result
        assert"retrieved_documents" in result
        assert"precision_at_k" in result
        assert"recall_at_k" in result
        assert"reciprocal_rank" in result


def test_empty_evaluation_dataset_returns_zero_scores():
    search_engine=SearchEngine(DOCUMENTS)
    evaluation=evaluate_search_engine(
        search_engine,
        [],
        k=5,
    )
    assert evaluation["summary"]["query_count"] == 0
    assert evaluation["summary"]["mean_precision_at_k"] == 0.0
    assert evaluation["summary"]["mean_recall_at_k"] == 0.0
    assert evaluation["summary"]["mrr"] == 0.0