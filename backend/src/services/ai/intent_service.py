import re
from typing import TypedDict, Optional

KNOWN_TOPICS = {
    # History - Ancient & Medieval
    'indus valley civilization': 'Indus Valley Civilisation',
    'indus valley civilisation': 'Indus Valley Civilisation',
    'indus valley': 'Indus Valley Civilisation',
    'harappa': 'Indus Valley Civilisation - Harappa',
    'mohenjo daro': 'Indus Valley Civilisation - Mohenjo-Daro',
    'mohenjodaro': 'Indus Valley Civilisation - Mohenjo-Daro',
    'lothal': 'Indus Valley Civilisation - Lothal',
    'sangam age': 'Ancient Tamil Nadu - Sangam Age',
    'keezhadi': 'Ancient Tamil Nadu - Keezhadi',
    'cholas': 'South Indian Dynasties - Cholas',
    'pandyas': 'South Indian Dynasties - Pandyas',
    'pallavas': 'South Indian Dynasties - Pallavas',
    'mauryan empire': 'Ancient India - Mauryan Empire',
    'maurya': 'Ancient India - Mauryan Empire',
    'gupta': 'Ancient India - Gupta Dynasty',
    'delhi sultanate': 'Medieval India - Delhi Sultanate',
    'mughal': 'Medieval India - Mughal Empire',
    'marathas': 'Medieval India - Maratha Empire',
    # History - Modern & Freedom Struggle
    'freedom struggle': 'Indian National Movement',
    'national movement': 'Indian National Movement',
    '1857 revolt': 'Indian History - 1857 Revolt',
    'indian national congress': 'Indian National Movement - INC',
    'non cooperation': 'Indian National Movement - Non-Cooperation',
    'civil disobedience': 'Indian National Movement - Civil Disobedience',
    'quit india': 'Indian National Movement - Quit India',
    'subhas chandra bose': 'Indian National Movement - INA',
    # Indian Polity
    'indian polity': 'Indian Polity',
    'polity': 'Indian Polity',
    'constitution': 'Indian Polity - Constitution',
    'fundamental rights': 'Indian Polity - Fundamental Rights',
    'directive principles': 'Indian Polity - Directive Principles',
    'dpsp': 'Indian Polity - Directive Principles',
    'fundamental duties': 'Indian Polity - Fundamental Duties',
    'indian parliament': 'Indian Polity - Parliament',
    'parliament': 'Indian Polity - Parliament',
    'supreme court': 'Indian Polity - Judiciary',
    'judiciary': 'Indian Polity - Judiciary',
    'panchayati raj': 'Indian Polity - Local Governance',
    'governor': 'Indian Polity - State Executive',
    'president': 'Indian Polity - Union Executive',
    # Geography
    'geography': 'Geography of India',
    'indian geography': 'Geography of India',
    'monsoon': 'Geography - Monsoon & Climate',
    'rivers': 'Geography - Rivers & Drainage',
    'himalayas': 'Geography - Physical Features',
    # Economy
    'indian economy': 'Indian Economy',
    'economy': 'Indian Economy',
    'rbi': 'Indian Economy - Banking & Monetary Policy',
    'monetary policy': 'Indian Economy - Monetary Policy',
    'fiscal policy': 'Indian Economy - Public Finance',
    'budget': 'Indian Economy - Budget',
    'five year plans': 'Indian Economy - Planning',
    'gst': 'Indian Economy - Taxation',
    # General Science
    'general science': 'General Science',
    'science': 'General Science',
    'physics': 'General Science - Physics',
    'chemistry': 'General Science - Chemistry',
    'biology': 'General Science - Biology',
    'cell biology': 'General Science - Cell Biology',
    'human physiology': 'General Science - Human Physiology',
    'genetics': 'General Science - Genetics',
    # Aptitude
    'aptitude': 'Aptitude & Mental Ability',
    'maths': 'Aptitude & Mental Ability',
    'reasoning': 'Reasoning',
}

class IntentResult(TypedDict):
    intent: str
    topic: Optional[str]
    custom_topic: Optional[str]
    question_count: int
    difficulty: str
    duration_minutes: Optional[int]
    source: str
    is_referring_to_chat_content: bool

def detect_intent(message: str, has_prior_study_content: bool = False) -> IntentResult:
    text = message.strip()
    lower = text.lower()

    # Determine reference to chat content
    content_refs = ['from this', 'from the above', 'from my notes', 'from what i pasted', 'based on this', 'from text', 'this topic', 'from here']
    refers_to_content = any(ref in lower for ref in content_refs) or ('this' in lower and has_prior_study_content)

    # 1. Extract question count if present
    count = 10
    count_match = re.search(r'(\d+)\s*(?:questions?|mcqs?|queries|cards)', lower)
    if not count_match:
        count_match = re.search(r'(?:generate|practice|ask|give me|test me on|take)\s+(\d+)', lower)
    if count_match:
        val = int(count_match.group(1))
        if 1 <= val <= 100:
            count = val

    # 2. Extract duration in minutes if present
    duration = None
    duration_match = re.search(r'(\d+)\s*(?:mins?|minutes?)', lower)
    if duration_match:
        duration = int(duration_match.group(1))
    else:
        hr_match = re.search(r'(\d+)\s*(?:hrs?|hours?)', lower)
        if hr_match:
            duration = int(hr_match.group(1)) * 60

    # 3. Extract difficulty
    difficulty = 'MIXED'
    if 'easy' in lower:
        difficulty = 'EASY'
    elif 'hard' in lower or 'difficult' in lower:
        difficulty = 'HARD'
    elif 'medium' in lower or 'moderate' in lower:
        difficulty = 'MEDIUM'

    # 4. Extract topic
    topic = None
    custom_topic = None
    for key, val in KNOWN_TOPICS.items():
        if re.search(rf'\b{re.escape(key)}\b', lower):
            topic = val
            break

    # If no predefined topic, check for phrases like "define <Topic>", "explain <Topic>", "on <Topic>", etc.
    if not topic:
        def_match = re.search(r'(?:define|meaning of|definition of|overview of|details on|explain|about|on|from|topic)\s+([A-Za-z0-9\s\-]+?)(?:\s+for\s+\d+|\s+with\s+\d+|$|\.|\?)', text, re.IGNORECASE)
        if def_match:
            candidate = def_match.group(1).strip()
            if candidate.lower() not in ['this', 'that', 'it', 'my notes', 'the content', 'the above', 'a practice', 'a mock test', 'questions']:
                custom_topic = candidate
                topic = candidate

    source = 'CHAT_CONTENT' if refers_to_content and has_prior_study_content else 'DATABASE'

    # 5. Classify intent
    # Practice Intent
    if any(k in lower for k in ['practice', 'i want to practice', 'practice questions', 'practice test', 'start practice']):
        return {
            'intent': 'PRACTICE',
            'topic': topic or ('Pasted Study Content' if refers_to_content else 'Indian Polity'),
            'custom_topic': custom_topic,
            'question_count': count,
            'difficulty': difficulty,
            'duration_minutes': None,
            'source': source,
            'is_referring_to_chat_content': refers_to_content
        }

    # Mock Test Intent
    if any(k in lower for k in ['mock test', 'mock', 'conduct a mock', 'conduct an exam', 'full test', 'timed test', 'start a mock']):
        return {
            'intent': 'MOCK_TEST',
            'topic': topic or 'Indian Polity',
            'custom_topic': custom_topic,
            'question_count': count if count != 10 else 20,
            'difficulty': difficulty,
            'duration_minutes': duration or 30,
            'source': 'DATABASE',
            'is_referring_to_chat_content': False
        }

    # Revision Intent
    if any(k in lower for k in ['revise', 'revision', 'wrong answers', 'mistakes', 'revise this']):
        return {
            'intent': 'REVISION',
            'topic': topic,
            'custom_topic': custom_topic,
            'question_count': count,
            'difficulty': difficulty,
            'duration_minutes': None,
            'source': 'DATABASE',
            'is_referring_to_chat_content': refers_to_content
        }

    # MCQ Generation Intent (Learning Mode in Chat)
    if (
        re.search(r'\b(?:generate|create|give|make|ask|quiz)\b.*?\b(?:mcqs?|questions?)\b', lower)
        or any(k in lower for k in ['generate mcq', 'generate questions', 'give me mcq', 'give me questions', 'create questions', 'ask me questions', 'quiz me', 'create mcq', 'mcqs from this', 'mcqs on', 'questions on'])
    ):
        return {
            'intent': 'GENERATE_MCQ',
            'topic': topic,
            'custom_topic': custom_topic,
            'question_count': count if count <= 20 else 10,
            'difficulty': difficulty,
            'duration_minutes': None,
            'source': source,
            'is_referring_to_chat_content': refers_to_content
        }

    # Simple Explanation Intent
    if any(k in lower for k in ['explain simply', 'simply', 'easy english', 'simple language', 'simple english', 'beginner', 'like a beginner', 'make this easy', 'in simple terms']):
        return {
            'intent': 'SIMPLIFY',
            'topic': topic,
            'custom_topic': custom_topic,
            'question_count': 0,
            'difficulty': difficulty,
            'duration_minutes': None,
            'source': source,
            'is_referring_to_chat_content': refers_to_content
        }

    # Summary Intent
    if any(k in lower for k in ['summarize', 'summary', 'short notes', 'important points', 'key takeaways', 'bullet points', 'main points']):
        return {
            'intent': 'SUMMARIZE',
            'topic': topic,
            'custom_topic': custom_topic,
            'question_count': 0,
            'difficulty': difficulty,
            'duration_minutes': None,
            'source': source,
            'is_referring_to_chat_content': refers_to_content
        }

    # General Explanation Intent
    if any(k in lower for k in ['define', 'explain', 'teach me', 'what is', 'what does', 'meaning of', 'definition of', 'tell me about', 'describe', 'overview of', 'brief on', 'who is', 'who was', 'where was']):
        return {
            'intent': 'EXPLAIN',
            'topic': topic,
            'custom_topic': custom_topic,
            'question_count': 0,
            'difficulty': difficulty,
            'duration_minutes': None,
            'source': source,
            'is_referring_to_chat_content': refers_to_content
        }

    # General study conversation
    return {
        'intent': 'GENERAL_CHAT',
        'topic': topic,
        'custom_topic': custom_topic,
        'question_count': count,
        'difficulty': difficulty,
        'duration_minutes': duration,
        'source': source,
        'is_referring_to_chat_content': refers_to_content
    }
