def precision_at_k(retrieved, relevant , k):
    if k <= 0:
        return 0.0
    
    top_k=retrieved[:k]
    
    if not top_k:
        return 0.0
    
    relevant_set=set(relevant)
    
    maches=sum(
        1
        for document in top_k
        if document in relevant_set
    )
    return maches / len(top_k)

def recall_at_k(retrieved, relevant ,k ):
    if k <= 0 or not relevant:
        return 0.0
    
    top_k=retrieved[:k]
    relevant_set=set(relevant)
    
    matches=sum(
        1
        for document in top_k
        if document in relevant_set
    )
    return matches / len(relevant_set)


def reciprocal_rank(retrieved, relevant):
    relevant_set=set(relevant)
    for rank, document in enumerate(retrieved, start=1):
        if document in relevant_set:
            return 1 / rank

    return 0.0