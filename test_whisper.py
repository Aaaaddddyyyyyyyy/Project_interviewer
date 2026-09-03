from services.speech_to_text import transcribe_audio


AUDIO_FILE = r"E:\ai_inter\test_audio.wav"


text = transcribe_audio(AUDIO_FILE)

print("\n" + "=" * 60)
print("TRANSCRIPTION")
print("=" * 60)

print(text)

print("=" * 60)