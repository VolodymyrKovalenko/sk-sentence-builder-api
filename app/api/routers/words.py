from fastapi import APIRouter, Depends, HTTPException
import re
import random
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.word import WordOut
from app.schemas.sentence import SentenceOut
from app.utils.random import get_daily_random_ids
from app.models.word import Word
from app.models.sentence import Sentence

router = APIRouter(prefix="/words", tags=["words"])


@router.get("/", response_model=list[WordOut])
def get_all_words(db: Session = Depends(get_db)) -> list[WordOut]:
    return db.scalars(select(Word)).all()


@router.get("/{word_id}/sentences/", response_model=list[SentenceOut])
def get_word_sentences(word_id: int, db: Session = Depends(get_db)) -> list[SentenceOut]:
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
def get_daily_words(db: Session = Depends(get_db)) -> list[WordOut]:
    all_words = db.scalars(select(Word)).all()
    ids = [word.id for word in all_words]

    selected_ids = get_daily_random_ids(ids)
    return [word for word in all_words if word.id in selected_ids]
