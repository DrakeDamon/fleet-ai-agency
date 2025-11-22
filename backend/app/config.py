from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_SECRET: str
    HUNTER_API_KEY: str
    FMCSA_WEBKEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
