# 🧠 AI Interview Coach Agent

A conversational AI agent built with LangChain, LangGraph, and OpenAI — designed to:

- Parse resumes
- Extract candidate roles using LLMs
- Generate tailored technical interview questions
- Offer follow-up questions
- Export sessions as JSON and CSV
- Provide an interactive CLI chat experience
- ✅ Save & retrieve sessions from Redis memory

Great for candidates, recruiters, and developers showcasing AI agent skills!

---

## ✨ Features

- 📄 Upload resume (PDF) and extract role via LLM
- 🧠 Automatically generate 3 technical interview questions
- 🔁 Optionally request a follow-up question
- 💬 Chat interface for mock interviews
- 📊 Save session details as JSON and CSV
- 🧠 Save and resume sessions with Redis
- 🚀 LangGraph-powered modular state machine
- 🪵 Structured logging and graceful error handling

---

## 🏗️ Architecture

```
📄 Resume PDF
   ↓
🔍 Extract Text
   ↓
🧠 Extract Role using LLM
   ↓
❓ Generate Questions
   ↓
🔁 Optional Follow-Up
   ↓
💾 Save JSON & CSV & Redis
```

Components:
- **LangGraph Nodes** for extracting role, generating questions, and follow-ups.
- **StateGraph** from LangGraph to manage flow.
- **ChatOpenAI** used for all LLM logic.
- **CLI** to provide user interface options.
- **Redis** to store and recall sessions

---

## ⚙️ Tech Stack

- Python 3.10+
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- OpenAI GPT-3.5 (via `langchain_openai`)
- PyPDF2 (for parsing PDF resumes)
- dotenv (for environment config)
- logging (for structured logs)
- redis (for memory-based session history)

---

## 💻 Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-repo/ai-interview-coach.git
cd ai-interview-coach

# 2. Create environment (with conda or venv)
conda create -n ai-interview-coach python=3.10 -y
conda activate ai-interview-coach

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key and Redis URL
touch .env

# .env file content:
OPENAI_API_KEY=your-openai-key
REDIS_URL=redis://localhost:6379

# 5. Start Redis server (macOS example)
brew services start redis

# or with Docker:
docker run -d -p 6379:6379 --name redis redis:latest

# 6. Run the app
python -m app.main
```

---

## 🚀 Usage

On running `python -m app.main`, you'll see:

```
🧠 AI Interview Coach – Choose Your Mode

1. Generate questions manually (enter role)
2. Upload resume + chat mode
3. Upload resume + LangGraph flow
```

✅ Follow the prompts, upload a PDF, and let the AI do the rest.

---

## 🧭 Modes

### Option 1 – Manual
- Type a role
- Get tailored questions

### Option 2 – Resume + Chat
- Upload resume
- Extract role → Questions → Enter Chat Mode

### Option 3 – Resume + LangGraph Flow
- Entire flow runs as a LangGraph state machine
- Outputs saved to:
  - `sessions/session_YYYYMMDD_HHMMSS.json`
  - `sessions/interview_sessions.csv`
  - Redis: `session:<session_id>`

---

## 🔄 LangGraph Interview Flow

LangGraph nodes:
1. `extract_role_node` – detects role from resume
2. `generate_questions_node` – uses LLM to create questions
3. `follow_up_node` – asks if user wants a follow-up

```
📄 Resume → 🧠 Extract Role → ❓ Questions → 🔁 Follow-Up → 💾 Save
```

This flow is compiled and invoked through:

```python
graph = build_graph()
final_state = graph.invoke(state)
```

---

## 🛡️ Logging & Exception Handling

All modules implement:

- `try-except` blocks for robustness
- `logger.exception()` for full stack traces
- `logging` formatted for production

Logs include:
- Resumes processed
- Roles extracted
- Questions generated
- Files saved
- Redis memory events

---

## 🗃️ Data Storage

Each LangGraph session saves:

- ✅ `sessions/session_*.json` → Full state dump
- ✅ `sessions/interview_sessions.csv` → Summary table
- ✅ Redis key `session:<ID>` → For session recall

These outputs allow:
- Auditing
- Review by recruiters
- Training datasets
- Resuming past conversations

---

## 💡 Best Practices Used

- Modular, testable code
- CLI-based UX with clear modes
- Structured logs with log levels
- Exception-safe flows
- Separation of concerns (core, services, app)
- Stateless and stateful flow support
- Memory-based persistence

---

## 🔮 Future Enhancements

- 🌐 Wrap with FastAPI and expose REST endpoints
- 📥 Upload multiple resumes via CLI or UI
- 📊 Add dashboard for visualizing session logs
- 📁 Export to PDF format
- 🔐 Add authentication layer for session reuse

---

## 👨‍💻 Built By

This project is part of a learning initiative by [@Ish](https://github.com/ish) to master LangChain, LangGraph, and modern LLM integrations.

Co-piloted by ChatGPT as mentor, debugger, and brainstorming buddy ❤️
