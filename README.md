# 🧠⚡ AI INTERVIEWER

### *An intelligent, adaptive & stateful AI-powered technical interview platform*

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2500&pause=700&color=00F7FF&center=true&vCenter=true&width=900&lines=AI-Powered+Technical+Interviewer+%F0%9F%A4%96;Adaptive+Interview+Workflows+%F0%9F%A7%A0;LangGraph+%2B+LLM+Agents+%E2%9A%A1;Persistent+Interview+Memory+%F0%9F%92%BE;Real-Time+Candidate+Evaluation+%F0%9F%8E%AF" alt="Typing Animation" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-Agentic%20AI-1C3C3C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/Aaaaddddyyyyyyyy/ai-interviewer?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/github/forks/Aaaaddddyyyyyyyy/ai-interviewer?style=for-the-badge&logo=github" />
  <img src="https://img.shields.io/github/issues/Aaaaddddyyyyyyyy/ai-interviewer?style=for-the-badge" />
  <img src="https://img.shields.io/github/license/Aaaaddddyyyyyyyy/ai-interviewer?style=for-the-badge" />
</p>

---

## 🚀 What is AI Interviewer?

**AI Interviewer** is an intelligent technical interview platform designed to simulate a real-world interview experience using **Large Language Models, LangGraph-based agentic workflows, persistent state, structured evaluation and adaptive questioning**.

Instead of following a simple:

> Question → Answer → Question → Answer

pipeline, the system maintains interview state and dynamically decides what should happen next.

```text
                    👤 CANDIDATE
                         │
                         ▼
                ┌─────────────────┐
                │  INTERVIEW UI   │
                │   Streamlit 🎨   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    FastAPI ⚡    │
                │   Backend API   │
                └────────┬────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │      LangGraph 🧠    │
              │  Agentic Interview   │
              │      Workflow        │
              └──────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     🤖 Question     📊 Evaluation   🧠 Memory
       Agent            Agent          State
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  ┌───────────────┐
                  │  PostgreSQL   │
                  │      💾       │
                  └───────────────┘
```

---

# ✨ Core Features

| Feature                   | Description                                          |
| ------------------------- | ---------------------------------------------------- |
| 🤖 AI Interviewer         | Conducts natural technical interviews                |
| 🧠 Adaptive Questions     | Questions dynamically depend on candidate responses  |
| 🔀 Agentic Workflow       | LangGraph controls interview state and transitions   |
| 💾 Persistent State       | Interview progress can be persisted                  |
| 📊 Candidate Evaluation   | Evaluates answers using structured criteria          |
| 🎯 Difficulty Adaptation  | Interview difficulty can adapt to performance        |
| 🧩 Modular Architecture   | Separate agents/services/components                  |
| ⚡ FastAPI Backend         | REST API layer for application logic                 |
| 🎨 Streamlit UI           | Interactive interview interface                      |
| 🗄️ PostgreSQL            | Persistent relational storage                        |
| 🔐 Environment Secrets    | API keys and credentials kept outside source code    |
| 📝 Structured Outputs     | Machine-readable AI responses                        |
| 🔄 Stateful Conversations | Maintains context throughout an interview            |
| 📈 Interview Analytics    | Designed for storing and analyzing interview results |

---

# 🧠 AI / LLM Techniques Used

This project isn't just an LLM chatbot.

It combines multiple modern **Generative AI + Agentic AI techniques**.

### 🤖 Large Language Models

The LLM acts as the reasoning engine for:

* Question generation
* Answer evaluation
* Follow-up questions
* Candidate feedback
* Interview decisions
* Difficulty adaptation

---

### 🔀 Agentic AI

The system uses an **agentic workflow** rather than a simple linear chain.

The workflow can reason about:

```text
Candidate Answer
      ↓
Evaluate
      ↓
Determine Performance
      ↓
Choose Next Action
      ↓
Generate Next Question
      ↓
Continue Interview
```

---

### 🧠 LangGraph State Machine

LangGraph is used to model the interview as a **stateful graph**.

Example:

```text
              ┌──────────────┐
              │ Start        │
              └──────┬───────┘
                     ↓
            ┌─────────────────┐
            │ Generate        │
            │ Question        │
            └────────┬────────┘
                     ↓
            ┌─────────────────┐
            │ Candidate       │
            │ Answer          │
            └────────┬────────┘
                     ↓
            ┌─────────────────┐
            │ Evaluate Answer │
            └────────┬────────┘
                     ↓
              ┌──────┴───────┐
              │              │
          Strong           Weak
              │              │
              ▼              ▼
       Harder Question   Follow-up
              │              │
              └──────┬───────┘
                     ↓
              Next Interview
```

---

### 💾 Short-Term Memory

The current interview state can contain:

```text
Candidate Profile
Current Question
Candidate Answer
Previous Questions
Previous Evaluations
Current Difficulty
Interview Progress
```

---

### 🧠 Long-Term / Persistent Memory

Interview state can be persisted so that an interview does not necessarily disappear when the application process ends.

This enables:

* Resume interview sessions
* Store candidate history
* Retrieve previous evaluations
* Maintain interview state
* Analyze historical performance

---

### 🎯 Adaptive Interviewing

The interviewer can adjust question difficulty according to candidate performance.

Example:

```text
Excellent Answer
      ↓
Increase Difficulty
      ↓
Advanced Question
```

while:

```text
Weak Answer
      ↓
Ask Clarifying Question
      ↓
Re-test Concept
```

---

### 📊 Structured Evaluation

Instead of asking the LLM for random feedback, the evaluation layer can produce structured information such as:

```text
Technical Accuracy
Concept Understanding
Communication
Problem Solving
Confidence
Completeness
Overall Score
```

This makes the output easier to store, analyze and display.

---

### 🔗 Prompt Engineering

The system uses structured prompts for different responsibilities:

```text
System Prompt
      ↓
Interview Context
      ↓
Candidate Profile
      ↓
Previous Conversation
      ↓
Current Question
      ↓
Candidate Answer
      ↓
LLM
```

Prompt design focuses on:

* Role definition
* Interview constraints
* Question difficulty
* Evaluation criteria
* Output structure
* Context management

---

### 🧩 Context Management

The application manages conversation context rather than repeatedly sending irrelevant information.

This helps reduce:

* Token consumption
* Context noise
* Unnecessary model calls

and improves:

* Response consistency
* Interview continuity
* State management

---

# 🛠️ Technology Stack

## 💻 Programming

<p>
<img src="https://skillicons.dev/icons?i=python" />
</p>

**Python**

Used for:

* Backend
* AI orchestration
* LangGraph workflows
* Database interaction
* API development
* Application logic

---

## 🧠 Generative AI

<p>
<img src="https://skillicons.dev/icons?i=python" />
</p>

### Technologies

* 🧠 Large Language Models
* 🔗 LangChain
* 🔀 LangGraph
* ⚡ Groq / LLM APIs
* 📝 Prompt Engineering
* 📦 Structured Outputs
* 🤖 Agentic Workflows
* 💾 LLM Memory
* 🔄 Stateful AI Applications

---

## ⚡ Backend

<p>
<img src="https://skillicons.dev/icons?i=fastapi,python" />
</p>

### FastAPI

Responsible for:

* REST APIs
* Request validation
* Backend services
* AI workflow execution
* Interview session management

---

## 🎨 Frontend

<p>
<img src="https://skillicons.dev/icons?i=streamlit" />
</p>

### Streamlit

Provides the interactive interface for:

* Candidate interaction
* Interview questions
* Answer submission
* Interview progress
* Evaluation results

---

## 🗄️ Database

<p>
<img src="https://skillicons.dev/icons?i=postgresql" />
</p>

### PostgreSQL

Used for persistent application data such as:

* Candidates
* Interview sessions
* Questions
* Answers
* Evaluations
* Workflow checkpoints

---

## 🐳 DevOps / Infrastructure

<p>
<img src="https://skillicons.dev/icons?i=docker,git,github" />
</p>

Technologies:

* 🐳 Docker
* 🐙 Git
* 🐙 GitHub
* 🖥️ Docker Compose
* 🔐 Environment Variables

---

# 🏗️ System Architecture

```text
                         ┌────────────────────┐
                         │      Candidate     │
                         │         👤         │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │     Streamlit      │
                         │       🎨 UI        │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │      FastAPI       │
                         │       ⚡ API        │
                         └─────────┬──────────┘
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │            LangGraph             │
                  │             🧠                   │
                  │                                  │
                  │  ┌───────────┐ ┌─────────────┐ │
                  │  │ Question  │ │ Evaluation  │ │
                  │  │   Agent   │ │    Agent    │ │
                  │  └─────┬─────┘ └──────┬──────┘ │
                  │        │              │         │
                  │        └──────┬───────┘         │
                  │               │                 │
                  │        ┌──────▼──────┐          │
                  │        │ State /     │          │
                  │        │ Memory      │          │
                  │        └─────────────┘          │
                  └────────────────┬────────────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │    PostgreSQL      │
                         │        💾          │
                         └────────────────────┘
```

---

# 🔄 Interview Workflow

### 1️⃣ Candidate Registration

Candidate information is collected.

```text
Candidate
   ↓
Profile
   ↓
Interview Configuration
```

---

### 2️⃣ Interview Initialization

The AI determines the initial interview context.

```text
Role
Experience
Skills
Difficulty
Interview Type
```

---

### 3️⃣ Question Generation

The LLM generates a question according to:

```text
Role
   +
Candidate Profile
   +
Current Difficulty
   +
Previous Questions
```

---

### 4️⃣ Candidate Answer

Candidate submits an answer.

```text
Question
   ↓
Candidate Answer
```

---

### 5️⃣ Answer Evaluation

The evaluation layer analyzes:

```text
Accuracy
Relevance
Depth
Reasoning
Communication
Completeness
```

---

### 6️⃣ Decision

The workflow determines what happens next.

```text
                    Evaluation
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Excellent       Average       Weak
          │             │             │
          ▼             ▼             ▼
       Harder        Similar       Follow-up
       Question      Difficulty     Question
```

---

### 7️⃣ Final Evaluation

At the end of the interview:

```text
Answers
   ↓
Evaluations
   ↓
Aggregate Performance
   ↓
Final Score
   ↓
Candidate Feedback
```

---

# 📁 Project Structure

```text
ai-interviewer/
│
├── backend/
│   ├── api/
│   ├── agents/
│   ├── services/
│   ├── models/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── db/
│   ├── schema.sql
│   └── ...
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

> 📌 Update this section if your actual directory structure differs.

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Aaaaddddyyyyyyyy/ai-interviewer.git
```

```bash
cd ai-interviewer
```

---

## 2️⃣ Create Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
.env
```

Example:

```env
GROQ_API_KEY=your_api_key_here

DATABASE_URL=your_database_url_here
```

⚠️ **Never commit `.env` to GitHub.**

Use `.env.example` as the public template.

---

# ▶️ Running the Application

## Start Backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
streamlit run frontend/app.py
```

The Streamlit application will open in your browser.

---

# 🧪 Testing

Run:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

---

# 📡 API Architecture

Example API structure:

```text
POST   /candidate
POST   /interview/start
POST   /interview/question
POST   /interview/answer
GET    /interview/{id}
GET    /interview/{id}/result
```

> Update these endpoints according to the final FastAPI implementation.

---

# 🧠 LangGraph Concept

The central idea behind the project is treating an interview as a **stateful graph rather than a simple chatbot conversation**.

Example state:

```python
InterviewState = {
    "candidate": {},
    "current_question": "",
    "current_answer": "",
    "questions": [],
    "evaluations": [],
    "difficulty": "medium",
    "question_number": 1,
    "score": 0,
    "status": "in_progress"
}
```

The graph controls how this state evolves throughout the interview.

---

# 🔥 Engineering Concepts Demonstrated

This project demonstrates practical knowledge of:

### Python

* Object-oriented programming
* Type hints
* Exception handling
* Modular architecture
* Environment configuration
* Async programming

### Generative AI

* LLM integration
* Prompt engineering
* Structured output
* Context management
* AI agents
* Stateful conversations
* Adaptive questioning
* Evaluation pipelines

### LangChain

* Chat models
* Messages
* Prompt templates
* Runnable pipelines
* Structured outputs
* Tool integration

### LangGraph

* Graph-based workflows
* Nodes
* Edges
* Conditional routing
* State management
* Checkpointing
* Persistent workflows
* Human-in-the-loop architecture

### Backend Engineering

* FastAPI
* REST APIs
* Pydantic validation
* API routing
* Service layers
* Dependency management

### Database

* PostgreSQL
* SQL
* Relational schema design
* Persistent state
* Candidate data
* Interview records
* Evaluation storage

### Frontend

* Streamlit
* Session state
* Interactive UI
* API integration

### DevOps

* Git
* GitHub
* Docker
* Docker Compose
* Environment variables

---

# 📊 Evaluation Pipeline

```text
Candidate Answer
       │
       ▼
┌──────────────────┐
│ Answer Analysis  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Technical Score  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Quality Analysis │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Difficulty Logic │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Next Question    │
└──────────────────┘
```

---

# 🔮 Future Improvements

The architecture is designed to support future upgrades such as:

* 🎙️ Voice-based interviews
* 🗣️ Speech-to-text
* 🔊 Text-to-speech
* 👁️ Interview behavior analysis
* 📄 Resume parsing
* 🧠 RAG-based questioning
* 📚 Question-bank retrieval
* 🎯 Personalized interview plans
* 📊 Advanced candidate analytics
* 🏆 Candidate ranking
* 📧 Automated interview reports
* 👨‍💼 Recruiter dashboard
* 🔐 Authentication & authorization
* ☁️ Cloud deployment
* 📦 Production Dockerization
* 📈 Monitoring & observability

---

# 🗺️ Development Roadmap

```text
Foundation
    │
    ├── Python
    ├── FastAPI
    ├── PostgreSQL
    └── Streamlit
         │
         ▼
LLM Integration
    │
    ├── Prompt Engineering
    ├── Structured Outputs
    └── Context Management
         │
         ▼
Agentic AI
    │
    ├── LangChain
    ├── LangGraph
    ├── State Management
    └── Conditional Routing
         │
         ▼
Memory
    │
    ├── Short-Term State
    ├── Checkpointing
    └── Persistent Memory
         │
         ▼
Production
    │
    ├── Testing
    ├── Docker
    ├── Authentication
    ├── Monitoring
    └── Cloud Deployment
```

---

# 📸 Screenshots

Add your application screenshots here:

```text
docs/
├── dashboard.png
├── interview.png
├── evaluation.png
└── architecture.png
```

Then embed them:

```markdown
![Interview Dashboard](docs/dashboard.png)

![AI Interview](docs/interview.png)

![Evaluation](docs/evaluation.png)
```

---

# 🎥 Demo

> 🚧 Demo video coming soon.

Once available:

```markdown
[▶️ Watch AI Interviewer Demo](YOUR_VIDEO_LINK)
```

---

# 🤝 Contributing

Contributions are welcome.

```bash
git clone https://github.com/Aaaaddddyyyyyyyy/ai-interviewer.git
```

Create a feature branch:

```bash
git checkout -b feature/amazing-feature
```

Commit your changes:

```bash
git commit -m "Add amazing feature"
```

Push:

```bash
git push origin feature/amazing-feature
```

Open a Pull Request 🚀

---

# 🔐 Security

Never commit:

```text
.env
API keys
Database passwords
Access tokens
Private credentials
```

The project uses environment variables for sensitive configuration.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Aditya Jha

🎓 B.Tech Computer Science & Engineering — AI/ML

### 🔗 Connect

<p align="center">

<a href="https://github.com/Aaaaddddyyyyyyyy">
<img src="https://img.shields.io/badge/GitHub-Aaaaddddyyyyyyyy-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>

<a href="https://www.linkedin.com/in/aditya-jha-aa211a290/">
<img src="https://img.shields.io/badge/LinkedIn-Aditya%20Jha-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

</p>

---

<p align="center">

### ⭐ If you found this project interesting, consider giving it a star!

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=120&section=footer"/>

</p>

<p align="center">

```text
Built with 🧠 + ⚡ + ☕ + a lot of debugging
```

</p>
