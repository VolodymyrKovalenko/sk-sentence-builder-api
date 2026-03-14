from pydantic import BaseModel, ConfigDict


class WordOut(BaseModel):
    id: int
    text: str
    translation: str
    level: str

    model_config = ConfigDict(from_attributes=True)