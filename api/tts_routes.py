from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from services.auth import get_current_candidate
from db.models import Candidate
from services.text_to_speech import text_to_speech


router = APIRouter(
    prefix="/interview",
    tags=["Interview TTS"],
)


@router.post("/tts")
def generate_interview_tts(
    text: str,
    current_candidate: Candidate = Depends(get_current_candidate),
):
    if not text or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text is required.",
        )

    try:
        audio_path = text_to_speech(text)

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename="interview_question.mp3",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"TTS generation failed: {str(e)}",
        )