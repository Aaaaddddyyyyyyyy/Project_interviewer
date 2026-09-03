import cv2
import mediapipe as mp


MODEL_PATH = (
    r"E:\ai_inter\models\blaze_face_short_range.tflite"
)


def analyze_video(video_path: str) -> dict:

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(
            f"Could not open video file: {video_path}"
        )

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    if fps <= 0:
        fps = 30.0

    from mediapipe.tasks.python import BaseOptions

    from mediapipe.tasks.python.vision import (
        FaceDetector,
        FaceDetectorOptions,
        RunningMode,
    )

    options = FaceDetectorOptions(
        base_options=BaseOptions(
            model_asset_path=MODEL_PATH
        ),
        running_mode=RunningMode.IMAGE,
        min_detection_confidence=0.5,
    )

    detector = FaceDetector.create_from_options(
        options
    )

    analyzed_frames = 0
    face_detected_frames = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        analyzed_frames += 1

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame,
        )

        results = detector.detect(
            mp_image
        )

        if results.detections:
            face_detected_frames += 1

    cap.release()
    detector.close()

    # ------------------------------------------------------------
    # IMPORTANT:
    # FLV metadata reports an invalid frame count/duration.
    # Therefore calculate duration from successfully decoded frames.
    # ------------------------------------------------------------

    if analyzed_frames > 0 and fps > 0:
        duration = analyzed_frames / fps
    else:
        duration = 0.0

    if analyzed_frames > 0:
        face_visibility = (
            face_detected_frames
            / analyzed_frames
        ) * 100
    else:
        face_visibility = 0.0

    return {
        "video_path": video_path,

        "duration_seconds": round(
            duration,
            2
        ),

        "fps": round(
            fps,
            2
        ),

        "frame_count": frame_count,

        "analyzed_frames": analyzed_frames,

        "width": width,

        "height": height,

        "face_detected_frames":
            face_detected_frames,

        "face_visibility_percentage":
            round(
                face_visibility,
                2
            ),
    }