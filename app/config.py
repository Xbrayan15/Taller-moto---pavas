from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    api_title: str
    api_version: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
