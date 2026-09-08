from sqlalchemy.orm import Session
from src.models.wrong_answer_model import WrongAnswer
from src.models.question_model import Question
def wrong_questions(db: Session, user_id: int, topic_id: int | None, limit: int):
    query = db.query(Question, WrongAnswer).join(WrongAnswer, WrongAnswer.question_id == Question.id).filter(WrongAnswer.user_id == user_id, WrongAnswer.needs_revision.is_(True))
    if topic_id: query = query.filter(Question.topic_id == topic_id)
    return query.order_by(WrongAnswer.wrong_count.desc(), WrongAnswer.last_wrong_at.desc()).limit(limit).all()
