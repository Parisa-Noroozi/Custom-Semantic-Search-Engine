from backend.services.query.query_expander import QueryExpander


expander = QueryExpander()


def test_expand_query_keeps_original_token():
    expanded_tokens, _, weights = expander.expand_query(["python"])
    assert "python" in expanded_tokens
    assert weights["python"] == 1.0

def test_expand_query_adds_dictionary_expansions():
    expanded_tokens, _, _ = expander.expand_query(["python"])
    assert "programming" in expanded_tokens
    assert "coding" in expanded_tokens
    assert "script" in expanded_tokens


def test_expand_query_assigns_expansion_weights():
    _, _, weights = expander.expand_query(["python"])
    assert weights["programming"] == 0.40
    assert weights["coding"] == 0.25
    assert weights["script"] == 0.15


def test_expand_query_records_expansion_reason():
    _, reasons, _ = expander.expand_query(["python"])
    assert "python" in reasons
    assert "programming" in reasons["python"]
    assert "coding" in reasons["python"]
    assert "script" in reasons["python"]



def test_expand_query_keeps_unknown_token():
    expanded_tokens, reasons, weights = expander.expand_query(["unknownterm"])
    assert "unknownterm" in expanded_tokens
    assert weights["unknownterm"] == 1.0
    assert reasons == {}




def test_expand_query_removes_duplicate_tokens():
    expanded_tokens, _, _ = expander.expand_query(["python", "python"])
    assert len(expanded_tokens) == len(set(expanded_tokens))