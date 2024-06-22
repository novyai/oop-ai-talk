import instructor
from openai import AsyncOpenAI

from health_ai.config import config

openai_client = AsyncOpenAI(api_key=config.openai_api_key)
instructor_client = instructor.from_openai(openai_client)
whisper_client = AsyncOpenAI(api_key=config.openai_api_key)
