import json
from pathlib import Path
from openai import OpenAI
from pypdf import PdfReader
from src.settings import settings

DATA = Path(__file__).resolve().parents[2] / 'data'
SOURCE_FILES = [
    DATA / 'sources' / 'tnpsc1 syllabus.pdf',
    DATA / 'sources' / 'TNPSC Group-I 2024 Prelims Official Paper (Held On_ 13 Jul, 2024).pdf',
    DATA / 'sources' / 'TNPSC Group I-B & I-C Prelims Official Paper (Held On_ 12 Jul, 2024).pdf',
    DATA / 'sources' / 'TNPSC CCSE Group 1 (General Studies) Official Paper (Held On_ 15 Jun, 2025).pdf',
]

def _extract(path: Path, pages: int = 8) -> str:
    if not path.exists(): return ''
    try:
        reader = PdfReader(str(path))
        return '\n'.join((page.extract_text() or '') for page in reader.pages[:pages])
    except Exception: return ''

def build_context() -> str:
    book_root = DATA / 'tn_books'
    candidates = [path for path in book_root.rglob('*.pdf') if 'polit' in path.name.lower()]
    candidates = (candidates or list(book_root.rglob('*.pdf')))[:3]
    corpus = '\n\n'.join(f'FILE: {path.name}\n{_extract(path)}' for path in [*SOURCE_FILES, *candidates])
    return corpus[:45000]

def generate_indian_polity_questions() -> list[dict]:
    if not settings.nvidia_api_key: raise RuntimeError('NVIDIA_API_KEY is required for generated questions.')
    prompt = f'''Create exactly 10 TNPSC Group 1 Indian Polity MCQs for a 10 minute practice test.
Use only the evidence in this syllabus and prior-paper context. Do not invent citations.
Return JSON only: an array with question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, source_book, source_chapter, source_page.
correct_option must be A, B, C, or D.\n\n{build_context()}'''
    client = OpenAI(base_url='https://integrate.api.nvidia.com/v1', api_key=settings.nvidia_api_key)
    response = client.chat.completions.create(model='nvidia/nemotron-3.5-lightning-30b-a3b', messages=[{'role':'user','content':prompt}], temperature=.2, top_p=.95, max_tokens=8192)
    content = response.choices[0].message.content or '[]'
    if content.startswith('```'): content = content.split('\n', 1)[1].rsplit('```', 1)[0]
    questions = json.loads(content)
    if not isinstance(questions, list) or len(questions) != 10: raise ValueError('Model did not return exactly 10 questions.')
    required = {'question_text','option_a','option_b','option_c','option_d','correct_option','explanation'}
    if not all(required <= set(item) and item['correct_option'] in 'ABCD' for item in questions): raise ValueError('Model returned invalid question data.')
    return questions
