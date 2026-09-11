from backend.services.search.ranking_engine import RankingEngine


engine = RankingEngine()


def test_calculate_score_uses_default_weights():
    score = engine.calculate_score(
        bm25_score=2.0,
        semantic_score=0.5,
        expansion_bonus=1.0,
        intent_bonus=1.0,
    )

    expected = (
        2.0 * 0.6
        + 0.5 * 1.5
        + 1.0 * 0.2
        + 1.0 * 0.1
    )
    assert score == expected


def test_calculate_score_uses_custom_weights():
    weights = {
        "bm25": 1.0,
        "semantic": 2.0,
        "expansion": 0.5,
        "intent": 0.25,
    }

    score = engine.calculate_score(
        bm25_score=2.0,
        semantic_score=0.5,
        expansion_bonus=1.0,
        intent_bonus=2.0,
        weights=weights,
    )

    expected = (
        2.0 * 1.0
        + 0.5 * 2.0
        + 1.0 * 0.5
        + 2.0 * 0.25
    )
    assert score == expected



def test_calculate_score_adds_all_direct_bonuses():
    score = engine.calculate_score(
        bm25_score=0,
        semantic_score=0,
        expansion_bonus=0,
        intent_bonus=0,
        exact_bonus=0.5,
        relation_bonus=0.25,
        category_bonus=0.75,
    )
    assert score == 1.5


def test_relation_bonus_returns_zero_for_unknown_concept():
    knowledge = {
        "python": {
            "relations": ["programming language"]
        }
    }


    bonus = engine.relation_bonus(
        query_concepts=["unknown"],
        document_tokens=["programming", "language"],
        knowledge=knowledge,
    )
    assert bonus == 0




def test_relation_bonus_matches_multiword_relation():
    knowledge = {
        "python": {
            "relations": ["programming language"]
        }
    }

    bonus = engine.relation_bonus(
        query_concepts=["python"],
        document_tokens=["python", "programming", "language"],
        knowledge=knowledge,
    )
    assert bonus == 0.25


def test_relation_bonus_requires_all_relation_tokens():
    knowledge = {
        "python": {
            "relations": ["programming language"]
        }
    }


    bonus = engine.relation_bonus(
        query_concepts=["python"],
        document_tokens=["python", "programming"],
        knowledge=knowledge,
    )
    assert bonus == 0