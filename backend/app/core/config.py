# app/core/config.py
from typing import List, Set, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # CORS / Hosts
    ALLOWED_HOSTS: List[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    # Files
    ALLOWED_FILE_TYPES: Set[str] = Field(
        default_factory=lambda: {"image/jpeg", "image/png", "image/gif", "application/pdf"}
    )

    # Integrations
    OPENAI_API_KEY: Optional[str] = None

    # Storage
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"  # override in .env for Postgres

    # Pydantic settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Allow comma-separated strings in .env for list/set fields
    @field_validator("ALLOWED_HOSTS", "CORS_ORIGINS", mode="before")
    @classmethod
    def split_csv_list(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @field_validator("ALLOWED_FILE_TYPES", mode="before")
    @classmethod
    def split_csv_set(cls, v):
        if isinstance(v, (set, list)):
            return set(v)
        if isinstance(v, str):
            return {s.strip() for s in v.split(",") if s.strip()}
        return v


settings = Settings()
