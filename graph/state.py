from typing import TypedDict


class InterviewState(TypedDict):
    question: str
    answer: str
    feedback: str
    history: list

    round: int
    max_rounds: int

    role: str
    difficulty: str
    interview_type: str

    final_report: str