from math import log2


def precision_at_k(retrieved, relevant , k):
    if k <= 0:
        return 0.0
    
    top_k=retrieved [:k]
    relevant_set=set(relevant)
    
    maches=sum(
        1
        for document in top_k
        if document in relevant_set)
    return maches / k


def recall_at_k(retrieved, relevant ,k ):
    if k <= 0 or not relevant:
        return 0.0
    
    top_k=retrieved[:k]
    relevant_set=set(relevant)
    
    matches=sum(
        1
        for document in top_k
        if document in relevant_set)
    return matches / len(relevant_set)


def reciprocal_rank(retrieved, relevant ):
    relevant_set=set( relevant)
    for rank, document in enumerate(retrieved , start=1):
        if document in relevant_set:
            return 1 / rank

    return 0.0




def dcg_at_k(retrieved, relevant, k) :
    if k <= 0:
        return 0.0

    relevant_set=set(relevant)
    top_k=retrieved [:k]
    score=0.0
    for rank, document in enumerate( top_k,  start=1) :
        if document in relevant_set:
            score += 1 / log2(rank + 1)
    return score


def ndcg_at_k(retrieved , relevant , k) :
    if k <= 0 or not relevant :
        return 0.0
    actual_dcg= dcg_at_k(
        retrieved,
        relevant,
        k,)
    ideal_result_count=min(
        len(set(relevant)),
        k,)

    ideal_retrieved=list(set(relevant))[:ideal_result_count]
    ideal_dcg=dcg_at_k(
        ideal_retrieved,
        relevant,
        k,)

    if ideal_dcg == 0:
        return 0.0
    return actual_dcg / ideal_dcg