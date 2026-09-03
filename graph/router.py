from graph.state import InterviewState


def should_continue(state: InterviewState):

    current_round = state.get("round", 1)
    max_rounds = state.get("max_rounds", 5)

    if current_round >= max_rounds:
        return "end"

    return "continue"