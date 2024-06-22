import tempfile
from typing import IO, Any

from pydub import AudioSegment

from health_ai.ai import whisper_client


async def transcribe_file(file: IO[Any]):
    transcript = await whisper_client.audio.transcriptions.create(
        file=file,
        language="en",
        temperature=0.0,
        model="whisper-1",
    )

    return transcript


async def transcribe(audio: AudioSegment):
    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
        audio.export(temp_file.name, format="mp3")
        transcript = await transcribe_file(temp_file.file)

    return transcript
