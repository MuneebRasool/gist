"""
Application settings and configuration.
Load environment variables and define app-wide settings.
"""

from typing import List, Optional
from dotenv import load_dotenv,dotenv_values
load_dotenv('.env')
config = dotenv_values('.env')

# Application Constants
APP_NAME = "FastAPI Template"
VERSION = "1.0.0"
API_V1_PREFIX: str = "/api"
ALLOWED_HOSTS: List[str] = ["*"]

ENV: str = config.get("ENV", "development")
DEBUG: bool = config.get("DEBUG", "True").lower() == "true"
DATABASE_URL: str = config.get("DATABASE_URL", "sqlite://db.sqlite3")
SECRET_KEY: str = config.get("SECRET_KEY", "your-super-secret-key-change-it")

# SMTP Configuration
SMTP_USERNAME: Optional[str] = config.get("SMTP_USERNAME")
SMTP_PASSWORD: Optional[str] = config.get("SMTP_PASSWORD")
SMTP_FROM: Optional[str] = config.get("SMTP_FROM")
SMTP_SERVER: Optional[str] = config.get("SMTP_SERVER")
SMTP_PORT: int = int(config.get("SMTP_PORT", "587"))

# Tortoise ORM Config
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["src.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}
