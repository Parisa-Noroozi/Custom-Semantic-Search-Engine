from backend.data.documents import DOCUMENTS
from backend.evaluation.dataset import EVALUATION_DATASET


def test_evaluation_dataset_is_not_empty():
    assert len(EVALUATION_DATASET) > 0



def test_each_evaluation_case_has_query():
    for case in EVALUATION_DATASET:
        assert case["query"]



def test_each_evaluation_case_has_relevant_documents():
    for case in EVALUATION_DATASET:
        assert len(case["relevant_documents"]) > 0



def test_all_relevant_documents_exist_in_search_dataset():
    for case in EVALUATION_DATASET:
        for document in case["relevant_documents"]:
            assert document in DOCUMENTS





def test_evaluation_queries_are_unique():
    queries=[
        case["query"]
        for case in EVALUATION_DATASET
    ]
    assert len(queries) == len(set(queries))