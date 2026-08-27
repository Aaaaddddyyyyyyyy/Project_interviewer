from langgraph.graph import StateGraph, START, END

from graph.state import InterviewState
from agents.interviewer import generate_question
from agents.candidate import get_candidate_answer
from agents.evaluator import evaluate_answer
from agents.reporter import generate_final_report
from graph.router import should_continue
from db.checkpointer import checkpointer


def build_interview_graph():

    builder = StateGraph(InterviewState)

    builder.add_node(
        "generate_question",
        generate_question
    )

    builder.add_node(
        "get_candidate_answer",
        get_candidate_answer
    )

    builder.add_node(
        "evaluate_answer",
        evaluate_answer
    )

    builder.add_node(
        "generate_final_report",
        generate_final_report
    )

    builder.add_edge(
        START,
        "generate_question"
    )

    builder.add_edge(
        "generate_question",
        "get_candidate_answer"
    )

    builder.add_edge(
        "get_candidate_answer",
        "evaluate_answer"
    )

    builder.add_conditional_edges(
        "evaluate_answer",
        should_continue,
        {
            "continue": "generate_question",
            "end": "generate_final_report",
        },
    )

    builder.add_edge(
        "generate_final_report",
        END
    )

    return builder.compile(
        checkpointer=checkpointer
    )


interview_graph = build_interview_graph()