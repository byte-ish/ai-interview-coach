import os
import json
import csv
import logging
from datetime import datetime
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

InterviewState = dict

# ✅ Logger Setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# 📄 Node: Extract Role from Resume
def extract_role_node(state: InterviewState) -> InterviewState:
    try:
        if "resume_text" not in state:
            raise KeyError("Missing 'resume_text' in state.")
        resume_text = state["resume_text"]

        logger.info("🧠 Extracting role from resume")
        prompt = PromptTemplate.from_template("""
        You are an expert at reading resumes. Extract the job title from this resume:

        {resume_text}

        Just return the job title.
        """)
        chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
        role = chain.invoke({"resume_text": resume_text[:2000]})
        state["role"] = role.strip()
        logger.info(f"🎯 Extracted Role: {state['role']}")
        return state

    except Exception as e:
        logger.exception("❌ Error in extract_role_node")
        raise e

# ❓ Node: Generate Interview Questions
def generate_questions_node(state: InterviewState) -> InterviewState:
    try:
        role = state["role"]
        logger.info(f"🧠 Generating questions for: {role}")
        prompt = PromptTemplate.from_template("""
        You are an AI interview coach. Generate 3 technical interview questions for a candidate applying for the role: {role}
        """)
        chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
        questions = chain.invoke({"role": role})
        state["questions"] = questions
        print(f"\n🧠 Generated Questions:\n{questions}")
        return state

    except Exception as e:
        logger.exception("❌ Error in generate_questions_node")
        raise e

# 🔁 Node: Follow-up Questions
def follow_up_node(state: InterviewState) -> InterviewState:
    try:
        role = state["role"]
        print("\n🤖 Would you like a follow-up question? (y/n)")
        answer = input("👉 ").strip().lower()

        if answer == "y":
            prompt = PromptTemplate.from_template("""
            Based on the role of {role}, generate one tough follow-up interview question.
            """)
            chain = prompt | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
            follow_up = chain.invoke({"role": role})
            state["follow_up"] = follow_up
            print(f"\n🧠 Follow-up Question:\n{follow_up}")
        else:
            print("✅ Interview session complete.")

        return state

    except Exception as e:
        logger.exception("❌ Error in follow_up_node")
        raise e

# 🧠 LangGraph Flow
def build_graph():
    logger.info("⚙️ Building LangGraph flow")
    workflow = StateGraph(InterviewState)

    workflow.add_node("extract_role", extract_role_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("follow_up", follow_up_node)

    workflow.set_entry_point("extract_role")
    workflow.add_edge("extract_role", "generate_questions")
    workflow.add_edge("generate_questions", "follow_up")
    workflow.add_edge("follow_up", END)

    return workflow.compile()

# 💾 Save JSON
def save_session_to_file(state: InterviewState, directory: str = "sessions") -> None:
    try:
        os.makedirs(directory, exist_ok=True)
        state["timestamp"] = datetime.now().isoformat()
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(directory, f"session_{session_id}.json")

        with open(file_path, "w") as f:
            json.dump(state, f, indent=4)

        logger.info(f"💾 JSON saved to {file_path}")
        print(f"\n💾 Session saved to: {file_path}")
    except Exception as e:
        logger.exception("❌ Failed to save session to JSON")
        raise e

# 📄 Save CSV
def save_session_to_csv(state: InterviewState, csv_path: str = "sessions/interview_sessions.csv") -> None:
    try:
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

        row = {
            "timestamp": state.get("timestamp"),
            "role": state.get("role", ""),
            "questions": state.get("questions", "").replace("\n", " "),
            "follow_up": state.get("follow_up", "").replace("\n", " "),
        }

        file_exists = os.path.isfile(csv_path)
        with open(csv_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

        logger.info(f"📄 CSV updated: {csv_path}")
        print(f"📄 CSV updated: {csv_path}")
    except Exception as e:
        logger.exception("❌ Failed to save session to CSV")
        raise e