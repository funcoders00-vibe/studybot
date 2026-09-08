from sqlalchemy.orm import Session
from src.repository.question_repository import select_questions
from src.repository.topic_repository import get_topic, list_topics
from src.services.test_services import start_test
from src.models.question_model import Question
from src.services.ai.question_generation_service import generate_grounded_questions

def start_mock_test(db: Session, user_id: int, request):
    topic = None
    target_topic_id = None
    custom_topic = (request.custom_topic or '').strip()

    if request.topic_id:
        topic = get_topic(db, request.topic_id)
        if not topic:
            raise ValueError('Predefined topic not found')
        target_topic_id = topic.id
    elif custom_topic:
        all_topics = list_topics(db)
        matched = next((t for t in all_topics if t.name.lower() in custom_topic.lower() or custom_topic.lower() in t.name.lower()), None)
        if matched:
            topic = matched
            target_topic_id = matched.id
        else:
            topic = all_topics[0] if all_topics else None
            target_topic_id = topic.id if topic else None
    else:
        all_topics = list_topics(db)
        topic = all_topics[0] if all_topics else None
        target_topic_id = topic.id if topic else None

    # Handle custom topic generation
    if custom_topic and not request.topic_id:
        raw_questions = generate_grounded_questions(
            topic=custom_topic,
            study_content="",
            count=request.number_of_questions,
            difficulty=request.difficulty,
            source_type='AI_GENERATED'
        )
        questions = [
            Question(
                topic_id=target_topic_id or 1,
                difficulty=q.get('difficulty', request.difficulty).upper(),
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option'],
                explanation=q.get('explanation', ''),
                source_book=q.get('source_book', 'TNPSC Syllabus & PYQ'),
                source_chapter=custom_topic,
                source_page=str(q.get('source_page', '1'))
            )
            for q in raw_questions
        ]
        db.add_all(questions)
        db.flush()
        return start_test(
            db,
            user_id,
            target_topic_id,
            questions,
            'MOCK_TEST',
            duration=request.duration_minutes,
            question_source='AI_GENERATED',
            custom_topic=custom_topic,
            chat_session_id=request.chat_session_id
        )

    # Standard database + syllabus generation
    existing_questions = select_questions(db, target_topic_id, request.number_of_questions, request.difficulty) if target_topic_id else []
    if len(existing_questions) < request.number_of_questions:
        needed = request.number_of_questions - len(existing_questions)
        generated_raw = generate_grounded_questions(
            topic=topic.name if topic else "General Studies",
            study_content="",
            count=needed,
            difficulty=request.difficulty,
            source_type='AI_GENERATED'
        )
        new_questions = [
            Question(
                topic_id=target_topic_id or 1,
                difficulty=q.get('difficulty', request.difficulty).upper(),
                question_text=q['question_text'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option'],
                explanation=q.get('explanation', ''),
                source_book=q.get('source_book', 'TNPSC Syllabus & PYQ'),
                source_chapter=topic.name if topic else 'General Studies',
                source_page=str(q.get('source_page', '1'))
            )
            for q in generated_raw
        ]
        db.add_all(new_questions)
        db.flush()
        existing_questions.extend(new_questions)

    return start_test(
        db,
        user_id,
        target_topic_id,
        existing_questions[:request.number_of_questions],
        'MOCK_TEST',
        duration=request.duration_minutes,
        question_source='DATABASE',
        custom_topic=custom_topic or (topic.name if topic else None),
        chat_session_id=request.chat_session_id
    )
