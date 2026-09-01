from backend.services.query.tokenizer import tokenize
from backend.services.intent_detector import IntentDetector
from backend.services.search.search import search
from backend.services.query_expander import QueryExpander
from backend.services.ranking_strategy import RankingStrategy
from backend.services.search.semantic_ranker import SemanticRanker
from backend.services.search.ranking_engine import RankingEngine
from backend.services.embeddings.document_embeddings import DocumentEmbeddings
from backend.services.embeddings.knowledge_base import KNOWLEDGE_BASE
class SearchEngine:
    
    def __init__(self,documents,index,frequency_table):
        self.documents=documents
        self.index=index
        self.frequency_table=frequency_table
        self.intent_detector = IntentDetector()
        self.query_expander= QueryExpander()
        self.ranking_strategy = RankingStrategy()
        self.semantic_ranker = SemanticRanker()
        self.document_embedding=DocumentEmbeddings(self.documents)
        self.ranker = RankingEngine()
        self.search_function=search
        
        self.intent_keywords = {
    "Learning": {
        "learn",
        "learning",
        "tutorial",
        "course",
        "guide",
        "education"
    },

    "PDF": {
        "pdf",
        "ebook",
        "book",
        "document"
    }
}
        
    def apply_intent_bonus(self, score, document, intents):
        document_tokens = set(tokenize(document))
        bonus = 0
        for intent, percentage in intents:
            keywords = self.intent_keywords.get(intent, set())
            if document_tokens.intersection(keywords):
                bonus += percentage / 100
        return score + bonus


    @staticmethod
    def contains_term(document_tokens, term):
        term_tokens = term.split()

        if len(term_tokens) == 1:
            return term in document_tokens

        term_length = len(term_tokens)

        for i in range(len(document_tokens) - term_length + 1):
            if document_tokens[i:i + term_length] == term_tokens:
                return True

        return False
    
        
    def search(self,query):
        tokens = tokenize(query.original_query)
        query.set_tokens(tokens)
        intents = self.intent_detector.detect_intent(tokens)
        query.set_intents(intents)

        expanded_tokens, expansion_reason, expansion_weights = self.query_expander.expand_query(tokens)

        query.set_expanded_tokens(expanded_tokens)
        query.set_expansion_reason(expansion_reason)
        query.set_expansion_weights(expansion_weights)
        
                
        weights = self.ranking_strategy.get_weights(
                query.intents,
                query.tokens
            )
        
        print("ranking strategy:",weights)
        
        query_vector = self.semantic_ranker.get_query_vector(query.expanded_tokens)
        
        results=self.search_function(query.expanded_tokens, self.documents,self.index, )
        

        new_results = []
        for score, document in results:
            document_tokens = tokenize(document)
            document_token_set = set(document_tokens)
            document_concepts = []
            document_vector = self.document_embedding.get(document)

            for token in document_tokens:
                normalized_token = (
                    self.semantic_ranker.embedding_engine.normalize_token(token)
                )

                if normalized_token in self.semantic_ranker.embedding_engine.knowledge:
                    document_concepts.append(normalized_token)

            semantic_score = self.semantic_ranker.semantic_score_from_vector(
                query_vector,
                document_vector,
            )

            intent_score = self.apply_intent_bonus(
                score,
                document,
                query.intents
            )
            intent_bonus = intent_score - score

            exact_bonus = 0

            for token in query.tokens:
                if token in document_token_set:
                    exact_bonus += 2
                    
                    

            expansion_bonus = 0
            for token in query.expanded_tokens:
                if token in query.tokens:
                    continue

                if self.contains_term(document_tokens, token):
                    expansion_bonus += query.expansion_weights.get(token, 0)
                    
                
                
            query_concepts = self.semantic_ranker.embedding_engine.extract_concepts(  query.expanded_tokens )
            relation_bonus = self.ranker.relation_bonus(query_concepts,document_token_set,KNOWLEDGE_BASE)
                
            category_bonus = self.semantic_ranker.category_similarity(   query_concepts,  document_concepts   )
            final_score = self.ranker.calculate_score(
                                bm25_score=score,
                                semantic_score=semantic_score,
                                expansion_bonus=expansion_bonus,
                                intent_bonus=intent_bonus,
                                exact_bonus=exact_bonus,
                                relation_bonus=relation_bonus,
                                category_bonus=category_bonus,
                                weights=weights,
                            )

            mached_intents =[]
            for intent, percentage in query.intents:
                    keywords = self.intent_keywords.get(intent, set())
                    if document_token_set.intersection(keywords):
                        mached_intents.append(intent)
                        
                        
            
            reason = []
            document_token_set = set(tokenize(document))
            if relation_bonus > 0:
                reason.append(f"Relation Bonus: +{round(relation_bonus,2)}")

            if category_bonus > 0:
                reason.append(f"Category Bonus: +{round(category_bonus,2)}")
                                        
                    
            for token in query.tokens:
                        if token in document_tokens:
                            reason.append(f"Contains keyword: {token}")

            for intent in mached_intents:
                        reason.append(f"Matched Intent: {intent}")

            reason.append(f"BM25 Score: {round(score,2)}")
            reason.append(f"Intent Bonus: +{round(intent_bonus,2)}")
            reason.append(f"Expansion Bonus: +{round(expansion_bonus,2)}")
            reason.append(f"Exact Match Bonus: +{round(exact_bonus,2)}")
            reason.append(f"Semantic Score: {round(semantic_score,3)}")
                
                
            new_results.append({
                        "text": document,
                        "bm25_score": round(score, 2),

                        "intent_bonus": round(intent_bonus, 2),
                        
                        "expansion_bonus": round(expansion_bonus, 2),

                        "final_score": round(final_score, 2),
                        "bm25_weight": weights["bm25"],
                        "intent_weight": weights["intent"],
                        "expansion_weight": weights["expansion"],
                        "semantic_score": round(semantic_score,3),
                        "semantic_weight": weights["semantic"],
                        "ranking_reason": weights["reason"],
                        "matched_intents": mached_intents,
                        "reason":reason,
                        "exact_bonus": round(exact_bonus, 2),
                        "relation_bonus": round(relation_bonus, 2),
                        "category_bonus": round(category_bonus, 2),
                        "query_concepts": query_concepts,
                        
                    })
 
                
        new_results.sort( key=lambda item: item["final_score"],  reverse=True)
        new_results = new_results[:5]
            
        print("\n========== FINAL RESULTS ==========")
        for result in new_results:
                print(result)
        results = new_results

        return query  , results
    
    
    

        