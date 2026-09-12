from fastapi import APIRouter, Query
from backend.dependencies import get_suggestions


router = APIRouter()


@router.get("/suggest")
def suggest( q: str = Query(min_length=1),):
    return get_suggestions(q)