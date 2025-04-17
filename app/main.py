# app/main.py

import os
import logging
from dotenv import load_dotenv

from core.question_generator import generate_interview_questions
from core.resume_role_extractor import extract_role_from_text
from core.conversational_chain import create_conversational_chain
from core.langgraph_flow import (
    build_graph,
    InterviewState,
    save_session_to_file,
    save_session_to_csv,
)
from services.resume_parser import extract_text_from_resume
from services.redis_memory import RedisSessionStore

load_dotenv()

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

def generate_questions_flow():
    try:
        print("\nDo you want to (1) Type a role or (2) Upload a resume PDF?")
        choice = input("Enter 1 or 2: ").strip()

        role = ""

        if choice == "1":
            role = input("Enter the job role (e.g., QA Automation Engineer): ").strip()

        elif choice == "2":
            resume_path = input("Enter path to resume PDF (e.g., data/sample_resume.pdf): ").strip()
            if not os.path.exists(resume_path):
                print("❌ File not found. Please check the path.")
                return

            print("\n📄 Extracting text from resume...")
            resume_text = extract_text_from_resume(resume_path)

            print("🔍 Extracting role from resume using LLM...")
            role = extract_role_from_text(resume_text)
            print(f"\n🎯 Detected Role: {role}\n")

        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
            return

        if not role:
            print("❌ Role cannot be empty.")
            return

        print("⏳ Generating interview questions...\n")
        questions = generate_interview_questions(role)
        print("✅ Here are your questions:\n")
        print(questions)

    except Exception as e:
        logger.exception("❌ Error in generate_questions_flow")

def chat_mode():
    try:
        print("\n💬 Entering Interview Chat Mode (type 'exit' to quit)\n")
        chain = create_conversational_chain()

        while True:
            user_input = input("🧑 You: ")
            if user_input.lower() in ("exit", "quit"):
                print("👋 Exiting chat mode.")
                break
            response = chain.run(user_input)
            print(f"🤖 Coach: {response}\n")

    except Exception as e:
        logger.exception("❌ Error in chat_mode")

def run_langgraph_flow(resume_text: str):
    try:
        graph = build_graph()
        state = InterviewState({"resume_text": resume_text})
        logger.info("🧪 Initial state before invoking graph: %s", state)

        final_state = graph.invoke(state)

        save_session_to_file(final_state)
        save_session_to_csv(final_state)

        # ✅ Save to Redis
        store = RedisSessionStore()
        redis_session_id = store.save_session(final_state)
        print(f"🧠 Session saved to Redis with ID: {redis_session_id}")

    except Exception as e:
        logger.exception("❌ Error in run_langgraph_flow")

def main():
    try:
        print("🧠 AI Interview Coach – Choose Your Mode\n")
        print("1. Generate questions manually (enter role)")
        print("2. Upload resume + chat mode")
        print("3. Upload resume + LangGraph flow")

        choice = input("Select an option (1, 2, or 3): ").strip()

        if choice == "1":
            generate_questions_flow()

        elif choice == "2":
            resume_path = input("Enter path to resume PDF (e.g., data/sample_resume.pdf): ").strip()
            if not os.path.exists(resume_path):
                print("❌ File not found. Please check the path.")
                return

            print("\n📄 Extracting text from resume...")
            resume_text = extract_text_from_resume(resume_path)

            print("🔍 Extracting role from resume using LLM...")
            role = extract_role_from_text(resume_text)
            print(f"\n🎯 Detected Role: {role}\n")

            print("⏳ Generating interview questions...\n")
            questions = generate_interview_questions(role)
            print("✅ Here are your questions:\n")
            print(questions)

            use_chat = input("Do you want to start a mock interview chat? (y/n): ").strip().lower()
            if use_chat == "y":
                chat_mode()
            else:
                print("👋 Thank you for using AI Interview Coach!")

        elif choice == "3":
            resume_path = input("Enter path to resume PDF (e.g., data/sample_resume.pdf): ").strip()
            if not os.path.exists(resume_path):
                print("❌ File not found. Please check the path.")
                return

            print("\n📄 Extracting text from resume...")
            resume_text = extract_text_from_resume(resume_path)

            print("🧠 Starting LangGraph-based interview flow...")
            run_langgraph_flow(resume_text)

        else:
            print("❌ Invalid option. Please choose 1, 2, or 3.")

    except Exception as e:
        logger.exception("❌ Fatal error in main()")

if __name__ == "__main__":
    main()