from langgraph.types import interrupt
from graph.state import InterviewState


def get_candidate_answer(state: InterviewState):

    answer = interrupt({
        "type": "candidate_answer",
        "question": state["question"],
        "round": state["round"]
    })

    return {
        "answer": answer
    }