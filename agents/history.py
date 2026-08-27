from graph.state import InterviewState


def save_history(state: InterviewState):

    history = state.get("history", [])

    history.append({
        "question": state["question"],
        "answer": state["answer"],
        "feedback": state["feedback"]
    })

    return {
        "history": history
    }