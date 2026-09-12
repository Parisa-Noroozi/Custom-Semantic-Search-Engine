from backend.data.documents import DOCUMENTS
from backend.evaluation.dataset import EVALUATION_DATASET
from backend.evaluation.runner import evaluate_search_engine
from backend.services.search.search_engine import SearchEngine


def format_evaluation_report(evaluation, k):
    lines=[
        "Search Evaluation Report",
        "========================",
        "",
    ]

    for result in evaluation["queries"]:
        lines.append(f"Query: {result['query']}")
        lines.append(
            f"Precision@{k}: "
            f"{result['precision_at_k']:.4f}"
        )
        lines.append(
            f"Recall@{k}: "
            f"{result['recall_at_k']:.4f}"
        )
        lines.append(
            "Reciprocal Rank: "
            f"{result['reciprocal_rank']:.4f}"
        )
        lines.append("")
    summary = evaluation["summary"]

    lines.extend(
        [
            "Summary",
            "-------",
            f"Queries: {summary['query_count']}",
            (
                f"Mean Precision@{k}: "
                f"{summary['mean_precision_at_k']:.4f}"
            ),
            (
                f"Mean Recall@{k}: "
                f"{summary['mean_recall_at_k']:.4f}"
            ),
            f"MRR: {summary['mrr']:.4f}",
        ]
    )

    return "\n".join(lines)


def run_evaluation_report(k=5):
    search_engine=SearchEngine(DOCUMENTS)

    evaluation=evaluate_search_engine(
        search_engine,
        EVALUATION_DATASET,
        k=k,
    )

    report=format_evaluation_report(
        evaluation,
        k,
    )

    print(report)


if __name__ == "__main__":
    run_evaluation_report()