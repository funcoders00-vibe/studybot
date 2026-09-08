from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.models.question_model import Question
from src.models.test_model import Test
from src.models.user_answer_model import UserAnswer
from src.models.wrong_answer_model import WrongAnswer
from src.models.topic_performance_model import TopicPerformance
from src.repository import test_repository
def start_test(
    db: Session,
    user_id: int,
    topic_id: int | None,
    questions: list[Question],
    test_type: str,
    duration: int,
    question_source: str = 'DATABASE',
    custom_topic: str | None = None,
    chat_session_id: int | None = None
):
    if not questions:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'No questions match this selection')
    return test_repository.create_test(
        db,
        Test(
            user_id=user_id,
            topic_id=topic_id,
            custom_topic=custom_topic,
            question_source=question_source,
            chat_session_id=chat_session_id,
            test_type=test_type,
            total_questions=len(questions),
            duration_minutes=duration
        ),
        [q.id for q in questions]
    )

def submit_test(db: Session, test: Test, answers):
    if test.status == 'COMPLETED': raise HTTPException(status.HTTP_409_CONFLICT, 'Test already completed')
    question_ids = {mapping.question_id for mapping in test_repository.test_questions(db, test.id)}
    submitted = {answer.question_id: answer.selected_option for answer in answers}
    if not set(submitted).issubset(question_ids): raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid question submitted')
    questions = {q.id: q for q in db.query(Question).filter(Question.id.in_(question_ids)).all()}
    saved=[]; correct=0
    for question_id in question_ids:
        selected = submitted.get(question_id, '')
        is_correct = selected == questions[question_id].correct_option
        correct += is_correct
        saved.append(UserAnswer(test_id=test.id, question_id=question_id, selected_option=selected or ' ', is_correct=is_correct))
        if not is_correct:
            wrong = db.query(WrongAnswer).filter_by(user_id=test.user_id, question_id=question_id).first()
            if wrong: wrong.wrong_count += 1; wrong.last_wrong_at = datetime.utcnow(); wrong.needs_revision = True
            else: db.add(WrongAnswer(user_id=test.user_id, question_id=question_id))
    db.add_all(saved)
    total = len(question_ids)
    if test.topic_id:
        performance = db.query(TopicPerformance).filter_by(user_id=test.user_id, topic_id=test.topic_id).first()
        if not performance:
            performance = TopicPerformance(
                user_id=test.user_id,
                topic_id=test.topic_id,
                total_attempted=0,
                correct_answers=0,
                wrong_answers=0,
                accuracy_percentage=0.0
            )
            db.add(performance)
        performance.total_attempted = (performance.total_attempted or 0) + total
        performance.correct_answers = (performance.correct_answers or 0) + correct
        performance.wrong_answers = (performance.wrong_answers or 0) + (total - correct)
        performance.accuracy_percentage = round(performance.correct_answers / performance.total_attempted * 100, 2) if performance.total_attempted else 0
    test.status = 'COMPLETED'
    test.completed_at = datetime.utcnow()
    db.commit()
    return {'total_questions': total, 'correct_answers': correct, 'wrong_answers': total - correct, 'score_percentage': round(correct / total * 100, 2) if total else 0}
