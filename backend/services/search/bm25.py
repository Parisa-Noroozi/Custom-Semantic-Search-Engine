import math

k = 1.5
b = 0.75


def term_frequency(term, document_tokens):
    term_tokens = term.split()
    if len(term_tokens) == 1:
        return document_tokens.count(term)

    count = 0
    term_length = len(term_tokens)

    for i in range(len(document_tokens) - term_length + 1):
        if document_tokens[i:i + term_length] == term_tokens:
            count += 1
    return count


def idf(term, tokenized_documents):
    df = 0
    for document_tokens in tokenized_documents:
        if term_frequency(term, document_tokens) > 0:
            df += 1

    return math.log( ( len(tokenized_documents) - df + 0.5  ) / (  df + 0.5   ) + 1 )


def bm25(
    term,
    document_tokens,
    doc_len,
    avg_len,
    idf_score,
):
    tf = term_frequency(term, document_tokens)
    if tf == 0:
        return 0

    numerator = tf * (k + 1)
    denominator = tf + k * (  1 - b + b * (doc_len / avg_len) )

    return idf_score * (numerator / denominator)