from typing import List

from pydantic import BaseModel


class SearchResultSchema(BaseModel):
    text: str
    bm25_score: float
    intent_bonus: float
    expansion_bonus: float
    final_score: float
    bm25_weight: float
    intent_weight: float
    expansion_weight: float
    semantic_score: float
    semantic_weight: float
    ranking_reason: str
    matched_intents: List[str]
    reason: List[str]
    exact_bonus: float
    relation_bonus: float
    category_bonus: float
    query_concepts: List[str]


class SearchStatsSchema(BaseModel):
    documents_scanned: int
    returned_results: int
    original_tokens: int
    expanded_tokens: int
    added_terms: int


class SearchResponseSchema(BaseModel):
    query: str
    tokens: List[str]
    expanded_tokens: List[str]
    expansion_reason: dict
    intents: list
    results: List[SearchResultSchema]
    stats: SearchStatsSchema