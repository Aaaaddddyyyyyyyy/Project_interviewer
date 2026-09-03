from services.video_analysis import analyze_video


VIDEO_PATH = (
    r"E:\ai_inter\interview_recordings"
    r"\3fff3a7e-57b9-43a7-9268-ae04fa8397f5.flv"
)


result = analyze_video(VIDEO_PATH)


print()
print("=" * 70)
print("VIDEO ANALYSIS RESULT")
print("=" * 70)


for key, value in result.items():
    print(f"{key}: {value}")


print("=" * 70)