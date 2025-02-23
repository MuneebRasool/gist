"""
Application settings and configuration.
Load environment variables and define app-wide settings.
"""

from typing import List, Optional
from dotenv import load_dotenv,dotenv_values
from neontology import Neo4jConfig

load_dotenv('.env')
config = dotenv_values('.env')

# Application Constants
APP_NAME = "Gist"
VERSION = "1.0.0"
API_V1_PREFIX: str = "/api"
ALLOWED_HOSTS: List[str] = ["*"]

ENV: str = config.get("ENV", "development")
DEBUG: bool = config.get("DEBUG", "True").lower() == "true"
SECRET_KEY: str = config.get("SECRET_KEY", "your-super-secret-key-change-it")

# Database Configuration
DATABASE_URL: str = config.get(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/db_name"
)

# Neo4j Configuration
NEO4J_URI: str = config.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME: str = config.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD: str = config.get("NEO4J_PASSWORD", "password")

# SMTP Configuration
SMTP_USERNAME: Optional[str] = config.get("SMTP_USERNAME")
SMTP_PASSWORD: Optional[str] = config.get("SMTP_PASSWORD")
SMTP_FROM: Optional[str] = config.get("SMTP_FROM")
SMTP_SERVER: Optional[str] = config.get("SMTP_SERVER")
SMTP_PORT: int = int(config.get("SMTP_PORT", "587"))

POSTGRES_USER: str = config.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = config.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB: str = config.get("POSTGRES_DB", "db_name")
POSTGRES_HOST: str = config.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(config.get("POSTGRES_PORT", "5432"))

# Nylas Configuration
NYLAS_CLIENT_ID: Optional[str] = config.get("NYLAS_CLIENT_ID")
NYLAS_API_KEY: Optional[str] = config.get("NYLAS_API_KEY")
NYLAS_API_URI: Optional[str] = config.get("NYLAS_API_URI")
NYLAS_CALLBACK_URI: Optional[str] = config.get("NYLAS_CALLBACK_URI")


# Tortoise ORM Config
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": POSTGRES_DB,
                "host": POSTGRES_HOST,
                "password": POSTGRES_PASSWORD,
                "port": POSTGRES_PORT,
                "user": POSTGRES_USER,
            }
        }
    },
    "apps": {
        "models": {
            "models": ["src.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}


neo4j_config = Neo4jConfig(uri=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)