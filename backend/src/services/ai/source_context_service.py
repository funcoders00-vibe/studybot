import os
from pathlib import Path
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[3] / 'data'
SOURCES_DIR = DATA_DIR / 'sources'
TN_BOOKS_DIR = DATA_DIR / 'tn_books'

_CACHED_CONTEXT = None

def _extract_text_from_pdf(path: Path, max_pages: int = 15) -> str:
    if not path.exists():
        return ""
    try:
        reader = PdfReader(str(path))
        pages_to_read = min(len(reader.pages), max_pages)
        return "\n".join((reader.pages[i].extract_text() or "") for i in range(pages_to_read))
    except Exception as e:
        logger.warning(f"Failed to read PDF {path}: {e}")
        return ""

def load_syllabus_and_pyq_context(topic_keyword: str = "") -> str:
    global _CACHED_CONTEXT
    if _CACHED_CONTEXT is not None:
        return _CACHED_CONTEXT

    pdf_files = [
        SOURCES_DIR / 'tnpsc1 syllabus.pdf',
        SOURCES_DIR / 'TNPSC CCSE Group 1 (General Studies) Official Paper (Held On_ 15 Jun, 2025).pdf',
        SOURCES_DIR / 'TNPSC Group-I 2024 Prelims Official Paper (Held On_ 13 Jul, 2024).pdf',
        SOURCES_DIR / 'TNPSC Group I-B & I-C Prelims Official Paper (Held On_ 12 Jul, 2024).pdf',
    ]

    snippets = []
    for pdf_path in pdf_files:
        if pdf_path.exists():
            text = _extract_text_from_pdf(pdf_path, max_pages=5)
            if text:
                snippets.append(f"--- SOURCE: {pdf_path.name} ---\n{text[:8000]}")

    _CACHED_CONTEXT = "\n\n".join(snippets)[:30000]
    return _CACHED_CONTEXT
