from sqlalchemy.orm import Session
from src.models.question_model import Question
from src.repository.revision_repository import wrong_questions
from src.services.test_services import start_test
def get_wrong_answers(db: Session, user_id: int, topic_id: int | None, limit: int): return wrong_questions(db,user_id,topic_id,limit)
def start_revision(db: Session, user_id: int, request):
    rows = wrong_questions(db,user_id,request.topic_id,request.number_of_questions)
    return start_test(db,user_id,request.topic_id,[row[0] for row in rows],'REVISION',0)
