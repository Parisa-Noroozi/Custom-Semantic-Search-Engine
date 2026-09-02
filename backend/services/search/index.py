from backend.services.query.tokenizer import tokenize

def build_index(documents):
    index = {}

    for doc in documents:
        words = tokenize(doc)
        for word in words:
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                if prefix not in index:
                    index[prefix] = set()
                index[prefix].add(word)

    return index