from health_ai.eleven import eleven_client


async def text_to_speech(voice_id: str, text: str) -> bytes:
    audio = b""

    async for audio_chunk in eleven_client.text_to_speech.convert(
        voice_id=voice_id, text=text
    ):
        audio += audio_chunk

    return audio