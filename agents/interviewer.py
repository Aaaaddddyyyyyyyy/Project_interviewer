from graph.state import InterviewState
from services.llm import llm


def generate_question(state: InterviewState):

    role = state.get("role", "Software Engineer")
    difficulty = state.get("difficulty", "Medium")
    interview_type = state.get(
        "interview_type",
        "Technical"
    )

    prompt = f"""
You are a professional technical interviewer.

Candidate Role:
{role}

Interview Type:
{interview_type}

Difficulty:
{difficulty}

Current Round:
{state.get("round", 1)}

Previous Question:
{state.get("question", "")}

Previous Candidate Answer:
{state.get("answer", "")}

Previous Feedback:
{state.get("feedback", "")}

Generate ONE interview question.

Rules:

1. The question must be relevant to the candidate role.
2. Follow the requested interview type.
3. Match the requested difficulty.
4. Adapt the next question based on the previous answer.
5. Ask exactly ONE question.
6. Do not provide the answer.
7. Do not explain the question.

Return ONLY the interview question.
"""

    response = llm.invoke(prompt)

    return {
        "question": response.content
    }