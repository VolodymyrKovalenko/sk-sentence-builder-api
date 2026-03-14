from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from app.db.base import Base
from app.models.word_topic import word_topics
from app.models.mixins import TimestampMixin


class Word(Base, TimestampMixin):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(String(255), nullable=False)
    translation: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[str] = mapped_column(String(2), nullable=False)

    topics: Mapped[list["Topic"]] = relationship(
        secondary=word_topics,
        back_populates="words",
    )
    sentences: Mapped[list["Sentence"]] = relationship(
        back_populates="word",
        cascade="all, delete-orphan",
    )