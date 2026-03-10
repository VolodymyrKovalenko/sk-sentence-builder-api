from fastapi import APIRouter
from app.data.mock_words import mock_words
from app.schemas.word import WordOut
from app.utils.random import get_daily_random_ids

router = APIRouter(prefix="/words", tags=["words"])


@router.get("/", response_model=list[WordOut])
def list_words() -> list[WordOut]:
    return mock_words

@router.get("/daily/")
def get_daily_words():
    ids = [word.id for word in mock_words]

    selected_ids = get_daily_random_ids(ids)

    return [word for word in mock_words if word.id in selected_ids]