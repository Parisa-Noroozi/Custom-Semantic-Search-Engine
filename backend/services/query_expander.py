from backend.services.embeddings.embedding_engine import EmbeddingEngine
from backend.services.embeddings.knowledge_base import KNOWLEDGE_BASE
class QueryExpander:

    def __init__(self):
        self.expansion_dictionary = {

    "python": {

        "programming": 0.40,
        "coding": 0.25,
        "script": 0.15

    },

    "tutorial": {

        "guide": 0.50,
        "course": 0.35,
        "learning": 0.25

    },

    "pdf": {

        "ebook": 0.40,
        "document": 0.30

    },

    "ai": {

        "artificial": 0.30,
        "intelligence": 0.30,
        "machine": 0.20,
        "learning": 0.20

    }
}
        self.embedding_engine = EmbeddingEngine()
        self.knowledge = KNOWLEDGE_BASE
        
        
    def expand_query(self, tokens):
        expanded_tokens = list(tokens)
        expansion_reason = {}
        expansion_weights = {}
        for token in tokens:
            expansion_weights[token] = 1.0

        for token in tokens:
            if token in self.knowledge:
                relations = self.knowledge[token].get("relations", [])

                for relation in relations:
                    if relation not in expanded_tokens:
                        expanded_tokens.append(relation)
                        expansion_weights[relation] = 0.10
                        expansion_reason.setdefault(token, []).append(relation)
            normalized = self.embedding_engine.normalize_token(token)

            if normalized != token:
                expanded_tokens.append(normalized)
            token = normalized

            if token in self.expansion_dictionary:
                expansion_reason[token] = []
                for word, weight in self.expansion_dictionary[token].items():
                    expanded_tokens.append(word)
                    expansion_weights[word] = weight
                    expansion_reason[token].append(word)
                    
                    
        expanded_tokens = list(dict.fromkeys(expanded_tokens))
        print(expanded_tokens)
        print(expansion_weights)

        return expanded_tokens, expansion_reason,expansion_weights