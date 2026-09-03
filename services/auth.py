from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pwdlib import PasswordHash

from db.database import get_session
from db.models import Candidate


load_dotenv()


# ============================================================
# PASSWORD HASHING
# ============================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-secret-key",
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60",
    )
)


# ============================================================
# OAUTH2
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(
    candidate_id: str,
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": candidate_id,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# DECODE ACCESS TOKEN
# ============================================================

def decode_access_token(
    token: str,
) -> str | None:

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        candidate_id = payload.get("sub")

        if not candidate_id:
            return None

        return candidate_id

    except JWTError:

        return None


# ============================================================
# CURRENT CANDIDATE
# ============================================================

def get_current_candidate(
    token: str = Depends(oauth2_scheme),
):

    candidate_id = decode_access_token(token)

    if not candidate_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    session = get_session()

    try:

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
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Candidate not found.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        return candidate

    finally:

        session.close()