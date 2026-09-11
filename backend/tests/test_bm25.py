from backend.services.search.bm25 import term_frequency, idf, bm25


def test_term_frequency_counts_single_word():
    tokens = ["python", "python", "tutorial"]
    assert term_frequency("python", tokens) == 2



def test_term_frequency_counts_multiword_phrase():
    tokens = ["machine", "learning", "machine", "learning"]
    assert term_frequency("machine learning", tokens) == 2




def test_term_frequency_requires_exact_phrase_order():
    tokens = ["learning", "machine"]
    assert term_frequency("machine learning", tokens) == 0


def test_idf_is_higher_for_rarer_term():
    documents = [
        ["python", "tutorial"],
        ["python", "guide"],
        ["machine", "learning"],
    ]
    python_idf = idf("python", documents)
    machine_idf = idf("machine", documents)
    assert machine_idf > python_idf

def test_bm25_returns_zero_when_term_is_missing():
    score = bm25(
        term="python",
        document_tokens=["java", "tutorial"],
        doc_len=2,
        avg_len=2,
        idf_score=1.0,
    )
    assert score == 0


def test_bm25_returns_positive_score_for_match():
    score = bm25(
        term="python",
        document_tokens=["python", "tutorial"],
        doc_len=2,
        avg_len=2,
        idf_score=1.0,
    )
    assert score > 0