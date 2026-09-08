from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class UserAnswer(Base):
    __tablename__ = 'user_answers'
    __table_args__ = (UniqueConstraint('test_id', 'question_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    selected_option: Mapped[str] = mapped_column(String(1))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
