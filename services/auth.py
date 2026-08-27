from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

import os

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-development-secret"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:

    return pwd_context.verify(
        plain_password,
        password_hash,
    )


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


def decode_access_token(
    token: str,
):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )


def get_current_candidate(
    credentials: HTTPAuthorizationCredentials,
):

    token = credentials.credentials

    try:

        payload = decode_access_token(token)

        candidate_id = payload.get("sub")

        if not candidate_id:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
            )

        return candidate_id

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )