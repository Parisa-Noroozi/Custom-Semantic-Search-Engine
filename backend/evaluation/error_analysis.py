from backend.evaluation.baseline_experiment import run_baseline_experiment
from backend.evaluation.dataset import EVALUATION_DATASET



def get_relevant_ranks(retrieved_documents, relevant_documents):
    relevant_set=set(relevant_documents)
    ranks=[]
    for rank, document in enumerate(
        retrieved_documents,
        start=1, ):
        if document in relevant_set:
            ranks.append({
                    "document": document,
                    "rank": rank,} )
            
    return ranks


def analyze_errors(k=5):
    experiment=run_baseline_experiment(k=k)
    baseline_queries=experiment["baseline"]["queries"]
    search_queries=experiment["search_engine"]["queries"]
    analysis=[]
    for case, baseline_result, search_result in zip(
    EVALUATION_DATASET,
    baseline_queries,
    search_queries,):
        difference=(
            search_result["ndcg_at_k"]
            - baseline_result["ndcg_at_k"])
        if difference > 0 :
            status="improved"
        elif difference < 0:
            status="regressed"
        else :
            status="unchanged"
            
        relevant_documents=case["relevant_documents"]
        baseline_relevant_ranks=get_relevant_ranks(baseline_result["retrieved_documents"],relevant_documents,)
        search_relevant_ranks=get_relevant_ranks(
            search_result["retrieved_documents"],
            relevant_documents,)    
        baseline_missed=[
            document
            for document in relevant_documents
            if document not in baseline_result["retrieved_documents"]]
        search_missed=[
            document
            for document in relevant_documents
            if document not in search_result["retrieved_documents"]]

            
        analysis.append({
           "query": baseline_result["query"],
                "baseline_ndcg": baseline_result["ndcg_at_k"],
                "search_engine_ndcg": search_result["ndcg_at_k"],
                "ndcg_difference": difference,
                "status": status,
                "baseline_results": baseline_result["retrieved_documents"] ,
                "search_engine_results": search_result["retrieved_documents"] , 
                                "relevant_documents": relevant_documents,
                "baseline_relevant_ranks": baseline_relevant_ranks,
                "search_relevant_ranks": search_relevant_ranks,
                "baseline_missed": baseline_missed,
                "search_missed": search_missed,} )
    return analysis



def format_error_analysis(analysis, k=5):
    improved=sum( 1 for result in analysis if result["status"] == "improved")
    regressed=sum(1 for result in analysis  if result["status"] == "regressed")
    unchanged=sum( 1 for result in analysis if result["status"] == "unchanged")
    lines=[
        "Search Error Analysis",
        "=====================",
        "",
        f"Queries: {len(analysis)}",
        f"Improved: {improved}",
        f"Regressed: {regressed}",
        f"Unchanged: {unchanged}",]
    for result in analysis:
        if result["status"] == "unchanged":
            continue
        lines.extend([
                "",
                f"Query: {result['query']}",
                f"Status: {result['status']}",
                (
                    f"Baseline nDCG@{k}: "
                    f"{result['baseline_ndcg']:.4f}"
                ),
                (
                    f"Search Engine nDCG@{k}: "
                    f"{result['search_engine_ndcg']:.4f}"
                ),
                (
                    "Difference: "
                    f"{result['ndcg_difference']:.4f}"
                ),
                "Baseline relevant ranks:",])
        for item in result["baseline_relevant_ranks"]:
            lines.append( f"  Rank {item['rank']}: {item['document']}")
            
        lines.append("Search Engine relevant ranks:")
        for item in result["search_relevant_ranks"]:
            lines.append(
                f"  Rank {item['rank']}: {item['document']}")
            
    return "\n".join(lines)       




if __name__ == "__main__":
    analysis=analyze_errors(k=5)
    print( format_error_analysis(  analysis, k=5, ) )


