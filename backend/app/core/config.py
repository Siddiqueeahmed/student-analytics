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


settings = Settings()
