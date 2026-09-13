from backend.data.documents import DOCUMENTS
from backend.evaluation.baseline import BM25Baseline
from backend.models.query import Query


def test_bm25_baseline_returns_matching_documents() :
    baseline=BM25Baseline(DOCUMENTS)
    query=Query("python")
    _, results=baseline.search(query)
    assert len(results) > 0
    assert all( "text" in result for result in results )
    
    
def test_bm25_baseline_returns_at_most_five_results():
    baseline=BM25Baseline(DOCUMENTS)
    query=Query("python")
    _, results=baseline.search(query)
    assert len(results) <= 5
    
    
def test_bm25_baseline_keeps_positive_scores():
    baseline=BM25Baseline(DOCUMENTS)
    query=Query("python")
    _, results=baseline.search(query)
    assert all(
        result["bm25_score"] > 0
        for result in results)

def test_bm25_baseline_uses_raw_query_without_expansion() :
    baseline=BM25Baseline(DOCUMENTS)
    query=Query("python")
    baseline.search(query)
    assert query.expanded_tokens == []