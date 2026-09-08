from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class Test(Base):
    __tablename__ = 'tests'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    topic_id: Mapped[int | None] = mapped_column(ForeignKey('topics.id'), nullable=True)
    custom_topic: Mapped[str | None] = mapped_column(String(200), nullable=True)
    question_source: Mapped[str] = mapped_column(String(30), default='DATABASE')
    chat_session_id: Mapped[int | None] = mapped_column(ForeignKey('chat_sessions.id'), nullable=True)
    test_type: Mapped[str] = mapped_column(String(20))
    total_questions: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default='IN_PROGRESS')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

