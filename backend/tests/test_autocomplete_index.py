from backend.services.query.autocomplete import autocomplete
from backend.services.search.index import build_index




def test_build_index_creates_prefixes ():
    index= build_index(
        ["Python programming"],
    )
    assert "p" in index
    assert "py" in index
    assert "pyt" in index
    assert "python" in index




def test_build_index_maps_prefix_to_word():
    index=build_index (
        ["Python programming"],
)
    assert "python" in index["py"]


def test_build_index_avoids_duplicate_words() :
    index=build_index(
        [
            "Python tutorial",
            "Python course",
        ],
    )
    assert index["py"] == {"python"}


def test_autocomplete_returns_sorted_matches() :
    index={
        "py": {
            "pytest",
            "python",
            "pytorch",
        },
    }
    results = autocomplete(
        "py",
        index,
    )
    assert results == [
        "pytest",
        "python",
        "pytorch",
    ]



def test_autocomplete_is_case_insensitive ():
    index={
        "py": {
            "python",
        },
    }
    results = autocomplete (
        "PY",
        index,
    )
    assert results == ["python"]


def test_autocomplete_returns_empty_list_for_unknown_prefix():
    index={
        "py": {
            "python",
        },
    }
    results = autocomplete (
        "java",
        index,
    )
    assert results == []