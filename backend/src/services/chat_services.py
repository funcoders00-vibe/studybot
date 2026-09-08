import re
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repository import chat_repository
from src.services.ai.intent_service import detect_intent
from src.services.ai.content_explanation_service import generate_explanation
from src.services.ai.question_generation_service import generate_grounded_questions

def create_chat_session(db: Session, user_id: int, title: str | None = None):
    return chat_repository.create_session(db, user_id, title)

def list_user_sessions(db: Session, user_id: int):
    return chat_repository.list_sessions(db, user_id)

def get_chat_history(db: Session, session_id: int, user_id: int):
    session = chat_repository.get_session(db, session_id, user_id)
    if not session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Chat session not found")
    messages = chat_repository.get_messages(db, session_id)
    return {'session': session, 'messages': messages}

def delete_chat_session(db: Session, session_id: int, user_id: int):
    success = chat_repository.delete_session(db, session_id, user_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Chat session not found")
    return {'success': True}

def process_chat_message(db: Session, session_id: int, user_id: int, message_text: str) -> Dict[str, Any]:
    session = chat_repository.get_session(db, session_id, user_id)
    if not session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Chat session not found")

    text = message_text.strip()
    if not text:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Message cannot be empty")

    # 1. Save user message
    chat_repository.create_message(db, session_id, 'USER', text)

    # 2. Update session title if default
    if session.title in ['New Study Session', 'New Chat']:
        clean_title = re.sub(r'[\r\n]+', ' ', text)[:40].strip()
        chat_repository.update_session_title(db, session, clean_title or 'Study Chat')

    # 3. Fetch prior study content in this session
    prior_study_content = chat_repository.get_latest_study_content(db, session_id)

    # Check if the user is pasting a substantial paragraph of study content directly
    is_pasted_content = len(text) > 140 and not text.endswith('?') and not any(text.lower().startswith(q) for q in ['explain', 'summarize', 'generate', 'practice', 'what', 'who', 'how', 'why', 'tell me'])

    if is_pasted_content:
        reply_message = (
            "📖 **Study Material Captured!**\n\n"
            "I've indexed your notes. What would you like to do next?\n\n"
            "- **Explain Simply**: *'Explain this in simple English'*\n"
            "- **Summary**: *'Give me short notes from this'*\n"
            "- **MCQs**: *'Generate 10 questions from this'*\n"
            "- **Practice**: *'I want to practice 10 questions from this'*"
        )
        chat_repository.create_message(db, session_id, 'ASSISTANT', reply_message)
        return {
            'response_type': 'GENERAL_RESPONSE',
            'message': reply_message,
            'action': 'NONE',
            'parameters': None,
            'mcqs': None
        }

    # 4. Intent detection
    intent_data = detect_intent(text, has_prior_study_content=bool(prior_study_content))
    intent = intent_data['intent']
    active_content = prior_study_content if intent_data['is_referring_to_chat_content'] else ""

    # Infer session topic from prior conversation if not explicitly stated in current message
    session_topic = intent_data['topic'] or intent_data['custom_topic']
    if not session_topic:
        recent_msgs = chat_repository.get_recent_messages(db, session_id, limit=8)
        for prev_m in reversed(recent_msgs):
            if prev_m.role == 'USER' and prev_m.content.strip().lower() != text.strip().lower():
                prev_intent = detect_intent(prev_m.content)
                if prev_intent.get('topic') or prev_intent.get('custom_topic'):
                    session_topic = prev_intent.get('topic') or prev_intent.get('custom_topic')
                    break

    # 5. Route by Intent
    if intent in ['EXPLAIN', 'SIMPLIFY', 'SUMMARIZE']:
        explanation = generate_explanation(
            query=text,
            topic=session_topic or "",
            study_content=active_content or prior_study_content,
            mode=intent
        )
        chat_repository.create_message(db, session_id, 'ASSISTANT', explanation)
        return {
            'response_type': 'EXPLANATION' if intent != 'SUMMARIZE' else 'SUMMARY',
            'message': explanation,
            'action': 'NONE',
            'parameters': None,
            'mcqs': None
        }

    if intent == 'GENERATE_MCQ':
        q_count = intent_data['question_count'] or 10
        raw_mcqs = generate_grounded_questions(
            topic=session_topic or "Indus Valley Civilisation",
            study_content=active_content or prior_study_content,
            count=q_count,
            difficulty=intent_data['difficulty'],
            source_type=intent_data['source']
        )
        formatted_mcqs = []
        for q in raw_mcqs:
            formatted_mcqs.append({
                'question': q['question_text'],
                'options': {
                    'A': q['option_a'],
                    'B': q['option_b'],
                    'C': q['option_c'],
                    'D': q['option_d'],
                },
                'correct_option': q['correct_option'],
                'explanation': q.get('explanation', ''),
                'difficulty': q.get('difficulty', intent_data['difficulty']),
                'source_book': q.get('source_book', 'StudyBot Bank')
            })

        source_desc = "your provided study notes" if (active_content or prior_study_content) else "the official syllabus and past examination papers"
        reply_message = f"Here are **{len(formatted_mcqs)} questions** generated from {source_desc}. Review the questions, options, and explanations below:"
        chat_repository.create_message(db, session_id, 'ASSISTANT', reply_message)
        return {
            'response_type': 'MCQ_GENERATION',
            'message': reply_message,
            'action': 'SHOW_MCQ',
            'parameters': {
                'topic': intent_data['topic'],
                'custom_topic': intent_data['custom_topic'],
                'question_count': len(formatted_mcqs),
                'difficulty': intent_data['difficulty'],
                'source': intent_data['source'],
                'chat_session_id': session_id
            },
            'mcqs': formatted_mcqs
        }

    if intent == 'PRACTICE':
        reply_message = (
            f"Ready to practice **{intent_data['topic'] or 'this topic'}**! "
            f"I have configured a session with {intent_data['question_count']} questions ({intent_data['difficulty']} difficulty). "
            "You can launch directly or edit any details before starting."
        )
        chat_repository.create_message(db, session_id, 'ASSISTANT', reply_message)
        return {
            'response_type': 'PRACTICE_REQUEST',
            'message': reply_message,
            'action': 'OPEN_PRACTICE',
            'parameters': {
                'topic': intent_data['topic'],
                'custom_topic': intent_data['custom_topic'],
                'question_count': intent_data['question_count'],
                'difficulty': intent_data['difficulty'],
                'source': intent_data['source'],
                'chat_session_id': session_id
            },
            'mcqs': None
        }

    if intent == 'MOCK_TEST':
        duration = intent_data['duration_minutes'] or 30
        reply_message = (
            f"Let's prepare your **{intent_data['topic'] or 'General Studies'}** Mock Test! "
            f"Configured: {intent_data['question_count']} questions · {duration} minutes · {intent_data['difficulty']} difficulty."
        )
        chat_repository.create_message(db, session_id, 'ASSISTANT', reply_message)
        return {
            'response_type': 'MOCK_TEST_REQUEST',
            'message': reply_message,
            'action': 'OPEN_MOCK_TEST',
            'parameters': {
                'topic': intent_data['topic'],
                'custom_topic': intent_data['custom_topic'],
                'question_count': intent_data['question_count'],
                'difficulty': intent_data['difficulty'],
                'duration_minutes': duration,
                'source': 'DATABASE',
                'chat_session_id': session_id
            },
            'mcqs': None
        }

    if intent == 'REVISION':
        reply_message = "Navigating to your personalized revision sanctuary to review past wrong answers."
        chat_repository.create_message(db, session_id, 'ASSISTANT', reply_message)
        return {
            'response_type': 'GENERAL_RESPONSE',
            'message': reply_message,
            'action': 'OPEN_REVISION',
            'parameters': None,
            'mcqs': None
        }

    # General Chat / Query
    explanation = generate_explanation(query=text, topic=session_topic or "", study_content=active_content or prior_study_content, mode='EXPLAIN')
    chat_repository.create_message(db, session_id, 'ASSISTANT', explanation)
    return {
        'response_type': 'EXPLANATION',
        'message': explanation,
        'action': 'NONE',
        'parameters': None,
        'mcqs': None
    }
