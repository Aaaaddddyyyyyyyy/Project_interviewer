from fastapi import APIRouter, HTTPException, Form
from db.database import get_session
from db.models import Candidate
from api.schemas import RegisterRequest, LoginRequest, TokenResponse
from services.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=TokenResponse,
)
def register(data: RegisterRequest):

    session = get_session()

    try:

        # Check candidate ID
        existing_candidate = (
            session.query(Candidate)
            .filter(
                Candidate.candidate_id == data.candidate_id
            )
            .first()
        )

        if existing_candidate:
            raise HTTPException(
                status_code=400,
                detail="Candidate ID already exists.",
            )

        # Check email
        existing_email = (
            session.query(Candidate)
            .filter(
                Candidate.email == data.email
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered.",
            )

        # Hash password
        password_hash_value = hash_password(
            data.password
        )

        # Create candidate
        candidate = Candidate(
            candidate_id=data.candidate_id,
            email=data.email,
            password_hash=password_hash_value,
        )

        session.add(candidate)
        session.commit()
        session.refresh(candidate)

        # Create JWT
        token = create_access_token(
            candidate.candidate_id
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    finally:
        session.close()


# ============================================================
# JSON LOGIN
# Used by Streamlit/frontend
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(data: LoginRequest):

    session = get_session()

    try:

        candidate = (
            session.query(Candidate)
            .filter(
                Candidate.email == data.email
            )
            .first()
        )

        if not candidate:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        if not verify_password(
            data.password,
            candidate.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        token = create_access_token(
            candidate.candidate_id
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    finally:
        session.close()


# ============================================================
# OAUTH2 LOGIN
# Used by Swagger / Authorize button
# ============================================================

@router.post(
    "/token",
    response_model=TokenResponse,
)
def token(
    username: str = Form(...),
    password: str = Form(...),
):

    session = get_session()

    try:

        # OAuth2 uses "username".
        # We use the candidate email as username.
        candidate = (
            session.query(Candidate)
            .filter(
                Candidate.email == username
            )
            .first()
        )

        if not candidate:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        if not verify_password(
            password,
            candidate.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        access_token = create_access_token(
            candidate.candidate_id
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    finally:
        session.close()