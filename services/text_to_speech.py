from pathlib import Path
import uuid

from gtts import gTTS


AUDIO_DIR = Path(r"E:\ai_inter\generated_audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def text_to_speech(text: str) -> str:

    if not text or not text.strip():
        raise ValueError("Text is required for TTS.")

    filename = f"{uuid.uuid4()}.mp3"
    output_path = AUDIO_DIR / filename

    tts = gTTS(
        text=text.strip(),
        lang="en",
        slow=False,
    )

    tts.save(str(output_path))

    return str(output_path)