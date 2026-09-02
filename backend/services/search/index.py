from backend.services.query.tokenizer import tokenize

def build_index(documents):
    index = {}
    document_frequency = {}

    for doc in documents:
        words = tokenize(doc)
        unique_words = set(words)
        for word in words:
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                if prefix not in index:
                    index[prefix] = set()
                index[prefix].add(word)
        for word in unique_words:
            document_frequency.setdefault(word, 0)
            document_frequency[word] += 1
    return index, document_frequency