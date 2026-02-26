"""Configuration settings for the Photobook Telegram Bot MVP v0.1.0.

Loads all settings from the .env file using Pydantic Settings (v2+).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Main bot configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Bot
    BOT_TOKEN: str

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # PostgreSQL
    POSTGRES_USER: str = "photobook"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "photobook"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432


# Global instance (required for imports)
config = Config()