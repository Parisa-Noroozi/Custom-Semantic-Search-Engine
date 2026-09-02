from backend.services.embeddings.knowledge_base import (
    TOPIC_SPACE,
    KNOWLEDGE_BASE
)
from backend.services.query.tokenizer import tokenize




class EmbeddingEngine:

    def __init__(self):
        self.knowledge = KNOWLEDGE_BASE
        self.topic_space = TOPIC_SPACE
        
        
    def normalize_token(self, token):
        token = token.lower()

        if token in self.knowledge:
            return token

        for concept, info in self.knowledge.items():
            aliases = info.get("aliases", [])
            if token in aliases:
                return concept
        return token
        
        
    def get_vector(self, concept):
        concept = concept.lower()
        print("Searching:", concept)
        if concept not in self.knowledge:
            print("NOT FOUND:", concept)
            return None

        topics = self.knowledge[concept]["topics"]

        vector = []

        for topic in self.topic_space:

            vector.append(
                topics.get(topic, 0)
            )
            
    
        print("Found:", concept, vector)
        
        return vector
    
    
    
    def average_vectors(self, tokens):
        vectors = []
        for token in tokens:
            token = self.normalize_token(token)
            vector = self.get_vector(token)
            if vector is not None:
                vectors.append(vector)
        if not vectors:
            return None

        dimensions = len(vectors[0])

        average_vector = []

        for i in range(dimensions):
            value = sum(vector[i] for vector in vectors)
            average_vector.append(
                value / len(vectors)
            )
        return average_vector


    def get_query_vector(self, tokens):
        concepts = self.extract_concepts(tokens)
        return self.average_vectors(concepts)
    
    
    def get_document_vector(self, document):
        tokens = tokenize(document)
        return self.average_vectors(tokens)
    
    
    def extract_concepts(self, tokens):
        concepts = []
        for token in tokens:
            normalized_token = self.normalize_token(token)
            if ( normalized_token in self.knowledge and normalized_token not in concepts):
                concepts.append(normalized_token)
        return concepts
    

