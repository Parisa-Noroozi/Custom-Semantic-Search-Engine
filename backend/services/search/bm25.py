import math
from backend.services.query.tokenizer import tokenize

k = 1.5
b = 0.75


def term_frequency(term, text):
    words = tokenize(text)
    term_tokens = term.split()

    if len(term_tokens) == 1:
        return words.count(term)

    count = 0
    term_length = len(term_tokens)

    for i in range(len(words) - term_length + 1):
        if words[i:i + term_length] == term_tokens:
            count += 1

    return count

def avg_doc_length(docs):
    lengths = [len(tokenize(d)) for d in docs]
    return sum(lengths) / len(lengths)


def idf(word, docs):
    df = 0
    for doc in docs:
         if term_frequency(word, doc) > 0:
            df += 1
    return math.log((len(docs) - df + 0.5) / (df + 0.5) + 1)


def bm25(word, doc, docs, doc_len, avg_len):
    tf = term_frequency(word, doc)
    
    if tf == 0:
        return 0
    idf_score = idf(word, docs)
    numerator = tf * (k + 1)
    denominator = tf + k * (1 - b + b * (doc_len / avg_len))
    score =idf_score * (numerator / denominator)
   
    return score