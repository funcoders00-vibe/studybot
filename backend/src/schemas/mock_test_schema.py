from typing import Optional
from pydantic import BaseModel, Field

class StartMockTestRequest(BaseModel):
    topic_id: Optional[int] = None
    custom_topic: Optional[str] = None
    number_of_questions: int = Field(default=20, ge=1, le=100)
    difficulty: str = 'MIXED'
    duration_minutes: int = Field(default=30, ge=1, le=180)
    source: str = 'DATABASE'
    chat_session_id: Optional[int] = None
