from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from app.db.base import Base
from app.models.mixins import TimestampMixin


class Sentence(Base, TimestampMixin):
    __tablename__ = "sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    translation: Mapped[str | None] = mapped_column(Text, nullable=True)

    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), nullable=False,
    )
    word: Mapped["Word"] = relationship(back_populates="sentences")