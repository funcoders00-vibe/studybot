from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.session_model import Session as UserSession
from src.repository import login_repository
from src.settings import settings
from src.utils.password import verify_password
def login(db: Session, email: str, password: str):
    user = login_repository.find_user_by_email(db, email)
    if not user or not user.is_active or not verify_password(password, user.password_hash): raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid email or password')
    session = UserSession(user_id=user.id, session_token=secrets.token_urlsafe(48), expires_at=datetime.utcnow() + timedelta(hours=settings.session_expire_hours))
    return user, login_repository.create_session(db, session)
