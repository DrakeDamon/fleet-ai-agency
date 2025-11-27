from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_SECRET: str
    HUNTER_API_KEY: str
    FMCSA_WEBKEY: str | None = None
    
    # Resend
    RESEND_API_KEY: str | None = None
    RESEND_API: str | None = None
    RESEND_AUDIENCE_ID: str | None = None
    
    # Render-specific: PORT is automatically set by Render
    PORT: int = int(os.getenv("PORT", 8000))

    class Config:
        # env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
