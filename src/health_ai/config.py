from pydantic_settings import BaseSettings


class HeathConfig(BaseSettings):
    openai_api_key: str = ""
    eleven_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


config = HeathConfig()