# services/resume_parser.py

import logging
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def extract_text_from_resume(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)

        if not text.strip():
            raise ValueError("No text extracted from the PDF resume.")

        logger.info(f"✅ Extracted resume text from: {file_path}")
        return text.strip()

    except FileNotFoundError:
        logger.exception(f"❌ Resume file not found: {file_path}")
        raise
    except Exception as e:
        logger.exception("❌ Failed to extract text from resume")
        raise