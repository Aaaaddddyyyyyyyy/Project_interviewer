from langgraph.graph import StateGraph, START, END

from graph.state import InterviewState
from agents.evaluator import evaluate_answer
from agents.history import save_history
from db.checkpointer import checkpointer


def build_evaluation_graph():

    builder = StateGraph(InterviewState)

    builder.add_node("evaluate_answer", evaluate_answer)
    builder.add_node("save_history", save_history)

    builder.add_edge(START, "evaluate_answer")
    builder.add_edge("evaluate_answer", "save_history")
    builder.add_edge("save_history", END)

    return builder.compile(checkpointer=checkpointer)


evaluation_graph = build_evaluation_graph()