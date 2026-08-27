from pydantic import BaseModel


class CandidateCreate(BaseModel):

    candidate_id: str


class CandidateResponse(BaseModel):

    id: int
    candidate_id: str

    class Config:
        from_attributes = True