from pydantic import BaseModel


class WordOut(BaseModel):
    id: int
    value: str
    translation: str
    topic: str
    level: str