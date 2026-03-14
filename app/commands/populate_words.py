import json
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.word import Word
from app.models.sentence import Sentence


def seed_words_from_json(file_path: str) -> None:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    level = payload["level"]
    words_data = payload["words"]

    db = SessionLocal()
    try:
        created_words = 0
        skipped_words = 0

        for item in words_data:
            slovak_text = item["slovak"]
            english_translation = item["english"]
            examples = item.get("examples", [])

            existing_word = db.scalar(
                select(Word).where(Word.text == slovak_text)
            )
            if existing_word:
                skipped_words += 1
                continue

            word = Word(
                text=slovak_text,
                translation=english_translation,
                level=level,
            )
            db.add(word)
            db.flush()  # get word.id before inserting sentences

            for example_sentence in examples:
                sentence = Sentence(
                    word_id=word.id,
                    text=example_sentence,
                    translation=None
                )
                db.add(sentence)

            created_words += 1

        db.commit()
        print(f"Created words: {created_words}")
        print(f"Skipped words: {skipped_words}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_words_from_json("app/data/slovak_a2_words_300.json")