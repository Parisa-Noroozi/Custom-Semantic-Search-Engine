from backend.models.query import Query
from backend.evaluation.metrics import ( precision_at_k,recall_at_k, reciprocal_rank,)


def evaluate_search_engine(search_engine, dataset, k=5):
    query_results=[]
    precision_scores=[]
    recall_scores=[]
    reciprocal_rank_scores=[]
    for case in dataset:
        query_text=case["query"]
        relevant_documents=case["relevant_documents"]
        query= Query(query_text)
        _, results=search_engine.search(query)
        retrieved_documents=[
            result["text"]
            for result in results
        ]
        
        precision=precision_at_k(
            retrieved_documents,
            relevant_documents,
            k,
        )
        recall=recall_at_k(
            retrieved_documents,
            relevant_documents,
            k,
        )

        rr=reciprocal_rank(
            retrieved_documents,
            relevant_documents,
        )

        precision_scores.append(precision)
        recall_scores.append(recall)
        reciprocal_rank_scores.append(rr)

        query_results.append(
            {
                "query": query_text,
                "retrieved_documents": retrieved_documents,
                "precision_at_k": precision,
                "recall_at_k": recall,
                "reciprocal_rank": rr,
            }
        )

    query_count=len(query_results)

    if query_count == 0:
        return {
            "queries": [],
            "summary": {
                "query_count": 0,
                "mean_precision_at_k": 0.0,
                "mean_recall_at_k": 0.0,
                "mrr": 0.0,
            },
        }



    return {
        "queries":query_results,
        "summary":{
            "query_count":query_count,
            "mean_precision_at_k":(
                sum(precision_scores) /query_count
            ),
            "mean_recall_at_k":(
                sum(recall_scores) / query_count
            ),
            "mrr": (
                sum(reciprocal_rank_scores)/ query_count
            ),
        },
    }