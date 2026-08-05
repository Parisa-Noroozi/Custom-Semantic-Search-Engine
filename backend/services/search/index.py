from backend.services.query.tokenizer import tokenize

def build_index(documents):
    index = {}
    frequency_table = {}
    document_frequency = {}

    for doc in documents:
        words = tokenize(doc)
        unique_words = set(words)
        for word in words:
            frequency_table.setdefault(word, 0)
            frequency_table[word] += 1
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                if prefix not in index:
                    index[prefix] = set()
                index[prefix].add(word)
        for word in unique_words:
            document_frequency.setdefault(word, 0)
            document_frequency[word] += 1
    return index, frequency_table, document_frequency