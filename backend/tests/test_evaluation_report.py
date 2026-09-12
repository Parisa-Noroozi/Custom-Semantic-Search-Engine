from backend.evaluation.report import format_evaluation_report


def test_report_contains_title():
    evaluation = {
        "queries": [],
        "summary": {
            "query_count": 0,
            "mean_precision_at_k": 0.0,
            "mean_recall_at_k": 0.0,
            "mrr": 0.0,
        },
    }

    report = format_evaluation_report(
        evaluation,
        k=5,
    )
    assert "Search Evaluation Report" in report


def test_report_contains_summary_metrics():
    evaluation = {
        "queries": [],
        "summary": {
            "query_count": 2,
            "mean_precision_at_k": 0.5,
            "mean_recall_at_k": 0.75,
            "mrr": 1.0,
        },
    }

    report = format_evaluation_report(
        evaluation,
        k=5,
    )
    assert "Queries: 2" in report
    assert "Mean Precision@5: 0.5000" in report
    assert "Mean Recall@5: 0.7500" in report
    assert "MRR: 1.0000" in report


def test_report_contains_query_metrics():
    evaluation = {
        "queries": [
            {
                "query": "python",
                "retrieved_documents": ["doc1"],
                "precision_at_k": 0.2,
                "recall_at_k": 1.0,
                "reciprocal_rank": 1.0,
            }
        ],
        "summary": {
            "query_count": 1,
            "mean_precision_at_k": 0.2,
            "mean_recall_at_k": 1.0,
            "mrr": 1.0,
        },
    }

    report = format_evaluation_report(
        evaluation,
        k=5,
    )
    assert "Query: python" in report
    assert "Precision@5: 0.2000" in report
    assert "Recall@5: 1.0000" in report
    assert "Reciprocal Rank: 1.0000" in report


def test_report_uses_requested_k():
    evaluation = {
        "queries": [],
        "summary": {
            "query_count": 0,
            "mean_precision_at_k": 0.0,
            "mean_recall_at_k": 0.0,
            "mrr": 0.0,
        },
    }
    report = format_evaluation_report(
        evaluation,
        k=3,
    )
    assert "Mean Precision@3" in report
    assert "Mean Recall@3" in report