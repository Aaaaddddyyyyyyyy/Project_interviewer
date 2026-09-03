import queue
import wave
from pathlib import Path

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode


def record_and_transcribe():

    st.markdown("### 🎤 Record Your Answer")

    st.write(
        "Click START, allow microphone access, speak your answer, "
        "then click STOP."
    )

    ctx = webrtc_streamer(
        key="interview-microphone",
        mode=WebRtcMode.SENDONLY,
        media_stream_constraints={
            "video": False,
            "audio": True,
        },
        audio_receiver_size=1024,
    )

    if ctx.state.playing:
        st.success("🎙️ Microphone is recording...")

        if ctx.audio_receiver:

            try:
                frames = ctx.audio_receiver.get_frames(timeout=1)

                if "interview_audio_frames" not in st.session_state:
                    st.session_state.interview_audio_frames = []

                st.session_state.interview_audio_frames.extend(frames)

            except queue.Empty:
                pass

    else:
        st.info("Microphone is stopped.")

    stored_frames = st.session_state.get(
        "interview_audio_frames",
        [],
    )

    st.caption(
        f"Audio frames captured: {len(stored_frames)}"
    )

    if st.button(
        "📝 Convert Speech to Text",
        use_container_width=True,
    ):

        frames = st.session_state.get(
            "interview_audio_frames",
            [],
        )

        if not frames:

            st.error(
                "No audio was captured. "
                "Click START, speak, then click STOP."
            )

            return None

        try:

            output_path = Path(
                "E:/ai_inter/interview_answer.wav"
            )

            first_frame = frames[0]

            sample_rate = first_frame.sample_rate

            channels = len(
                first_frame.layout.channels
            )

            sample_width = (
                first_frame.format.bytes
            )

            pcm_data = b""

            for frame in frames:

                pcm_data += (
                    frame.to_ndarray().tobytes()
                )

            with wave.open(
                str(output_path),
                "wb",
            ) as wav_file:

                wav_file.setnchannels(
                    channels
                )

                wav_file.setsampwidth(
                    sample_width
                )

                wav_file.setframerate(
                    sample_rate
                )

                wav_file.writeframes(
                    pcm_data
                )

            st.success(
                "Audio captured successfully."
            )

            # Import here so Whisper is loaded only
            # when transcription is actually requested.
            from services.speech_to_text import (
                transcribe_audio
            )

            with st.spinner(
                "Transcribing your answer..."
            ):

                transcript = transcribe_audio(
                    str(output_path)
                )

            if not transcript:

                st.warning(
                    "Whisper could not detect any speech."
                )

                return None

            st.session_state.current_answer = (
                transcript
            )

            # Clear frames so the next round starts
            # with a fresh recording.
            st.session_state.interview_audio_frames = []

            st.success(
                "Speech converted to text successfully."
            )

            return transcript

        except Exception as e:

            st.error(
                f"Speech-to-text failed: {e}"
            )

            return None