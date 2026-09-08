from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class TestQuestion(Base):
    __tablename__ = 'test_questions'
    __table_args__ = (UniqueConstraint('test_id', 'question_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    question_order: Mapped[int] = mapped_column(Integer)
