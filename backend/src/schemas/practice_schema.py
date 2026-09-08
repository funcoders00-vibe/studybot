from typing import Optional
from pydantic import BaseModel, Field

class StartPracticeRequest(BaseModel):
    topic_id: Optional[int] = None
    custom_topic: Optional[str] = None
    number_of_questions: int = Field(default=10, ge=1, le=100)
    difficulty: str = 'MIXED'
    source: str = 'DATABASE'
    chat_session_id: Optional[int] = None
