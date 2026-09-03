import streamlit as st
import queue
import wave
from pathlib import Path

from streamlit_webrtc import webrtc_streamer, WebRtcMode


st.set_page_config(page_title="Microphone Test")

st.title("🎤 Microphone Test")

st.write("Click START, allow the microphone, and speak for 10 seconds.")


ctx = webrtc_streamer(
    key="microphone-test",
    mode=WebRtcMode.SENDONLY,
    media_stream_constraints={
        "video": False,
        "audio": True,
    },
    audio_receiver_size=1024,
)


status = st.empty()


if ctx.state.playing:
    status.success("🎙️ Microphone is recording...")

    if ctx.audio_receiver:

        try:
            frames = ctx.audio_receiver.get_frames(timeout=1)

            status.info(
                f"Received {len(frames)} audio frames."
            )

            if "audio_frames" not in st.session_state:
                st.session_state.audio_frames = []

            st.session_state.audio_frames.extend(frames)

        except queue.Empty:
            status.warning("Waiting for audio frames...")

else:
    status.info("Microphone is stopped.")


st.write("---")

st.write("### Debug")

st.write("Playing:", ctx.state.playing)

frame_count = len(
    st.session_state.get("audio_frames", [])
)

st.write("Stored audio frames:", frame_count)


if st.button("Save Recording"):

    frames = st.session_state.get("audio_frames", [])

    if not frames:

        st.error("No audio frames captured.")

    else:

        output_path = Path(
            r"E:\ai_inter\test_recording.wav"
        )

        first_frame = frames[0]

        sample_rate = first_frame.sample_rate
        channels = len(first_frame.layout.channels)

        pcm_data = b""

        for frame in frames:

            pcm_data += frame.to_ndarray().tobytes()

        with wave.open(
            str(output_path),
            "wb"
        ) as wav_file:

            wav_file.setnchannels(channels)

            wav_file.setsampwidth(
                first_frame.format.bytes
            )

            wav_file.setframerate(
                sample_rate
            )

            wav_file.writeframes(pcm_data)

        st.success(
            f"Audio saved:\n{output_path}"
        )