import av
import wave
from pathlib import Path


class AudioRecorder:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame):
        self.frames.append(frame)
        return frame


def save_audio(recorder, output_path: str):

    if recorder is None:
        raise ValueError("Recorder is not available.")

    if not recorder.frames:
        raise ValueError("No audio frames were recorded.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    first_frame = recorder.frames[0]

    sample_rate = first_frame.sample_rate
    channels = len(first_frame.layout.channels)

    pcm_data = b""

    for frame in recorder.frames:
        pcm_data += frame.to_ndarray().tobytes()

    with wave.open(str(output_path), "wb") as wav:

        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)

    return str(output_path)