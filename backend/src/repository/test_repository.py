from sqlalchemy.orm import Session
from src.models.test_model import Test
from src.models.test_question_model import TestQuestion
from src.models.user_answer_model import UserAnswer
def create_test(db: Session, test: Test, question_ids: list[int]):
    db.add(test); db.flush()
    db.add_all([TestQuestion(test_id=test.id, question_id=qid, question_order=i + 1) for i, qid in enumerate(question_ids)])
    db.commit(); db.refresh(test); return test
def get_owned_test(db: Session, test_id: int, user_id: int): return db.query(Test).filter_by(id=test_id, user_id=user_id).first()
def test_questions(db: Session, test_id: int): return db.query(TestQuestion).filter_by(test_id=test_id).order_by(TestQuestion.question_order).all()
def save_answers(db: Session, answers: list[UserAnswer]): db.add_all(answers); db.commit()
