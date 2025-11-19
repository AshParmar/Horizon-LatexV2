"""
Configuration Management
Load environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """
    Application Settings
    
    TODO: Add your environment variables here
    Contributors should add configuration as needed
    """
    
    # App Settings
    APP_NAME: str = "AI Recruitment Platform"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000"
    ]
    
    # Database (TODO: Configure your database)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./recruitment.db")
    
    # API Keys (TODO: Add your API keys to .env)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    COMPOSIO_API_KEY: str = os.getenv("COMPOSIO_API_KEY", "")
    GOOGLE_GEMINI_API_KEY: str = os.getenv("GOOGLE_GEMINI_API_KEY", "")
    
    # Google OAuth (TODO: Configure OAuth credentials)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    
    # Composio Auth Configs
    AC_GMAIL: str = os.getenv("AC_GMAIL", "")
    AC_GOOGLE_CALENDAR: str = os.getenv("AC_GOOGLE_CALENDAR", "")
    AC_GOOGLE_SHEETS: str = os.getenv("AC_GOOGLE_SHEETS", "")
    
    # File Storage
    UPLOAD_DIR: str = "data/raw"
    PROCESSED_DIR: str = "data/processed"
    LOG_DIR: str = "data/logs"
    
    # Vector Database (TODO: Configure vector store)
    VECTOR_STORE_TYPE: str = os.getenv("VECTOR_STORE_TYPE", "chroma")
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "./data/vectorstore")
    
    # Scoring Thresholds
    MIN_SCORE_THRESHOLD: float = 0.5
    LLM_WEIGHT: float = 0.6
    KEYWORD_WEIGHT: float = 0.4
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


# Global settings instance
settings = Settings()
