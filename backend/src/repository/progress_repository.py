from sqlalchemy import func
from sqlalchemy.orm import Session
from src.models.topic_performance_model import TopicPerformance
from src.models.topic_model import Topic
def topic_rows(db: Session, user_id: int): return db.query(Topic, TopicPerformance).outerjoin(TopicPerformance, (TopicPerformance.topic_id == Topic.id) & (TopicPerformance.user_id == user_id)).all()
def overview(db: Session, user_id: int): return db.query(func.coalesce(func.sum(TopicPerformance.total_attempted),0),func.coalesce(func.sum(TopicPerformance.correct_answers),0),func.coalesce(func.sum(TopicPerformance.wrong_answers),0)).filter_by(user_id=user_id).one()
