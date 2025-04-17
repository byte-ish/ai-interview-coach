# core/resume_role_extractor.py

import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

def extract_role_from_text(resume_text: str) -> str:
    try:
        logger.info("Extracting role from resume text via LLM.")

        prompt = PromptTemplate.from_template("""
        You are an expert at reading resumes. Extract the job title from this resume:

        {resume_text}

        Just return the job title.
        """)

        chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
        role = chain.invoke({"resume_text": resume_text[:2000]})

        logger.info(f"Role extracted: {role}")
        return role.strip()

    except Exception as e:
        logger.exception("Failed to extract role from resume text.")
        raise