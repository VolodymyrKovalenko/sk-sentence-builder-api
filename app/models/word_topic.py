from sqlalchemy import Table, Column, ForeignKey
from app.db.base import Base

word_topics = Table(
    "word_topics",
    Base.metadata,
    Column("word_id", ForeignKey("words.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
)