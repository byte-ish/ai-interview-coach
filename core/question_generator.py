# core/question_generator.py

import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

def generate_interview_questions(role: str) -> str:
    try:
        logger.info(f"Generating interview questions for role: {role}")

        prompt = PromptTemplate.from_template("""
        You are an AI interview coach. Generate 3 technical interview questions for a candidate applying for the role: {role}
        """)

        chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
        questions = chain.invoke({"role": role})

        logger.info("Interview questions generated successfully.")
        return questions.strip()

    except Exception as e:
        logger.exception("Failed to generate interview questions.")
        raise