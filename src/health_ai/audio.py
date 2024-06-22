import numpy as np
import pyaudio
from pydub import AudioSegment

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 1500  # Adjust this threshold based on your environment
SILENCE_LIMIT = 1  # Seconds of silence to stop recording

def is_silent(data):
    return np.max(np.abs(np.frombuffer(data, np.int16))) < THRESHOLD

def record_until_silence():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0

    print("Recording...")

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if is_silent(data):
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > int(RATE / CHUNK * SILENCE_LIMIT):
            print("Silence detected, stopping recording.")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    audio_segment = AudioSegment(
        data=b''.join(frames),
        sample_width=pyaudio.get_sample_size(FORMAT),
        frame_rate=RATE,
        channels=CHANNELS
    )

    return audio_segment