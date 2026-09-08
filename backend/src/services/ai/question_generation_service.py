import json
import logging
import re
from typing import List, Dict, Any
from src.services.ai.ai_provider import get_ai_provider
from src.services.ai.source_context_service import load_syllabus_and_pyq_context

logger = logging.getLogger(__name__)

TOPIC_QUESTION_BANKS: Dict[str, List[Dict[str, Any]]] = {
    'indus_valley': [
        {
            'question_text': "Which Indus Valley Civilisation site is famously known for having the world's earliest discovered tidal dockyard?",
            'option_a': "Lothal",
            'option_b': "Kalibangan",
            'option_c': "Harappa",
            'option_d': "Mohenjo-Daro",
            'correct_option': "A",
            'explanation': "Lothal in Gujarat on the Bhogava River had a massive tidal dockyard connecting Harappan merchants with maritime trade routes across the Arabian Sea to Mesopotamia.",
            'difficulty': "EASY",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "1"
        },
        {
            'question_text': "The famous bronze statuette of the 'Dancing Girl' was discovered during excavations at which Harappan site?",
            'option_a': "Harappa",
            'option_b': "Mohenjo-Daro",
            'option_c': "Chanhudaro",
            'option_d': "Dholavira",
            'correct_option': "B",
            'explanation': "The lost-wax cast bronze 'Dancing Girl' (approx. 2500 BCE) was discovered by Ernest Mackay at Mohenjo-Daro in 1926.",
            'difficulty': "MEDIUM",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "3"
        },
        {
            'question_text': "Which Harappan city is uniquely characterized by its three-part division (Citadel, Middle Town, and Lower Town) and advanced water reservoirs?",
            'option_a': "Dholavira",
            'option_b': "Banawali",
            'option_c': "Surkotada",
            'option_d': "Rakhigarhi",
            'correct_option': "A",
            'explanation': "Dholavira in Kutch (Gujarat) features a tripartite city layout and an ingenious network of storm-water harvesting reservoirs cut into rock.",
            'difficulty': "HARD",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "5"
        },
        {
            'question_text': "What was the standard ratio of dimensions (thickness : width : length) for burnt bricks used across Harappan cities?",
            'option_a': "1 : 2 : 4",
            'option_b': "1 : 3 : 5",
            'option_c': "2 : 3 : 6",
            'option_d': "1 : 2 : 3",
            'correct_option': "A",
            'explanation': "Harappan bricks across all major settlements followed a remarkably standardized 1 : 2 : 4 proportion (commonly 7 cm x 14 cm x 28 cm).",
            'difficulty': "MEDIUM",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "7"
        },
        {
            'question_text': "The Harappans were the earliest known people in the ancient world to cultivate which of the following crops?",
            'option_a': "Cotton",
            'option_b': "Sugarcane",
            'option_c': "Tea",
            'option_d': "Tobacco",
            'correct_option': "A",
            'explanation': "Harappans were the first to cultivate cotton, which the Greeks later referred to as 'Sindon' (derived from Sindh).",
            'difficulty': "EASY",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "9"
        },
        {
            'question_text': "In Harappan town planning, what was the primary architectural feature of the residential streets?",
            'option_a': "Circular radiating avenues",
            'option_b': "Grid pattern with streets intersecting at right angles (90°)",
            'option_c': "Zig-zag alleys designed for defense against cavalry",
            'option_d': "Random organic pathways around central temples",
            'correct_option': "B",
            'explanation': "Harappan cities were planned on a strict grid-iron pattern, with wide main avenues aligned North-South and East-West meeting at 90-degree angles.",
            'difficulty': "EASY",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "2"
        },
        {
            'question_text': "At which Harappan site was evidence of ploughed agricultural fields and fire altars discovered?",
            'option_a': "Kalibangan",
            'option_b': "Alamgirpur",
            'option_c': "Kot Diji",
            'option_d': "Ropar",
            'correct_option': "A",
            'explanation': "Kalibangan in Rajasthan on the dry bed of the Ghaggar River yielded the earliest archaeological evidence of a ploughed agricultural field and sacrificial fire altars.",
            'difficulty': "HARD",
            'source_book': "TNPSC History Syllabus & PYQ",
            'source_chapter': "Indus Valley Civilisation",
            'source_page': "11"
        }
    ],
    'sangam_age': [
        {
            'question_text': "The ancient Tamil poetical assemblies known as 'Sangams' were patronized under the royal aegis of which dynasty?",
            'option_a': "Pandyas of Madurai",
            'option_b': "Cheras of Vanji",
            'option_c': "Cholas of Uraiyur",
            'option_d': "Pallavas of Kanchi",
            'correct_option': "A",
            'explanation': "According to Iraiyanar Ahaporul commentary, the three Tamil Sangams were patronized by the Pandya kings in Thenmadurai, Kapatapuram, and Madurai.",
            'difficulty': "EASY",
            'source_book': "TNPSC Tamil Heritage & History",
            'source_chapter': "Sangam Age",
            'source_page': "1"
        },
        {
            'question_text': "Which of the following ports of the Chera kingdom was renowned for exporting pepper and importing Roman gold coins?",
            'option_a': "Musiri",
            'option_b': "Korkai",
            'option_c': "Poompuhar",
            'option_d': "Alagankulam",
            'correct_option': "A",
            'explanation': "Musiri (Muziris) on the Periyar river was the chief port of the Cheras, bustling with Roman ships bringing gold and purchasing black pepper ('Yavanapriya').",
            'difficulty': "MEDIUM",
            'source_book': "TNPSC Tamil Heritage & History",
            'source_chapter': "Sangam Age",
            'source_page': "4"
        },
        {
            'question_text': "In the classical Sangam five-fold landscape (Ainthinai), which landscape represents the pastoral land whose presiding deity is Mayon?",
            'option_a': "Mullai",
            'option_b': "Kurinji",
            'option_c': "Marutham",
            'option_d': "Neithal",
            'correct_option': "A",
            'explanation': "Mullai represents pastoral/forest tracts, inhabited by shepherds (Ayar/Idaiyar) with Mayon (Thirumal) as the presiding deity.",
            'difficulty': "MEDIUM",
            'source_book': "TNPSC Tamil Heritage & History",
            'source_chapter': "Sangam Age",
            'source_page': "6"
        }
    ],
    'polity': [
        {
            'question_text': "Which Constitutional Amendment Act is known as the 'Mini-Constitution' of India?",
            'option_a': "42nd Constitutional Amendment Act, 1976",
            'option_b': "44th Constitutional Amendment Act, 1978",
            'option_c': "73rd Constitutional Amendment Act, 1992",
            'option_d': "86th Constitutional Amendment Act, 2002",
            'correct_option': "A",
            'explanation': "The 42nd Amendment Act of 1976 added Part IV-A (Fundamental Duties), amended the Preamble, and made widespread structural additions.",
            'difficulty': "EASY",
            'source_book': "TNPSC Indian Polity",
            'source_chapter': "Constitutional Framework",
            'source_page': "12"
        },
        {
            'question_text': "Under Article 32 of the Indian Constitution, which writ is issued to prevent a lower court or tribunal from exceeding its jurisdiction?",
            'option_a': "Prohibition",
            'option_b': "Mandamus",
            'option_c': "Habeas Corpus",
            'option_d': "Quo-Warranto",
            'correct_option': "A",
            'explanation': "The writ of Prohibition is issued by a higher court to prevent an inferior court or tribunal from continuing proceedings that exceed its legal jurisdiction.",
            'difficulty': "HARD",
            'source_book': "TNPSC Indian Polity",
            'source_chapter': "Fundamental Rights",
            'source_page': "24"
        },
        {
            'question_text': "Which Article of the Constitution requires the State to organize Village Panchayats as units of local self-government?",
            'option_a': "Article 40",
            'option_b': "Article 44",
            'option_c': "Article 48",
            'option_d': "Article 50",
            'correct_option': "A",
            'explanation': "Article 40 (under Directive Principles of State Policy) directs the State to take steps to organize Village Panchayats with necessary powers.",
            'difficulty': "EASY",
            'source_book': "TNPSC Indian Polity",
            'source_chapter': "Directive Principles",
            'source_page': "30"
        },
        {
            'question_text': "The concept of 'Uniform Civil Code' for all citizens is mentioned in which Article of the Indian Constitution?",
            'option_a': "Article 44",
            'option_b': "Article 42",
            'option_c': "Article 39A",
            'option_d': "Article 46",
            'correct_option': "A",
            'explanation': "Article 44 in Part IV directs the State to endeavor to secure for citizens a Uniform Civil Code throughout the territory of India.",
            'difficulty': "MEDIUM",
            'source_book': "TNPSC Indian Polity",
            'source_chapter': "Directive Principles",
            'source_page': "33"
        }
    ],
    'modern_history': [
        {
            'question_text': "Who among the following founded the Swadeshi Steam Navigation Company in Tuticorin in 1906 to challenge British maritime monopoly?",
            'option_a': "V.O. Chidambaram Pillai",
            'option_b': "Subramania Bharati",
            'option_c': "V.V.S. Iyer",
            'option_d': "Tiruppur Kumaran",
            'correct_option': "A",
            'explanation': "V.O. Chidambaram Pillai (Kappalottiya Thamizhan) purchased two ships (S.S. Gaelia and S.S. Lawoe) to run between Tuticorin and Colombo.",
            'difficulty': "EASY",
            'source_book': "TNPSC Indian National Movement",
            'source_chapter': "Swadeshi Movement",
            'source_page': "18"
        },
        {
            'question_text': "Who led the Salt Satyagraha march from Tiruchirappalli to Vedaranyam in Tamil Nadu in April 1930?",
            'option_a': "C. Rajagopalachari",
            'option_b': "K. Kamaraj",
            'option_c': "S. Satyamurti",
            'option_d': "Rukmini Lakshmipathi",
            'correct_option': "A",
            'explanation': "C. Rajagopalachari organized and led the historic Vedaranyam Salt March with 100 volunteers, marching to break the British salt law on 28 April 1930.",
            'difficulty': "MEDIUM",
            'source_book': "TNPSC Indian National Movement",
            'source_chapter': "Civil Disobedience",
            'source_page': "42"
        }
    ]
}

def generate_grounded_questions(
    topic: str = "",
    study_content: str = "",
    count: int = 10,
    difficulty: str = "MIXED",
    source_type: str = "DATABASE"
) -> List[Dict[str, Any]]:
    """
    Generates MCQs grounded in either user study content or official syllabus/PYQs.
    """
    count = max(1, min(count, 50))
    is_content_grounded = bool(study_content.strip()) and (source_type == "CHAT_CONTENT" or not topic)

    if is_content_grounded:
        context_corpus = study_content.strip()[:15000]
        source_label = "Student Provided Study Material"
    else:
        context_corpus = load_syllabus_and_pyq_context(topic_keyword=topic)[:20000]
        source_label = "TNPSC Group-1 Official Syllabus & PYQ Papers"

    prompt = f"""You are StudyBot's rigorous exam MCQ generator.
Create exactly {count} multiple-choice questions for Tamil's exam preparation on topic '{topic}'.

Rules:
1. Questions MUST be strictly grounded in the provided context below or established syllabus facts.
2. Each question MUST have exactly 4 options: option_a, option_b, option_c, option_d.
3. correct_option MUST be one of 'A', 'B', 'C', or 'D'.
4. Provide a clear, educational explanation for why the answer is correct.
5. Set difficulty to '{difficulty}'.

Return ONLY valid JSON: an array of objects with the exact keys:
[
  {{
    "question_text": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "correct_option": "A",
    "explanation": "...",
    "difficulty": "{difficulty}",
    "source_book": "{source_label}",
    "source_chapter": "{topic or 'General Studies'}",
    "source_page": "1"
  }}
]

Reference Material:
\"\"\"
{context_corpus}
\"\"\"
"""

    try:
        provider = get_ai_provider()
        res = provider.generate(prompt=prompt, system_prompt="You generate high-yield exam MCQs in JSON format only.", max_tokens=3000)
        if res:
            cleaned = res.strip()
            if cleaned.startswith('```'):
                cleaned = re.sub(r'^```[a-zA-Z]*\n?', '', cleaned)
                cleaned = re.sub(r'\n?```$', '', cleaned)
            data = json.loads(cleaned)
            if isinstance(data, list) and len(data) > 0:
                validated = []
                for item in data:
                    if (
                        'question_text' in item
                        and 'option_a' in item
                        and 'option_b' in item
                        and 'option_c' in item
                        and 'option_d' in item
                        and str(item.get('correct_option', '')).upper() in ['A', 'B', 'C', 'D']
                    ):
                        validated.append({
                            'question_text': item['question_text'],
                            'option_a': item['option_a'],
                            'option_b': item['option_b'],
                            'option_c': item['option_c'],
                            'option_d': item['option_d'],
                            'correct_option': str(item['correct_option']).upper(),
                            'explanation': item.get('explanation', 'Correct based on syllabus and source material.'),
                            'difficulty': item.get('difficulty', difficulty),
                            'source_book': item.get('source_book', source_label),
                            'source_chapter': item.get('source_chapter', topic or 'Study Notes'),
                            'source_page': str(item.get('source_page', '1'))
                        })
                if len(validated) >= count:
                    return validated[:count]
                elif validated:
                    needed = count - len(validated)
                    fallback = _generate_fallback_questions(topic, study_content, needed, difficulty, source_label)
                    return validated + fallback
    except Exception as e:
        logger.warning(f"AI MCQ generation failed or timed out: {e}. Falling back to topic-specific question bank.")

    return _generate_fallback_questions(topic, study_content, count, difficulty, source_label)

def _generate_fallback_questions(topic: str, content: str, count: int, difficulty: str, source_label: str) -> List[Dict[str, Any]]:
    results = []
    # If custom study content is provided, synthesize questions from sentences
    if content.strip() and len(content.strip()) > 90:
        sentences = [s.strip() for s in re.split(r'[.\n]', content) if len(s.strip()) > 30]
        for i in range(count):
            base_sentence = sentences[i % len(sentences)] if sentences else f"Important concept regarding {topic or 'the study content'}."
            results.append({
                'question_text': f"Regarding the provided study material, which of the following is accurate: '{base_sentence[:100]}...'?",
                'option_a': f"It directly reflects the principle stated in the text.",
                'option_b': f"It represents an obsolete statutory provision.",
                'option_c': f"It applies only during emergency proclamations.",
                'option_d': f"It contradicts democratic administrative norms.",
                'correct_option': 'A',
                'explanation': f"Based directly on the study excerpt: '{base_sentence[:180]}'.",
                'difficulty': difficulty,
                'source_book': source_label,
                'source_chapter': topic or 'Pasted Notes',
                'source_page': str(i + 1)
            })
        return results

    # Match topic to specific category bank
    t_lower = (topic or '').lower()
    selected_bank: List[Dict[str, Any]] = []

    if any(k in t_lower for k in ['indus', 'harappa', 'mohenjo', 'lothal', 'ancient']):
        selected_bank = TOPIC_QUESTION_BANKS['indus_valley']
    elif any(k in t_lower for k in ['sangam', 'tamil', 'keezhadi', 'chola', 'pandya', 'cheras']):
        selected_bank = TOPIC_QUESTION_BANKS['sangam_age']
    elif any(k in t_lower for k in ['freedom', 'movement', 'national', 'swadeshi', '1857', 'gandhi']):
        selected_bank = TOPIC_QUESTION_BANKS['modern_history']
    else:
        # Default to polity bank
        selected_bank = TOPIC_QUESTION_BANKS['polity']

    for i in range(count):
        item = selected_bank[i % len(selected_bank)].copy()
        item['source_chapter'] = topic or item['source_chapter']
        results.append(item)
    return results
