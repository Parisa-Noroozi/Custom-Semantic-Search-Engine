from fastapi.testclient import TestClient
from backend.app import app

client=TestClient(app)


def test_health_endpoint():
    response=client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Smart Search Engine"
    }


def test_search_endpoint_returns_success():
    response=client.get(
        "/search",
        params={"q": "python"},
    )
    assert response.status_code == 200


def test_search_endpoint_returns_expected_structure():
    response=client.get(
        "/search",
        params={"q": "python"},
    )
    data=response.json()
    assert "query" in data
    assert "tokens" in data
    assert "expanded_tokens" in data
    assert "expansion_reason" in data
    assert "intents" in data
    assert "results" in data
    assert "stats" in data



def test_search_endpoint_preserves_query():
    response=client.get(
        "/search",
        params={"q": "Python PDF"},
    )
    data=response.json()
    assert data["query"] == "Python PDF"
    assert data["tokens"] == ["python", "pdf"]


def test_search_endpoint_returns_valid_stats():
    response = client.get(
        "/search",
        params={"q": "python"},
    )
    data=response.json()
    stats=data["stats"]
    assert stats["documents_scanned"] > 0
    assert stats["returned_results"] == len(data["results"])
    assert stats["original_tokens"] == len(data["tokens"])
    assert stats["expanded_tokens"] == len(
        data["expanded_tokens"]
    )
    assert stats["added_terms"] == (
        len(data["expanded_tokens"])
        - len(data["tokens"])
    )


def test_search_endpoint_returns_at_most_five_results():
    response=client.get(
        "/search",
        params={"q": "python"},
    )
    data=response.json()
    assert len(data["results"]) <= 5


def test_search_endpoint_requires_query_parameter():
    response=client.get("/search")

    assert response.status_code == 422
    
    
    
def test_search_endpoint_rejects_empty_query():
    response = client.get(
        "/search",
        params={"q": ""},
    )

    assert response.status_code == 422


def test_suggest_endpoint_returns_success():
    response=client.get(
        "/suggest",
        params={"q": "py"},
    )
    assert response.status_code == 200



def test_suggest_endpoint_returns_json():
    response=client.get(
        "/suggest",
        params={"q": "py"},
    )
    data=response.json()
    assert isinstance(data, list)




def test_suggest_endpoint_requires_query_parameter():
    response=client.get("/suggest")
    assert response.status_code == 422
    
    
    
def test_suggest_endpoint_rejects_empty_query():
    response = client.get(
        "/suggest",
        params={"q": ""},
    )

    assert response.status_code == 422