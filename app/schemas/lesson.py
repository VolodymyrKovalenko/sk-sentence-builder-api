from pydantic import BaseModel


class ExerciseOut(BaseModel):
    id: int
    words: list[str]
    correctAnswer: list[str]


class WordLessonOut(BaseModel):
    wordId: int
    exercises: list[ExerciseOut]