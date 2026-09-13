from backend.evaluation.error_analysis import (analyze_errors, get_relevant_ranks,)
from backend.evaluation.error_analysis import (  analyze_errors,get_relevant_ranks,format_error_analysis,)


def test_error_analysis_returns_all_queries ():
    analysis=analyze_errors(k=5)
    assert len(analysis) == 8
    
    
    
    
def test_error_analysis_contains_comparison_fields() :
    analysis=analyze_errors(k=5)
    result=analysis[0]
    assert "query" in result
    assert "baseline_ndcg" in result
    assert "search_engine_ndcg" in result
    assert "ndcg_difference" in result
    assert "status" in result
    assert "baseline_results" in result
    assert "search_engine_results" in result



def test_error_analysis_uses_valid_statuses() :
    analysis=analyze_errors(k=5)
    valid_statuses={"improved","regressed", "unchanged" }
    assert all(
        result["status"] in valid_statuses
        for result in analysis )
    
    
def test_ndcg_difference_matches_scores() :
    analysis=analyze_errors(k=5)
    for result in analysis:expected=(
            result["search_engine_ndcg"]
            - result["baseline_ndcg"])
    assert result["ndcg_difference"] == expected
    
    
def test_get_relevant_ranks_returns_rank_positions():
    retrieved=[
        "doc1",
        "doc2",
        "doc3",]
    
    relevant=[
        "doc2",
        "doc3",]
    
    ranks=get_relevant_ranks(
        retrieved,
        relevant,)
    
    assert ranks == [{
            "document": "doc2",
            "rank": 2,
        },
        {
            "document": "doc3",
            "rank": 3,},]
    

    
def test_error_analysis_contains_relevance_diagnostics():
    analysis=analyze_errors(k=5)
    for result in analysis:
        assert "relevant_documents" in result
        assert "baseline_relevant_ranks" in result
        assert "search_relevant_ranks" in result
        assert "baseline_missed" in result
        assert "search_missed" in result
        
        
        
        

def test_error_analysis_report_contains_summary():
    analysis=analyze_errors(k=5)
    report=format_error_analysis(
        analysis,
        k=5,)
    assert "Search Error Analysis" in report
    assert "Queries:" in report
    assert "Improved:" in report
    assert "Regressed:" in report
    assert "Unchanged:" in report






