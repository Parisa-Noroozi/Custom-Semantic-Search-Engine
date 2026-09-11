from backend.services.search.search_retriever import SearchRetriever


def test_retriever_returns_search_results():
    documents = [
        "Python tutorial",
        "Java tutorial",
    ]

    retriever = SearchRetriever(documents)
    results = retriever.retrieve(["python"])
    assert len(results) == 2
    assert results[0][1] == "Python tutorial"


def test_retriever_uses_its_documents():
    documents = [
        "Machine learning guide",
        "Python tutorial",
    ]
    retriever = SearchRetriever(documents)
    results = retriever.retrieve(["machine"])
    returned_documents = [document for _, document in results]
    assert returned_documents == [
        "Machine learning guide",
        "Python tutorial",
    ]