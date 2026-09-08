from sqlalchemy.orm import Session
from src.repository.progress_repository import overview, topic_rows
from src.models.test_model import Test

def overview_data(db: Session, user_id: int):
    attempted, correct, wrong = overview(db, user_id)
    tests_completed = db.query(Test).filter_by(user_id=user_id, status='COMPLETED').count()
    return {
        'total_attempted': attempted,
        'correct_answers': correct,
        'wrong_answers': wrong,
        'overall_accuracy': round(correct / attempted * 100, 2) if attempted else 0,
        'tests_completed': tests_completed
    }

def topics_data(db: Session, user_id: int):
    return [{'topic_id': topic.id, 'name': topic.name, 'total_attempted': perf.total_attempted if perf else 0, 'accuracy_percentage': perf.accuracy_percentage if perf else 0} for topic, perf in topic_rows(db, user_id)]

