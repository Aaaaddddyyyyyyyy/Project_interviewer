from graph.state import InterviewState


def should_continue(state: InterviewState):

    if state["round"] > state["max_rounds"]:
        return "end"

    return "continue"