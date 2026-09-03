import uuid
from pathlib import Path

import streamlit as st
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import WebRtcMode, webrtc_streamer


# ============================================================
# CONFIGURATION
# ============================================================

VIDEO_DIR = Path(
    r"E:\ai_inter\interview_recordings"
)

VIDEO_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# VIDEO RECORDER
# ============================================================

def record_interview_video():

    st.markdown("### 📷 Camera Recording")

    st.write(
        "Click START, allow camera access, record your answer, "
        "then click STOP."
    )

    # --------------------------------------------------------
    # Create unique recording ID
    # --------------------------------------------------------

    if "video_recording_id" not in st.session_state:

        st.session_state.video_recording_id = str(
            uuid.uuid4()
        )

    recording_id = (
        st.session_state.video_recording_id
    )

    video_path = (
        VIDEO_DIR /
        f"{recording_id}.flv"
    )

    # --------------------------------------------------------
    # Recorder factory
    # --------------------------------------------------------

    def recorder_factory():

        return MediaRecorder(
            str(video_path),
            format="flv",
        )

    # --------------------------------------------------------
    # WebRTC
    # --------------------------------------------------------

    ctx = webrtc_streamer(
        key="interview-camera",

        mode=WebRtcMode.SENDRECV,

        media_stream_constraints={
            "video": True,
            "audio": False,
        },

        in_recorder_factory=recorder_factory,
    )

    # --------------------------------------------------------
    # Recording status
    # --------------------------------------------------------

    if ctx.state.playing:

        st.success(
            "📷 Camera is recording..."
        )

        st.caption(
            "Keep your face visible during the recording."
        )

    else:

        st.info(
            "Camera is stopped."
        )

    # --------------------------------------------------------
    # Check recording file
    # --------------------------------------------------------

    if video_path.exists():

        file_size = video_path.stat().st_size

        if file_size > 0:

            st.success(
                "🎥 Video recording saved successfully."
            )

            st.caption(
                f"Recording size: "
                f"{file_size / (1024 * 1024):.2f} MB"
            )

            st.session_state.interview_video_path = (
                str(video_path)
            )

        else:

            st.warning(
                "Recording file exists but is empty."
            )

    else:

        if not ctx.state.playing:

            st.caption(
                "No recording file created yet."
            )

    return ctx