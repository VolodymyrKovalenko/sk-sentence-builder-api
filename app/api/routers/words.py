import re
import random

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.word import WordOut
from app.schemas.sentence import SentenceOut
from app.utils.random import get_daily_random_ids
from app.models.word import Word
from app.models.user import User
from app.models.sentence import Sentence
from app.services.auth.jwt_token import get_current_user, get_optional_current_user
from app.core.config import settings
router = APIRouter(prefix="/words", tags=["words"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalCurrentUser = Annotated[User | None, Depends(get_optional_current_user)]


def _resolve_daily_limit(current_user: User | None) -> int:
    if current_user is None:
        return settings.ANON_DAILY_WORDS
    if bool(getattr(current_user, "is_premium", False)):
        return settings.PREMIUM_DAILY_WORDS
    return settings.FREE_DAILY_WORDS


def _get_daily_selected_word_ids(db: Session, current_user: User | None) -> set[int]:
    ids = db.scalars(select(Word.id)).all()
    daily_limit = _resolve_daily_limit(current_user)
    return set(get_daily_random_ids(ids, count=daily_limit))


@router.get("/", response_model=list[WordOut])
def get_all_words(db: DbSession, current_user: CurrentUser) -> list[WordOut]:
    return db.scalars(select(Word)).all()


@router.get("/{word_id}/sentences/", response_model=list[SentenceOut])
def get_word_sentences(word_id: int, db: DbSession, current_user: OptionalCurrentUser) -> list[SentenceOut]:
    selected_ids = _get_daily_selected_word_ids(db, current_user)

    if word_id not in selected_ids:
        raise HTTPException(status_code=403, detail="Word sentence is unavailable")

    word = db.get(Word, word_id)
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    sentences = db.scalars(
        select(Sentence).where(Sentence.word_id == word_id)
    ).all()

    data: list[SentenceOut] = []

    for sentence in sentences:
        sentence_text: str = sentence.text
        _sentence_words: list[str] = [w for w in re.findall(r"\b\w+\b", sentence_text)]
        first_word = _sentence_words[0]

        sentence_words: list[str] = [w.lower() for w in _sentence_words]
        shuffled_words: list[str] = random.sample(sentence_words, len(sentence_words))
        data.append(
            SentenceOut(
                id=sentence.id,
                text=sentence.text,
                words=shuffled_words,
                correct_order=sentence_words,
                first_word=first_word
            )
        )

    return data

@router.get("/daily/", response_model=list[WordOut])
def get_daily_words(db: DbSession, current_user: OptionalCurrentUser) -> list[WordOut]:
    selected_ids = _get_daily_selected_word_ids(db, current_user)
    return db.scalars(select(Word).where(Word.id.in_(selected_ids))).all()
