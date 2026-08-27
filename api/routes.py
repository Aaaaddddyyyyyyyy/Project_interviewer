from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from langgraph.types import Command

from graph.interview_graph import interview_graph

from db.database import get_session
from db.models import (
    Candidate,
    Interview,
    InterviewAnswer,
)

from services.auth import get_current_candidate


router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


# ============================================================
# START INTERVIEW
# ============================================================

@router.post("/start")
def start_interview(
    role: str = "AI Engineer",
    difficulty: str = "Medium",
    interview_type: str = "Technical",
    max_rounds: int = 3,
    current_candidate: str = Depends(
        get_current_candidate
    ),
):

    session = get_session()

    try:

        # JWT determines the candidate identity.
        # The frontend no longer supplies candidate_id.

        candidate_id = current_candidate

        # ----------------------------------------------------
        # Find candidate
        # ----------------------------------------------------

        candidate = (
            session.query(Candidate)
            .filter(
                Candidate.candidate_id
                == candidate_id
            )
            .first()
        )

        if not candidate:

            raise HTTPException(
                status_code=404,
                detail="Candidate not found.",
            )

        # ----------------------------------------------------
        # Create new interview
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
        # Each interview gets its own LangGraph thread
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id": str(interview.id)
            }
        }

        # ----------------------------------------------------
        # Initial LangGraph state
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
        # Start graph
        # ----------------------------------------------------

        result = interview_graph.invoke(
            initial_state,
            config=config,
        )

        return {

            "candidate_id":
                candidate_id,

            "interview_id":
                interview.id,

            "thread_id":
                str(interview.id),

            "question":
                result.get(
                    "question",
                    "",
                ),

            "round":
                result.get(
                    "round",
                    1,
                ),

            "role":
                role,

            "difficulty":
                difficulty,

            "interview_type":
                interview_type,

            "max_rounds":
                max_rounds,
        }

    finally:

        session.close()


# ============================================================
# SUBMIT ANSWER
# ============================================================

@router.post("/answer")
def submit_answer(
    answer: str,
    current_candidate: str = Depends(
        get_current_candidate
    ),
):

    session = get_session()

    try:

        # JWT determines candidate identity.

        candidate_id = current_candidate

        # ----------------------------------------------------
        # Find latest active interview
        # ----------------------------------------------------

        interview = (
            session.query(Interview)
            .filter(
                Interview.candidate_id
                == candidate_id,

                Interview.status
                == "in_progress",
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
        # LangGraph thread
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id":
                    str(interview.id)
            }
        }

        # ----------------------------------------------------
        # Resume graph with candidate answer
        # ----------------------------------------------------

        result = interview_graph.invoke(
            Command(
                resume=answer
            ),
            config=config,
        )

        # ----------------------------------------------------
        # Get history
        # ----------------------------------------------------

        history = result.get(
            "history",
            [],
        )

        feedback = ""
        question = ""

        if history:

            latest = history[-1]

            question = latest.get(
                "question",
                "",
            )

            feedback = latest.get(
                "feedback",
                "",
            )

        # ----------------------------------------------------
        # Current round
        # ----------------------------------------------------

        current_round = result.get(
            "round",
            1,
        )

        answered_round = max(
            current_round - 1,
            1,
        )

        # ----------------------------------------------------
        # Save answer
        # ----------------------------------------------------

        interview_answer = InterviewAnswer(

            interview_id=
                interview.id,

            round=
                answered_round,

            question=
                question,

            answer=
                answer,

            feedback=
                feedback,
        )

        session.add(
            interview_answer
        )

        # ----------------------------------------------------
        # Check completion
        # ----------------------------------------------------

        max_rounds = result.get(
            "max_rounds",
            interview.max_rounds,
        )

        completed = (
            current_round > max_rounds
        )

        if completed:

            interview.status = "completed"

            interview.final_report = (
                result.get(
                    "final_report",
                    "",
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
                        "",
                    ),
            }

        # ----------------------------------------------------
        # Continue interview
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
                    "",
                ),
        }

    finally:

        session.close()


# ============================================================
# RESUME INTERVIEW
# ============================================================

@router.get("/resume/{candidate_id}")
def resume_interview(
    candidate_id: str,
    current_candidate: str = Depends(
        get_current_candidate
    ),
):

    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if candidate_id != current_candidate:

        raise HTTPException(
            status_code=403,
            detail=(
                "You cannot resume another "
                "candidate's interview."
            ),
        )

    session = get_session()

    try:

        # ----------------------------------------------------
        # Find latest active interview
        # ----------------------------------------------------

        interview = (
            session.query(Interview)
            .filter(
                Interview.candidate_id
                == current_candidate,

                Interview.status
                == "in_progress",
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
        # LangGraph thread
        # ----------------------------------------------------

        config = {
            "configurable": {
                "thread_id":
                    str(interview.id)
            }
        }

        # ----------------------------------------------------
        # Retrieve saved state
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
        # Return saved state
        # ----------------------------------------------------

        return {

            "resume_available":
                True,

            "interview_id":
                interview.id,

            "thread_id":
                str(interview.id),

            "candidate_id":
                current_candidate,

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
    candidate_id: str,
    current_candidate: str = Depends(
        get_current_candidate
    ),
):

    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if candidate_id != current_candidate:

        raise HTTPException(
            status_code=403,
            detail=(
                "You cannot access another "
                "candidate's history."
            ),
        )

    session = get_session()

    try:

        interviews = (
            session.query(Interview)
            .filter(
                Interview.candidate_id
                == current_candidate
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
                current_candidate,

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

    current_candidate: str = Depends(
        get_current_candidate
    ),
):

    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if candidate_id != current_candidate:

        raise HTTPException(
            status_code=403,
            detail=(
                "You cannot access another "
                "candidate's interview."
            ),
        )

    session = get_session()

    try:

        interview = (
            session.query(Interview)
            .filter(

                Interview.id
                == interview_id,

                Interview.candidate_id
                == current_candidate,
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
def get_candidate(
    candidate_id: str,

    current_candidate: str = Depends(
        get_current_candidate
    ),
):

    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if candidate_id != current_candidate:

        raise HTTPException(
            status_code=403,
            detail=(
                "You cannot access another "
                "candidate's profile."
            ),
        )

    session = get_session()

    try:

        candidate = (
            session.query(Candidate)
            .filter(
                Candidate.candidate_id
                == current_candidate
            )
            .first()
        )

        if not candidate:

            raise HTTPException(
                status_code=404,
                detail="Candidate not found.",
            )

        return {

            "id":
                candidate.id,

            "candidate_id":
                candidate.candidate_id,

            "email":
                candidate.email,

            "created_at":
                candidate.created_at,
        }

    finally:

        session.close()

