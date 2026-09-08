from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class TopicPerformance(Base):
    __tablename__ = 'topic_performances'
    __table_args__ = (UniqueConstraint('user_id', 'topic_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey('topics.id'))
    total_attempted: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    wrong_answers: Mapped[int] = mapped_column(Integer, default=0)
    accuracy_percentage: Mapped[float] = mapped_column(Float, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
