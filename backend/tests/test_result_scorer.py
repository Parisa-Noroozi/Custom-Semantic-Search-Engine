from backend.services.search.result_scorer import ResultScorer

INTENT_KEYWORDS = {
    "Learning": {
        "learn",
        "learning",
        "tutorial",
        "course",
        "guide",
        "education",
    },
    "PDF": {
        "pdf",
        "ebook",
        "book",
        "document",
    },
}

scorer = ResultScorer(
    semantic_ranker=None,
    document_embedding=None,
    intent_keywords=INTENT_KEYWORDS,
)

def test_contains_term_finds_single_word():
    tokens= ["python", "programming", "tutorial"]
    assert scorer.contains_term(tokens, "python") is True


def test_contains_term_returns_false_for_missing_word():
    tokens= ["python", "programming", "tutorial"]
    assert scorer.contains_term(tokens, "java") is False


def test_contains_term_finds_multiword_phrase():
    tokens= ["machine", "learning", "tutorial"]
    assert scorer.contains_term(tokens, "machine learning") is True


def test_contains_term_requires_phrase_order():
    tokens= ["learning", "machine", "tutorial"]
    assert scorer.contains_term(tokens, "machine learning") is False


def test_apply_intent_bonus_adds_learning_bonus():
    score = scorer.apply_intent_bonus(
        score=2.0,
        document = "Python tutorial",
        intents =[("Learning", 50)],
    )
    assert score == 2.5


def test_apply_intent_bonus_adds_pdf_bonus():
    score = scorer.apply_intent_bonus(
        score=1.0,
        document="Python PDF document",
        intents=[("PDF", 50)],
    )
    assert score ==   1.5




def test_apply_intent_bonus_does_not_change_unrelated_document():
    score= scorer.apply_intent_bonus(
        score= 2.0,
        document="Python programming",
        intents= [("PDF", 50)],
    )
    assert score  == 2.0