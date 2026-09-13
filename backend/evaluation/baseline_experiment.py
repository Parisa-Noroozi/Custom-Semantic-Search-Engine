from backend.data.documents import DOCUMENTS
from backend.evaluation.baseline import BM25Baseline
from backend.evaluation.runner import evaluate_search_engine
from backend.services.search.search_engine import SearchEngine
from backend.evaluation.dataset import EVALUATION_DATASET



def run_baseline_experiment(k=5) :
    baseline=BM25Baseline(DOCUMENTS)
    search_engine=SearchEngine(DOCUMENTS)
    baseline_evaluation=evaluate_search_engine(
        baseline,
        EVALUATION_DATASET,
        k=k,)
    search_evaluation=evaluate_search_engine(
        search_engine,
        EVALUATION_DATASET,
        k=k,)
    
    return {
        "baseline" : baseline_evaluation,
        "search_engine" : search_evaluation,}
    
    
def format_baseline_comparison(experiment, k=5):
    baseline=experiment["baseline"]["summary"]
    search_engine=experiment["search_engine"]["summary"]
    lines=[
        "Baseline Experiment",
        "=====================",
        "",
        f"Metric              BM25 Baseline    Search Engine",
        f"Precision@{k}         {baseline['mean_precision_at_k']:.4f}           {search_engine['mean_precision_at_k']:.4f}",
        f"Recall@{k}            {baseline['mean_recall_at_k']:.4f}           {search_engine['mean_recall_at_k']:.4f}",
        f"MRR                 {baseline['mrr']:.4f}           {search_engine['mrr']:.4f}",
        f"nDCG@{k}              {baseline['mean_ndcg_at_k']:.4f}           {search_engine['mean_ndcg_at_k']:.4f}",
    ]
    return "\n".join(lines)
    
    
if __name__ == "__main__" :
      experiment=run_baseline_experiment()
      print(format_baseline_comparison( experiment, k=5,))
