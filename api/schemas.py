from pydantic import BaseModel


class CandidateCreate(BaseModel):

    candidate_id: str


class CandidateResponse(BaseModel):

    id: int
    candidate_id: str

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):

    candidate_id: str

    email: str

    password: str


class LoginRequest(BaseModel):

    email: str

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str