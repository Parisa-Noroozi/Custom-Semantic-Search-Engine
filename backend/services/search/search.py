from backend.services.query.tokenizer import tokenize
from backend.services.search.bm25 import bm25, idf
from backend.services.intent_detector import IntentDetector

def search(tokens, documents ):
    results=[]
    
    tokenized_documents = [ tokenize(document) for document in documents]

    avg_len = sum( len(document_tokens) for document_tokens in tokenized_documents ) / len(tokenized_documents)

    idf_scores = { token: idf(token, tokenized_documents)for token in tokens }
      
    for doc, document_tokens in zip( documents, tokenized_documents, ):
        score = 0
        doc_len = len(document_tokens)
       

        print(f"\nDocument: {doc}")

        for w in tokens:
            term_score = bm25(
                w,
                document_tokens,
                doc_len,
                avg_len,
                idf_scores[w],
            )

            print(f"{w} -> {term_score}")
            score += term_score
            
        results.append((score, doc))
    results.sort(reverse=True)
    return results