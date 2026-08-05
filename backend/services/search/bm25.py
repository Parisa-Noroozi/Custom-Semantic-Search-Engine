import math
from backend.services.query.tokenizer import tokenize

k = 1.5
b = 0.75

def avg_doc_length(docs):
    lengths = [len(tokenize(d)) for d in docs]
    return sum(lengths) / len(lengths)


def idf(word, docs):
    df = 0
    for doc in docs:
        if word in tokenize(doc):
            df += 1
    return math.log((len(docs) - df + 0.5) / (df + 0.5) + 1)


def bm25(word, doc, docs, doc_len, avg_len):
    words = tokenize(doc)
    tf = words.count(word)
    
    if tf == 0:
        return 0
    idf_score = idf(word, docs)
    numerator = tf * (k + 1)
    denominator = tf + k * (1 - b + b * (doc_len / avg_len))
    score =idf_score * (numerator / denominator)
   
    return score