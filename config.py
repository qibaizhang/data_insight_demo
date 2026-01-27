"""
DataInsight Configuration Management

Loads configuration from environment variables.
Demo version with SQLite database only.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Application configuration"""

    # Base paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    SCHEMA_DIR = DATA_DIR / 'schema'

    # Application settings
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'data-insight-secret-key')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8050))

    # LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')
    MEMORY_MODEL = os.getenv('MEMORY_MODEL')  # Model for memory extraction, defaults to DEFAULT_MODEL
    AVAILABLE_MODELS = [
        m.strip()
        for m in os.getenv('AVAILABLE_MODELS', '').split(',')
        if m.strip()
    ]

    # Database paths
    SESSION_DB_PATH = str(DATA_DIR / 'sessions.db')

    # SQLite Demo Database
    SQLITE_PATH = str(DATA_DIR / 'database.db')

    @classmethod
    def get_available_datasources(cls) -> list[str]:
        """Get list of available data sources"""
        # Demo version only supports SQLite
        return ['sqlite']

    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.SCHEMA_DIR.mkdir(parents=True, exist_ok=True)


# Create config instance
config = Config()

# Ensure directories on import
config.ensure_directories()
