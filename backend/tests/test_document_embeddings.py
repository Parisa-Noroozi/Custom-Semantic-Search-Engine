from backend.services.embeddings.document_embeddings import DocumentEmbeddings



def test_document_embeddings_caches_all_documents():
    documents=[
        "Python programming tutorial",
        "Machine learning course",
    ]
    
    embeddings = DocumentEmbeddings(documents)
    assert set(embeddings.cache) == set(documents)


def test_document_embeddings_returns_cached_vector ():
    documents=[
        "Python programming tutorial",
    ]
    embeddings=DocumentEmbeddings(documents)
    assert embeddings.get(documents[0]) == (
        embeddings.cache[documents[0]]
    )


def test_document_embeddings_returns_none_for_unknown_document() :
    embeddings= DocumentEmbeddings(
        ["Python programming tutorial"],
    )
    
    assert embeddings.get("Unknown document") is None