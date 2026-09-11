from backend.services.search.search import search


def test_search_returns_all_documents():
    documents = [
        "Python tutorial",
        "Java tutorial",
        "Machine learning guide",
    ]
    results = search(["python"], documents)
    assert len(results) == len(documents)


def test_search_ranks_matching_document_first():
    documents = [
        "Java tutorial",
        "Python programming tutorial",
        "Machine learning guide",
    ]

    results = search(["python"], documents)
    assert results[0][1] == "Python programming tutorial"


def test_search_gives_non_matching_document_zero_score():
    documents = [
        "Python tutorial",
        "Java tutorial",
    ]
    results = search(["python"], documents)
    java_result = next(
        result for result in results
        if result[1] == "Java tutorial"
    )
    assert java_result[0] == 0


def test_search_supports_multiple_query_terms():
    documents = [
        "Python programming tutorial",
        "Python guide",
        "Java programming",
    ]
    results = search(["python", "programming"], documents)
    assert results[0][1] == "Python programming tutorial"