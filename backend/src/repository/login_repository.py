from sqlalchemy.orm import Session
from src.models.user_model import User
from src.models.session_model import Session as UserSession
def find_user_by_email(db: Session, email: str): return db.query(User).filter_by(email=email).first()
def create_session(db: Session, session: UserSession): db.add(session); db.commit(); db.refresh(session); return session
def deactivate_session(db: Session, token: str): db.query(UserSession).filter_by(session_token=token).update({'is_active': False}); db.commit()
