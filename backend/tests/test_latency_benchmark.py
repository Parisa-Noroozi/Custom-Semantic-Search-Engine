from backend.evaluation.latency_benchmark import (
    benchmark_search_engine,
    format_latency_benchmark,
    measure_query_latency,
)
from backend.evaluation.baseline import BM25Baseline

def test_measure_query_latency_returns_non_negative_time():
    baseline=BM25Baseline([ "Python programming tutorial", ])
    latency=measure_query_latency( baseline,"python",)
    assert latency >= 0
    
    
    
    
def test_benchmark_returns_expected_measurement_count():
    baseline=BM25Baseline( [ "Python programming tutorial", ] )
    dataset=[{
            "query": "python",
            "relevant_documents": [
                "Python programming tutorial", ],  } ]
    
    result=benchmark_search_engine(
        baseline,
        dataset,
        runs=3,)
    assert result["measurement_count"] == 3
    
    
def test_empty_dataset_returns_zero_latency_summary():
    baseline=BM25Baseline([])
    result=benchmark_search_engine(
        baseline,
        [],
        runs=3,)
    assert result == {
        "measurement_count": 0,
        "mean_latency_ms": 0.0,
        "min_latency_ms": 0.0,
        "max_latency_ms": 0.0,}
    
    
def test_latency_report_contains_both_systems():
    benchmark={
        "baseline": {
            "measurement_count": 10,
            "mean_latency_ms": 1.0,
            "min_latency_ms": 0.5,
            "max_latency_ms": 2.0,
        },
        "search_engine": {
            "measurement_count": 10,
            "mean_latency_ms": 2.0,
            "min_latency_ms": 1.0,
            "max_latency_ms": 3.0, },}
    report=format_latency_benchmark(benchmark)
    assert "Search Latency Benchmark" in report
    assert "BM25 Baseline" in report
    assert "Current Search Engine" in report
    assert "Mean latency" in report


