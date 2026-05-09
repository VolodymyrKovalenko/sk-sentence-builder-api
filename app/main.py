from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.words import router as words_router
from app.api.routers.auth import router as auth_router

app = FastAPI(
    title="[SK] Practice API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5180",
        "http://localhost:5180",
        "http://192.168.100.23:5180"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(words_router)
app.include_router(auth_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "[SK] Practice API running"}