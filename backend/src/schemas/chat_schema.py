from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class CreateChatSessionRequest(BaseModel):
    title: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessageRequest(BaseModel):
    message: Optional[str] = None
    content: Optional[str] = None

    @property
    def text(self) -> str:
        return (self.message or self.content or '').strip()

class ChatMessageResponse(BaseModel):
    id: int
    chat_session_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistoryResponse(BaseModel):
    session: ChatSessionResponse
    messages: List[ChatMessageResponse]

class ChatMCQItem(BaseModel):
    question: str
    options: Dict[str, str]
    correct_option: str
    explanation: str
    difficulty: Optional[str] = 'MEDIUM'
    source_book: Optional[str] = None

class ChatActionParameters(BaseModel):
    topic: Optional[str] = None
    custom_topic: Optional[str] = None
    question_count: Optional[int] = 10
    difficulty: Optional[str] = 'MIXED'
    duration_minutes: Optional[int] = None
    source: Optional[str] = 'DATABASE'
    chat_session_id: Optional[int] = None

class ChatProcessResponse(BaseModel):
    response_type: str  # EXPLANATION, SUMMARY, MCQ_GENERATION, PRACTICE_REQUEST, MOCK_TEST_REQUEST, GENERAL_RESPONSE
    message: str
    action: str  # NONE, OPEN_PRACTICE, OPEN_MOCK_TEST, OPEN_REVISION, SHOW_MCQ
    parameters: Optional[ChatActionParameters] = None
    mcqs: Optional[List[ChatMCQItem]] = None
