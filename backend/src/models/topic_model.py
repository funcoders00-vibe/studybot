from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base

class Topic(Base):
    __tablename__ = 'topics'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    exam_category: Mapped[str] = mapped_column(String(30), default='COMMON')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
