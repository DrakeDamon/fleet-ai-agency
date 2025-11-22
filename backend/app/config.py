from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_SECRET: str
    HUNTER_API_KEY: str
    FMCSA_WEBKEY: str | None = None
    
    # Render-specific: PORT is automatically set by Render
    PORT: int = int(os.getenv("PORT", 8000))

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
