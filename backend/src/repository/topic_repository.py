from sqlalchemy.orm import Session
from src.models.topic_model import Topic
def list_topics(db: Session): return db.query(Topic).order_by(Topic.name).all()
def get_topic(db: Session, topic_id: int): return db.get(Topic, topic_id)
