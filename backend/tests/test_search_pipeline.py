from backend.models.query import Query
from backend.pipelines.search_pipeline import SearchPipeline



def test_pipeline_processes_query():
    documents = [
        "Python programming tutorial",
        "Java programming guide",
    ]
    pipeline = SearchPipeline(documents)
    query = Query("Python")
    processed_query, _ = pipeline.search(query)
    assert processed_query.tokens == ["python"]
    assert len(processed_query.expanded_tokens) > 0


def test_pipeline_returns_matching_results():
    documents= [
        "Python programming tutorial",
        "Java programming guide",
        "Machine learning course",
    ]
    pipeline= SearchPipeline(documents)
    query= Query("python")
    _, results = pipeline.search(query)
    assert len(results) > 0
    assert results[0]["text"] == "Python programming tutorial"


def test_pipeline_sorts_results_by_final_score():
    documents= [
        "Python programming tutorial",
        "Python guide",
        "Java programming",
    ]
    pipeline = SearchPipeline(documents)
    query= Query("python")
    _, results= pipeline.search(query)
    scores = [result["final_score"] for result in results]
    assert scores == sorted(scores, reverse=True)


def test_pipeline_filters_non_positive_results():
    documents = [
        "Python tutorial",
        "Java tutorial",
        "Cooking recipe",
    ]
    pipeline= SearchPipeline(documents)
    query= Query("python")
    _, results =pipeline.search(query)
    assert all(
        result["final_score"] > 0
        for result in results
    )


def test_pipeline_returns_at_most_five_results():
    documents=[
        "Python tutorial one",
        "Python tutorial two",
        "Python tutorial three",
        "Python tutorial four",
        "Python tutorial five",
        "Python tutorial six",
        "Python tutorial seven",
    ]
    pipeline=SearchPipeline(documents)
    query=Query("python")
    _, results=pipeline.search(query)
    assert len(results) <= 5