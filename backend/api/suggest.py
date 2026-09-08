from fastapi import APIRouter
from backend.dependencies import get_suggestions


router = APIRouter()


@router.get("/suggest")
def suggest(q: str):
    return get_suggestions(q)