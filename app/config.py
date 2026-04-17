from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///./taller.db"
    secret_key: str = "change-this-secret-key-in-render-env"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    api_title: str = "Taller Moto API"
    api_version: str = "1.0.0"

settings = Settings()
