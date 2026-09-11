from backend.services.query.ranking_strategy import RankingStrategy


strategy = RankingStrategy()


def test_get_weights_returns_default_strategy():
    weights = strategy.get_weights([], ["python"])
    assert weights["bm25"] == 0.6
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 0.1
    assert weights["expansion"] == 0.2
    assert weights["reason"] == "Default strategy"




def test_learning_intent_applies_learning_profile():
    weights = strategy.get_weights(
        [("Learning", 50)],
        ["learn", "python"],
    )
    assert weights["bm25"] == 1.0
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 1.6
    assert weights["expansion"] == 1.3
    assert weights["reason"] == "Learning query detected"



def test_pdf_intent_applies_pdf_profile():
    weights = strategy.get_weights(
        [("PDF", 50)],
        ["python", "pdf"],
    )
    assert weights["bm25"] == 1.0
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 2.0
    assert weights["expansion"] == 1.1
    assert weights["reason"] == "PDF query detected"




def test_multiple_intents_merge_using_highest_values():
    weights = strategy.get_weights(
        [("Learning", 50), ("PDF", 50)],
        ["learn", "pdf"],
    )
    assert weights["bm25"] == 1.0
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 2.0
    assert weights["expansion"] == 1.3



def test_long_query_applies_long_query_profile():
    weights = strategy.get_weights(
        [],
        ["python", "machine", "learning", "tutorial"],
    )
    assert weights["bm25"] == 1.5
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 0.8
    assert weights["expansion"] == 1.2
    assert weights["reason"] == "Long technical query"




def test_intent_and_long_query_profiles_are_combined():
    weights = strategy.get_weights(
        [("PDF", 25)],
        ["python", "pdf", "machine", "learning"],
    )
    assert weights["bm25"] == 1.5
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 2.0
    assert weights["expansion"] == 1.2
    assert weights["reason"] == "PDF query detected + Long technical query"

def test_unknown_intent_keeps_default_strategy():
    weights = strategy.get_weights(
        [("Unknown", 100)],
        ["python"],
    )
    assert weights["bm25"] == 0.6
    assert weights["semantic"] == 1.5
    assert weights["intent"] == 0.1
    assert weights["expansion"] == 0.2
    assert weights["reason"] == "Default strategy"