from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class WrongAnswer(Base):
    __tablename__ = 'wrong_answers'
    __table_args__ = (UniqueConstraint('user_id', 'question_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    wrong_count: Mapped[int] = mapped_column(Integer, default=1)
    last_wrong_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    needs_revision: Mapped[bool] = mapped_column(Boolean, default=True)
