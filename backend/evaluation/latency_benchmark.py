from time import perf_counter
from backend.data.documents import DOCUMENTS
from backend.evaluation.baseline import BM25Baseline
from backend.evaluation.dataset import EVALUATION_DATASET
from backend.models.query import Query
from backend.services.search.search_engine import SearchEngine


def measure_query_latency(search_engine, query_text):
    query=Query(query_text)
    start=perf_counter()
    search_engine.search(query)
    end=perf_counter()
    return end - start


def benchmark_search_engine(search_engine, dataset, runs=10):
    latencies=[]
    for _ in range(runs):
        for case in dataset:
            latency=measure_query_latency(
                search_engine,
                case["query"],)
            latencies.append(latency)
            
            
    if not latencies:
        return {
            "measurement_count": 0,
            "mean_latency_ms": 0.0,
            "min_latency_ms": 0.0,
            "max_latency_ms": 0.0,}
    latencies_ms=[
        latency * 1000
        for latency in latencies]   
    return {
        "measurement_count": len(latencies_ms),
        "mean_latency_ms": (sum(latencies_ms) / len(latencies_ms)),
        "min_latency_ms": min(latencies_ms),
        "max_latency_ms": max(latencies_ms),}
    
def run_latency_benchmark(runs=10):
        baseline=BM25Baseline(DOCUMENTS)
        search_engine=SearchEngine(DOCUMENTS)

        baseline_result=benchmark_search_engine(
            baseline,
            EVALUATION_DATASET,
            runs=runs,)

        search_result=benchmark_search_engine(
            search_engine,
            EVALUATION_DATASET,
            runs=runs,)
        return {"baseline": baseline_result, "search_engine": search_result,}
    
    
def format_latency_benchmark(benchmark):
    baseline=benchmark["baseline"]
    search_engine=benchmark["search_engine"]
    lines=[
        "Search Latency Benchmark",
        "============================",
        "",
        "BM25 Baseline",
        (
            "Measurements: "
            f"{baseline['measurement_count']}"
        ),
        (
            "Mean latency: "
            f"{baseline['mean_latency_ms']:.4f} ms"
        ),
        (
            "Min latency: "
            f"{baseline['min_latency_ms']:.4f} ms"
        ),
        (
            "Max latency: "
            f"{baseline['max_latency_ms']:.4f} ms"
        ),
        "",
        "Current Search Engine",
        (
            "Measurements: "
            f"{search_engine['measurement_count']}"
        ),
        (
            "Mean latency: "
            f"{search_engine['mean_latency_ms']:.4f} ms"
        ),
        (
            "Min latency: "
            f"{search_engine['min_latency_ms']:.4f} ms"
        ),
        (
            "Max latency: "
            f"{search_engine['max_latency_ms']:.4f} ms"
        ),]
    return "\n".join(lines)





if __name__ == "__main__":
    benchmark=run_latency_benchmark(runs=10)
    print(format_latency_benchmark( benchmark ))
