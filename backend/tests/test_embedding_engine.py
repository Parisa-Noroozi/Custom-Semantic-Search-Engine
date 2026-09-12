from backend.services.embeddings.embedding_engine import EmbeddingEngine


def test_normalize_token_keeps_known_concept():
    engine=EmbeddingEngine()

    concept=next(iter(engine.knowledge))

    assert engine.normalize_token(concept.upper()) == concept


def test_normalize_token_resolves_alias():
    engine=EmbeddingEngine()

    for concept, info in engine.knowledge.items():
        aliases=info.get("aliases", [])

        if aliases:
            alias=aliases[0]
            assert engine.normalize_token(alias) == concept
            return
    raise AssertionError("Knowledge base has no aliases to test")


def test_get_vector_returns_none_for_unknown_concept():
    engine=EmbeddingEngine()

    assert engine.get_vector("unknown-concept") is None


def test_get_vector_matches_topic_space_dimensions():
    engine = EmbeddingEngine()

    concept = next(iter(engine.knowledge))
    vector = engine.get_vector(concept)

    assert len(vector) == len(engine.topic_space)


def test_average_vectors_returns_none_without_known_tokens():
    engine = EmbeddingEngine()

    vector = engine.average_vectors(
        ["unknown-concept"],
    )

    assert vector is None


def test_extract_concepts_removes_duplicates():
    engine = EmbeddingEngine()

    concept = next(iter(engine.knowledge))

    concepts = engine.extract_concepts(
        [concept, concept],
    )

    assert concepts == [concept]