from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api.health import router as health_router
from backend.api.search import router as search_router
from backend.api.suggest import router as suggest_router
from backend.core.config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_HEADERS,
    CORS_ALLOW_METHODS,
    CORS_ORIGINS,
)

BASE_DIR=Path(__file__).resolve().parent.parent
FRONTEND_DIR=BASE_DIR / "frontend"


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(
        FRONTEND_DIR / "index.html"
)

app.include_router(search_router)
app.include_router(suggest_router)
app.include_router(health_router)