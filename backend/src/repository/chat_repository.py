from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.chat_session_model import ChatSession
from src.models.chat_message_model import ChatMessage

def create_session(db: Session, user_id: int, title: Optional[str] = None) -> ChatSession:
    session = ChatSession(user_id=user_id, title=title or 'New Study Session')
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def list_sessions(db: Session, user_id: int) -> List[ChatSession]:
    return db.query(ChatSession).filter_by(user_id=user_id).order_by(ChatSession.updated_at.desc()).all()

def get_session(db: Session, session_id: int, user_id: int) -> Optional[ChatSession]:
    return db.query(ChatSession).filter_by(id=session_id, user_id=user_id).first()

def update_session_title(db: Session, session: ChatSession, title: str) -> ChatSession:
    session.title = title
    db.commit()
    db.refresh(session)
    return session

def delete_session(db: Session, session_id: int, user_id: int) -> bool:
    session = get_session(db, session_id, user_id)
    if not session:
        return False
    db.delete(session)
    db.commit()
    return True

def create_message(db: Session, session_id: int, role: str, content: str) -> ChatMessage:
    msg = ChatMessage(chat_session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_messages(db: Session, session_id: int) -> List[ChatMessage]:
    return db.query(ChatMessage).filter_by(chat_session_id=session_id).order_by(ChatMessage.created_at.asc()).all()

def get_recent_messages(db: Session, session_id: int, limit: int = 10) -> List[ChatMessage]:
    return db.query(ChatMessage).filter_by(chat_session_id=session_id).order_by(ChatMessage.created_at.desc()).limit(limit).all()[::-1]

def get_latest_study_content(db: Session, session_id: int) -> str:
    """
    Finds the most recent substantial study notes pasted by the user in this session.
    Excludes questions, prompt commands, and short requests.
    """
    messages = db.query(ChatMessage).filter_by(chat_session_id=session_id, role='USER').order_by(ChatMessage.created_at.desc()).all()
    command_prefixes = (
        'generate', 'practice', 'start', 'mock', 'create', 'make', 'give', 'quiz',
        'explain', 'summarize', 'define', 'what', 'who', 'how', 'why', 'where', 'when', 'tell me', 'i want', 'can you'
    )
    for m in messages:
        txt = m.content.strip()
        lower = txt.lower()
        if len(txt) > 90 and not txt.endswith('?') and not any(lower.startswith(p) for p in command_prefixes):
            return txt
    return ""
