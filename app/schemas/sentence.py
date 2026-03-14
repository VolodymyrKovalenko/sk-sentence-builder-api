from pydantic import BaseModel


class SentenceOut(BaseModel):
    id: int
    text: str
    words: list[str]
    correct_order: list[str]
    first_word: str
