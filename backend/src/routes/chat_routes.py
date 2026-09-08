from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.utils.auth import get_current_user
from src.schemas.chat_schema import (
    CreateChatSessionRequest,
    ChatSessionResponse,
    ChatMessageRequest,
    ChatProcessResponse,
    ChatHistoryResponse
)
from src.services import chat_services

router = APIRouter(prefix='/chat', tags=['chat'])

@router.post('/sessions', response_model=dict)
def create_session(
    body: CreateChatSessionRequest = CreateChatSessionRequest(),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    session = chat_services.create_chat_session(db, user.id, body.title)
    return {
        'success': True,
        'message': 'Chat session created',
        'data': {
            'id': session.id,
            'title': session.title,
            'created_at': session.created_at,
            'updated_at': session.updated_at
        }
    }

@router.get('/sessions', response_model=dict)
def list_sessions(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    sessions = chat_services.list_user_sessions(db, user.id)
    return {
        'success': True,
        'message': 'Chat sessions retrieved',
        'data': [
            {
                'id': s.id,
                'title': s.title,
                'created_at': s.created_at,
                'updated_at': s.updated_at
            } for s in sessions
        ]
    }

@router.get('/sessions/{session_id}', response_model=dict)
def get_session_history(
    session_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    history = chat_services.get_chat_history(db, session_id, user.id)
    s = history['session']
    return {
        'success': True,
        'message': 'Chat history retrieved',
        'data': {
            'session': {
                'id': s.id,
                'title': s.title,
                'created_at': s.created_at,
                'updated_at': s.updated_at
            },
            'messages': [
                {
                    'id': m.id,
                    'chat_session_id': m.chat_session_id,
                    'role': m.role,
                    'content': m.content,
                    'created_at': m.created_at
                } for m in history['messages']
            ]
        }
    }

@router.delete('/sessions/{session_id}', response_model=dict)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    chat_services.delete_chat_session(db, session_id, user.id)
    return {'success': True, 'message': 'Chat session deleted'}

@router.post('/{session_id}/message', response_model=dict)
@router.post('/sessions/{session_id}/messages', response_model=dict)
def send_message(
    session_id: int,
    body: ChatMessageRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    text = body.text
    if not text:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
    result = chat_services.process_chat_message(db, session_id, user.id, text)
    return {
        'success': True,
        'message': 'Message processed',
        'data': result
    }
