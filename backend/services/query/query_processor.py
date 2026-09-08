from backend.services.query.tokenizer import tokenize
from backend.services.intent_detector import IntentDetector
from backend.services.query_expander import QueryExpander
from backend.services.ranking_strategy import RankingStrategy


class QueryProcessor:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.query_expander = QueryExpander()
        self.ranking_strategy = RankingStrategy()

    def process(self, query):
        tokens = tokenize(query.original_query)
        query.set_tokens(tokens)

        intents = self.intent_detector.detect_intent(tokens)
        query.set_intents(intents)

        expanded_tokens, expansion_reason, expansion_weights = (
            self.query_expander.expand_query(tokens)
        )

        query.set_expanded_tokens(expanded_tokens)
        query.set_expansion_reason(expansion_reason)
        query.set_expansion_weights(expansion_weights)

        weights = self.ranking_strategy.get_weights(
            query.intents,
            query.tokens
        )

        return query, weights