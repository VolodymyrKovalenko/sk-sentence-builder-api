from fastapi import APIRouter, HTTPException
from app.data.mock_lessons import mock_lessons
from app.schemas.lesson import WordLessonOut

router = APIRouter(prefix="/practice", tags=["practice"])


@router.get("/{word_id}", response_model=WordLessonOut)
def get_practice_lesson(word_id: int) -> WordLessonOut:
    lesson = next((lesson for lesson in mock_lessons if lesson.wordId == word_id), None)

    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson