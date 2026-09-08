from datetime import datetime
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.session_model import Session as UserSession
from src.models.user_model import User
from src.settings import settings

def get_current_user(token: str | None = Cookie(default=None, alias=settings.session_cookie_name), db: Session = Depends(get_db)) -> User:
    if not token: raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Authentication required')
    session = db.query(UserSession).filter_by(session_token=token, is_active=True).first()
    if not session or session.expires_at <= datetime.utcnow(): raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Session expired')
    user = db.get(User, session.user_id)
    if not user or not user.is_active: raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Unauthorized')
    return user
