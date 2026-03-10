from app.schemas.lesson import WordLessonOut, ExerciseOut


mock_lessons: list[WordLessonOut] = [
    WordLessonOut(
        wordId=1,
        exercises=[
            ExerciseOut(
                id=1,
                words=["zase", "mešká", "dnes", "Autobus"],
                correctAnswer=["Autobus", "dnes", "zase", "mešká"],
            ),
            ExerciseOut(
                id=2,
                words=["do", "Nechcem", "meškať", "práce"],
                correctAnswer=["Nechcem", "meškať", "do", "práce"],
            ),
            ExerciseOut(
                id=3,
                words=["mi", "Ak", "budeme", "zavolaj", "meškať"],
                correctAnswer=["Ak", "budeme", "meškať", "zavolaj", "mi"],
            ),
            ExerciseOut(
                id=4,
                words=["minút", "Vlak", "meškal", "dvadsať"],
                correctAnswer=["Vlak", "meškal", "dvadsať", "minút"],
            ),
            ExerciseOut(
                id=5,
                words=["kvôli", "často", "doprave", "meškám", "Ráno"],
                correctAnswer=["Ráno", "často", "meškám", "kvôli", "doprave"],
            ),
        ],
    ),
    WordLessonOut(
        wordId=2,
        exercises=[
            ExerciseOut(
                id=6,
                words=["večer", "Môžeš", "mne", "ku", "prísť"],
                correctAnswer=["Môžeš", "večer", "prísť", "ku", "mne"],
            ),
            ExerciseOut(
                id=7,
                words=["do", "prísť", "Nestihnem", "načas", "práce"],
                correctAnswer=["Nestihnem", "prísť", "načas", "do", "práce"],
            ),
            ExerciseOut(
                id=8,
                words=["Kedy", "prísť", "chceš", "na", "stanicu"],
                correctAnswer=["Kedy", "chceš", "prísť", "na", "stanicu"],
            ),
            ExerciseOut(
                id=9,
                words=["Prišiel", "som", "veľmi", "domov", "neskoro"],
                correctAnswer=["Prišiel", "som", "domov", "veľmi", "neskoro"],
            ),
            ExerciseOut(
                id=10,
                words=["môžeš", "Ak", "prísť", "zajtra", "aj", "chceš"],
                correctAnswer=["Ak", "chceš", "môžeš", "prísť", "aj", "zajtra"],
            ),
        ],
    ),
]