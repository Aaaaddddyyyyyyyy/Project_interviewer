from services.text_to_speech import text_to_speech


TEXT = """
You have a dataset with a continuous target variable and several
numeric and categorical features. Describe how you would build,
evaluate, and tune a regression model.
"""


audio_path = text_to_speech(TEXT)

print()
print("=" * 70)
print("TTS TEST")
print("=" * 70)
print(f"Audio generated: {audio_path}")
print("=" * 70)