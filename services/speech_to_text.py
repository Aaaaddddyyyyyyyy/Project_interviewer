import whisper


# ============================================================
# LOAD WHISPER MODEL
# ============================================================

MODEL_NAME = "base"

model = whisper.load_model(MODEL_NAME)


# ============================================================
# TRANSCRIBE AUDIO
# ============================================================

def transcribe_audio(audio_path: str) -> str:

    result = model.transcribe(
        audio_path,
        fp16=False,
    )

    return result["text"].strip()