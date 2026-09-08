from sqlalchemy import func
from sqlalchemy.orm import Session
from src.models.question_model import Question
def select_questions(db: Session, topic_id: int, count: int, difficulty: str = 'MIXED'):
    query = db.query(Question).filter_by(topic_id=topic_id)
    if difficulty != 'MIXED': query = query.filter(func.upper(Question.difficulty) == difficulty.upper())
    return query.order_by(func.random()).limit(count).all()
