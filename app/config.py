from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_days: int = 7
    token_renew_after_hours: int = 24
    cookie_secure: bool = False
    cors_origins: list[str] = ["http://localhost:5173"]
    enable_docs: bool = True

settings = Settings()
