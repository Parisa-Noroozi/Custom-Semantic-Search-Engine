import uuid
from datetime import datetime


class Query:

    def __init__(self, original_query):

        self.original_query = original_query

        self.query_id = str(uuid.uuid4())

        self.created_at = datetime.now()

        self.tokens = []

        self.intents = []

        self.expanded_tokens = []
        
        self.expansion_reason = {}
        
        self.expansion_weights = {}
       

    def set_tokens(self, tokens):

     self.tokens = tokens
     
     
    def set_intents(self, intents):

      self.intents = intents
      
      
    def set_expanded_tokens(self, expanded_tokens):
      self.expanded_tokens = expanded_tokens

    def get_expanded_tokens(self):
        return self.expanded_tokens
    
    
    def set_expansion_reason(self, reason):

      self.expansion_reason = reason


    def get_expansion_reason(self):

        return self.expansion_reason
      
    def set_expansion_weights(self, weights):

      self.expansion_weights = weights