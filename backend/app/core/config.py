"""Centralised settings loaded from environment / .env file."""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_path: Path = _REPO_ROOT / "data" / "students.csv"
    db_path: Path = _REPO_ROOT / "data" / "analytics.duckdb"

    # Auth
    secret_key: str = "change-me-in-production-use-a-long-random-string"
    access_token_expire_minutes: int = 60

    # Observability
    otlp_endpoint: str | None = None


settings = Settings()
