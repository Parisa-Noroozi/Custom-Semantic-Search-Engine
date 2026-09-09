from backend.models.query import Query
from backend.services.query.query_processor import QueryProcessor



processor = QueryProcessor()


def test_query_processor_tokenizes_original_query():
    query = Query("Python PDF")
    processed_query, _ = processor.process(query)
    assert processed_query.tokens == ["python", "pdf"]
    
    
    
def test_query_processor_keeps_original_query():
    query = Query("Python PDF")
    processed_query, _ = processor.process(query)
    assert processed_query.original_query == "Python PDF"
    
    
def test_query_processor_expands_python_query():
    query = Query("python")
    processed_query, _ = processor.process(query)
    assert "python" in processed_query.expanded_tokens
    assert len(processed_query.expanded_tokens) > len(processed_query.tokens)
    
    
def test_query_processor_detects_pdf_intent():
    query = Query("python pdf")
    processed_query, _ = processor.process(query)
    intent_names = [intent[0] for intent in processed_query.intents]
    assert "PDF" in intent_names
    
    
    

def test_query_processor_returns_ranking_weights():
    query = Query("python")
    _, weights = processor.process(query)
    assert "bm25" in weights
    assert "semantic" in weights
    assert "expansion" in weights
    assert "intent" in weights
    assert "reason" in weights




