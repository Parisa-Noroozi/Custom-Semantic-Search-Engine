from backend.evaluation.baseline_experiment import (run_baseline_experiment,format_baseline_comparison,)

def test_baseline_experiment_returns_both_systems() :
    experiment=run_baseline_experiment(k=5)
    assert "baseline" in experiment
    assert "search_engine" in experiment
    
    
    
def test_baseline_experiment_uses_same_query_count() :
    experiment=run_baseline_experiment(k=5)
    baseline_count=experiment["baseline"]["summary"]["query_count"]
    search_count=experiment["search_engine"]["summary"]["query_count"]
    assert baseline_count == search_count


def test_baseline_experiment_returns_comparable_metrics() :
    experiment=run_baseline_experiment(k=5)
    baseline_summary=experiment["baseline"]["summary"]
    search_summary=experiment["search_engine"]["summary"]
    metrics=[
        "mean_precision_at_k",
        "mean_recall_at_k",
        "mrr",
        "mean_ndcg_at_k",]
    
    for metric in metrics:
        assert metric in baseline_summary
        assert metric in search_summary
        
        
def test_baseline_comparison_contains_both_systems ():
    experiment=run_baseline_experiment(k=5)
    report=format_baseline_comparison(experiment,k=5, )
    assert "BM25 Baseline" in report
    assert "Search Engine" in report
    assert "Precision@5" in report
    assert "Recall@5" in report
    assert "MRR" in report
    assert "nDCG@5" in report