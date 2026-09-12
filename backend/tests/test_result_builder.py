from backend.models.query import Query
from backend.services.search.result_builder import ResultBuilder

def create_builder() :
    intent_keywords = {
        "Learning": {
            "learn",
            "tutorial",
            "course",
        },
        "PDF": {
            "pdf",
            "ebook",
            "book",
        },
    }
    return ResultBuilder(intent_keywords)


def test_get_matched_intents_returns_matching_intent():
    builder=create_builder()

    matched=builder.get_matched_intents(
        {"python", "tutorial"},
        [
            ("Learning", 1.0),
            ("PDF", 0.5),
        ],
    )
    assert matched == ["Learning"]


def test_get_matched_intents_returns_empty_list_without_match():
    builder=create_builder()

    matched=builder.get_matched_intents(
        {"python", "programming"},
        [
            ("Learning", 1.0),
            ("PDF", 0.5),
        ],
    )
    assert matched == []


def test_build_reason_includes_keyword_match():
    builder=create_builder()
    query=Query("python")
    query.tokens = ["python"]
    reason=builder.build_reason(
        query=query,
        document_tokens=["python", "tutorial"],
        matched_intents=[],
        score=1.2,
        semantic_score=0.5,
        intent_bonus=0,
        expansion_bonus=0,
        exact_bonus=0,
        relation_bonus=0,
        category_bonus=0,
    )
    assert "Contains keyword: python" in reason

def test_build_reason_includes_positive_bonuses() :
    builder= create_builder ()
    query= Query("python")
    query.tokens =["python"]
    reason=builder.build_reason(
        query=query,
        document_tokens=["python"],
        matched_intents=["Learning"],
        score=1.0,
        semantic_score=0.4,
        intent_bonus=0.1,
        expansion_bonus=0.2,
        exact_bonus=0.3,
        relation_bonus=0.15,
        category_bonus=0.15,
    )
    assert "Relation Bonus: +0.15" in reason
    assert "Category Bonus: +0.15" in reason
    assert "Matched Intent: Learning" in reason
    
    
    

def test_build_result_returns_expected_fields():
    builder=create_builder()

    query=Query("python")
    query.tokens=["python"]
    query.intents=[
        ("Learning", 1.0),
    ]

    weights={
        "bm25": 0.6,
        "semantic": 1.5,
        "intent": 0.1,
        "expansion": 0.2,
        "reason": "default",
    }
    score_data= {
        "document_tokens": ["python", "tutorial"],
        "document_token_set": {"python", "tutorial"},
        "semantic_score": 0.4567,
        "intent_bonus": 0.1,
        "expansion_bonus": 0.2,
        "exact_bonus": 0.3,
        "relation_bonus": 0.15,
        "category_bonus": 0.15,
        "final_score": 2.345,
        "query_concepts": ["python"],
    }
    result=builder.build_result(
        document="Python tutorial",
        score=1.234,
        weights=weights,
        score_data=score_data,
        query=query,
    )
    assert result["text"] == "Python tutorial"
    assert result["bm25_score"] == 1.23
    assert result["semantic_score"] == 0.457
    assert result["final_score"] == 2.35
    assert result["matched_intents"] == ["Learning"]
    assert result["query_concepts"] == ["python"]