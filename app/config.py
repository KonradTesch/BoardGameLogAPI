from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_days: int = 7
    token_renew_after_hours: int = 24

settings = Settings()