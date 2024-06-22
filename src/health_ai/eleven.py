import httpx
from elevenlabs.client import AsyncElevenLabs

from health_ai.config import config

eleven_client = AsyncElevenLabs(
  api_key=config.eleven_api_key,
  httpx_client=httpx.AsyncClient()
)
