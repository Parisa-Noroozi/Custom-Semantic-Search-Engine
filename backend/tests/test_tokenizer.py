from backend.services.query.tokenizer import tokenize


def test_tokenize_converts_text_to_lowercase():
    tokens = tokenize("Python PDF")
    assert tokens == ["python", "pdf"]

def test_tokenize_removes_punctuation():
    tokens = tokenize("Python, PDF!")
    assert tokens == ["python", "pdf"]


def test_tokenize_removes_stop_words():
    tokens = tokenize("the python tutorial is in the document")
    assert tokens == ["python", "tutorial", "document"]



def test_tokenize_handles_empty_text():
    tokens = tokenize("")
    assert tokens == []