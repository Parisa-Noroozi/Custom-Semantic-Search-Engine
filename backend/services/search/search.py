from backend.services.query.tokenizer import tokenize
from backend.services.query.spell_corrector import correct_word
from backend.services.search.bm25 import bm25
from backend.services.intent_detector import IntentDetector

def search(tokens, documents, index, ):
    results=[]
      
    for i, doc in enumerate(documents):
        score = 0
        doc_len = len(tokenize(doc))
        avg_len = sum(len(tokenize(d)) for d in documents) / len(documents)

        print(f"\nDocument: {doc}")

        for w in tokens:
            s = bm25(w, doc, documents, doc_len, avg_len)
            print(f"{w} -> {s}")
            score += bm25(w, doc, documents, doc_len, avg_len)
        if score > 0:
            results.append((score, doc))
    results.sort(reverse=True)
    return results[:5]