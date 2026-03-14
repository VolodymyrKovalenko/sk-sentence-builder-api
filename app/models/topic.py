from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.base import Base
from app.models.mixins import TimestampMixin
from app.models.word_topic import word_topics


class Topic(Base, TimestampMixin):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    words: Mapped[list["Word"]] = relationship(
        secondary=word_topics,
        back_populates="topics",
    )