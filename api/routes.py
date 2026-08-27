from fastapi import APIRouter, HTTPException
from langgraph.types import Command

from graph.interview_graph import interview_graph

from db.database import get_session
from db.models import Candidate, Interview, InterviewAnswer


router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


# ============================================================
# START INTERVIEW
# ============================================================

@router.post("/start")
def start_interview(
    candidate_id: str,
    role: str = "AI Engineer",
    difficulty: str = "Medium",
    interview_type: str = "Technical",
    max_rounds: int = 3,
):

    session = get_session()

    try:

        # ----------------------------------------------------
        # 1. Find or create candidate
        # ----------------------------------------------------

        candidate = (
            session.query(Candidate)
            .filter(
                Candidate.candidate_id == candidate_id
            )
            .first()
        )

        if not candidate:

            candidate = Candidate(
                candidate_id=candidate_id
            )

            session.add(candidate)
            session.commit()

        # ----------------------------------------------------
        # 2. Create a NEW interview
        # ----------------------------------------------------

        interview = Interview(
            candidate_id=candidate_id,
            role=role,
            difficulty=difficulty,
            interview_type=interview_type,
            max_rounds=max_rounds,
            status="in_progress",
        )

        session.add(interview)

        session.commit()

        session.refresh(interview)

        # ----------------------------------------------------
        # 3. IMPORTANT:
        #    Each interview gets its own LangGraph thread
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id": str(interview.id)
            }
        }

        # ----------------------------------------------------
        # 4. Initial LangGraph state
        # ----------------------------------------------------

        initial_state = {

            "question": "",
            "answer": "",
            "feedback": "",
            "history": [],

            "round": 1,
            "max_rounds": max_rounds,

            "role": role,
            "difficulty": difficulty,
            "interview_type": interview_type,

            "final_report": "",
        }

        # ----------------------------------------------------
        # 5. Start LangGraph
        # ----------------------------------------------------

        result = interview_graph.invoke(
            initial_state,
            config=config
        )

        return {

            "candidate_id": candidate_id,

            "interview_id": interview.id,

            "thread_id": str(interview.id),

            "question": result["question"],

            "round": result["round"],

            "role": role,

            "difficulty": difficulty,

            "interview_type": interview_type,

            "max_rounds": max_rounds,
        }

    finally:

        session.close()


# ============================================================
# SUBMIT ANSWER
# ============================================================

@router.post("/answer")
def submit_answer(
    candidate_id: str,
    answer: str,
):

    session = get_session()

    try:

        # ----------------------------------------------------
        # 1. Find latest active interview
        # ----------------------------------------------------

        interview = (
            session.query(Interview)
            .filter(
                Interview.candidate_id == candidate_id,
                Interview.status == "in_progress",
            )
            .order_by(
                Interview.id.desc()
            )
            .first()
        )

        if not interview:

            raise HTTPException(
                status_code=404,
                detail="No active interview found.",
            )

        # ----------------------------------------------------
        # 2. Use interview ID as LangGraph thread ID
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id": str(interview.id)
            }
        }

        # ----------------------------------------------------
        # 3. Resume LangGraph
        # ----------------------------------------------------

        result = interview_graph.invoke(
            Command(resume=answer),
            config=config
        )

        # ----------------------------------------------------
        # 4. Get latest history entry
        # ----------------------------------------------------

        history = result.get(
            "history",
            []
        )

        feedback = ""
        question = ""

        if history:

            latest = history[-1]

            question = latest.get(
                "question",
                ""
            )

            feedback = latest.get(
                "feedback",
                ""
            )

        # ----------------------------------------------------
        # 5. Determine answered round
        # ----------------------------------------------------

        current_round = result.get(
            "round",
            1
        )

        answered_round = max(
            current_round - 1,
            1
        )

        # ----------------------------------------------------
        # 6. Save answer
        # ----------------------------------------------------

        interview_answer = InterviewAnswer(

            interview_id=interview.id,

            round=answered_round,

            question=question,

            answer=answer,

            feedback=feedback,
        )

        session.add(interview_answer)

        # ----------------------------------------------------
        # 7. Check completion
        # ----------------------------------------------------

        max_rounds = result.get(
            "max_rounds",
            interview.max_rounds
        )

        completed = (
            current_round > max_rounds
        )

        if completed:

            interview.status = "completed"

            interview.final_report = (
                result.get(
                    "final_report",
                    ""
                )
            )

            session.commit()

            return {

                "candidate_id":
                    candidate_id,

                "interview_id":
                    interview.id,

                "feedback":
                    feedback,

                "round":
                    current_round,

                "completed":
                    True,

                "final_report":
                    result.get(
                        "final_report",
                        ""
                    ),
            }

        # ----------------------------------------------------
        # 8. Continue interview
        # ----------------------------------------------------

        session.commit()

        return {

            "candidate_id":
                candidate_id,

            "interview_id":
                interview.id,

            "feedback":
                feedback,

            "round":
                current_round,

            "completed":
                False,

            "next_question":
                result.get(
                    "question",
                    ""
                ),
        }

    finally:

        session.close()


# ============================================================
# RESUME INTERVIEW
# ============================================================

@router.get("/resume/{candidate_id}")
def resume_interview(
    candidate_id: str
):

    session = get_session()

    try:

        # ----------------------------------------------------
        # 1. Find latest active interview
        # ----------------------------------------------------

        interview = (
            session.query(Interview)
            .filter(
                Interview.candidate_id == candidate_id,
                Interview.status == "in_progress",
            )
            .order_by(
                Interview.id.desc()
            )
            .first()
        )

        if not interview:

            return {

                "resume_available":
                    False,

                "message":
                    "No active interview found.",
            }

        # ----------------------------------------------------
        # 2. Use interview ID as thread ID
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id": str(interview.id)
            }
        }

        # ----------------------------------------------------
        # 3. Retrieve saved LangGraph state
        # ----------------------------------------------------

        state = interview_graph.get_state(
            config
        )

        if not state.values:

            return {

                "resume_available":
                    False,

                "message":
                    "No saved interview state found.",
            }

        # ----------------------------------------------------
        # 4. Return saved interview information
        # ----------------------------------------------------

        return {

            "resume_available":
                True,

            "interview_id":
                interview.id,

            "thread_id":
                str(interview.id),

            "candidate_id":
                candidate_id,

            "role":
                interview.role,

            "difficulty":
                interview.difficulty,

            "interview_type":
                interview.interview_type,

            "max_rounds":
                interview.max_rounds,

            "round":
                state.values.get(
                    "round"
                ),

            "question":
                state.values.get(
                    "question"
                ),
        }

    finally:

        session.close()


# ============================================================
# ALL INTERVIEW HISTORY
# ============================================================

@router.get("/history/{candidate_id}")
def get_interview_history(
    candidate_id: str
):

    session = get_session()

    try:

        interviews = (
            session.query(Interview)
            .filter(
                Interview.candidate_id == candidate_id
            )
            .order_by(
                Interview.id.desc()
            )
            .all()
        )

        result = []

        for interview in interviews:

            answers = (
                session.query(
                    InterviewAnswer
                )
                .filter(
                    InterviewAnswer.interview_id
                    == interview.id
                )
                .order_by(
                    InterviewAnswer.round
                )
                .all()
            )

            result.append({

                "interview_id":
                    interview.id,

                "candidate_id":
                    interview.candidate_id,

                "role":
                    interview.role,

                "difficulty":
                    interview.difficulty,

                "interview_type":
                    interview.interview_type,

                "max_rounds":
                    interview.max_rounds,

                "status":
                    interview.status,

                "final_report":
                    interview.final_report,

                "created_at":
                    interview.created_at,

                "answers": [

                    {
                        "round":
                            item.round,

                        "question":
                            item.question,

                        "answer":
                            item.answer,

                        "feedback":
                            item.feedback,
                    }

                    for item in answers
                ],
            })

        return {

            "candidate_id":
                candidate_id,

            "interviews":
                result,
        }

    finally:

        session.close()


# ============================================================
# SPECIFIC INTERVIEW
# ============================================================

@router.get(
    "/history/{candidate_id}/{interview_id}"
)
def get_interview(
    candidate_id: str,
    interview_id: int,
):

    session = get_session()

    try:

        interview = (
            session.query(Interview)
            .filter(
                Interview.id == interview_id,
                Interview.candidate_id == candidate_id,
            )
            .first()
        )

        if not interview:

            raise HTTPException(
                status_code=404,
                detail="Interview not found.",
            )

        answers = (
            session.query(
                InterviewAnswer
            )
            .filter(
                InterviewAnswer.interview_id
                == interview.id
            )
            .order_by(
                InterviewAnswer.round
            )
            .all()
        )

        return {

            "interview_id":
                interview.id,

            "candidate_id":
                interview.candidate_id,

            "role":
                interview.role,

            "difficulty":
                interview.difficulty,

            "interview_type":
                interview.interview_type,

            "max_rounds":
                interview.max_rounds,

            "status":
                interview.status,

            "final_report":
                interview.final_report,

            "created_at":
                interview.created_at,

            "answers": [

                {
                    "round":
                        item.round,

                    "question":
                        item.question,

                    "answer":
                        item.answer,

                    "feedback":
                        item.feedback,
                }

                for item in answers
            ],
        }

    finally:

        session.close()

# ============================================================
# CANDIDATE PROFILE
# ============================================================

@router.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: str):

    session = get_session()

    try:

        candidate = (
            session.query(Candidate)
            .filter(
                Candidate.candidate_id == candidate_id
            )
            .first()
        )

        if not candidate:

            raise HTTPException(
                status_code=404,
                detail="Candidate not found.",
            )

        return {
            "id": candidate.id,
            "candidate_id": candidate.candidate_id,
            "created_at": candidate.created_at,
        }

    finally:

        session.close()