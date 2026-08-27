from graph.state import InterviewState
from services.llm import llm


def evaluate_answer(state: InterviewState):

    question = state["question"]
    answer = state["answer"]

    prompt = f"""
You are a professional technical interviewer.

Evaluate the candidate's answer objectively.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate:

1. Technical correctness
2. Understanding
3. Completeness
4. Clarity

Give a score from 0 to 10.

Return exactly:

Score: <number>/10

Strengths:
<strengths>

Weaknesses:
<weaknesses>

Feedback:
<short constructive feedback>
"""

    response = llm.invoke(prompt)

    current_history = state.get("history", [])

    new_history = current_history + [
        {
            "round": state["round"],
            "question": question,
            "answer": answer,
            "feedback": response.content,
        }
    ]

    return {
        "feedback": response.content,
        "history": new_history,
        "round": state["round"] + 1,
    }