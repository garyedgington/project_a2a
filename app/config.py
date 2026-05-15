from __future__ import annotations

from dataclasses import dataclass
import os


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() not in {"0", "false", "no", "off", ""}


@dataclass(frozen=True)
class Settings:
    app_version: str
    log_requests: bool
    formatter_url: str
    formatter_trial_url: str
    schema_checker_url: str
    schema_checker_trial_url: str
    classifier_url: str
    classifier_trial_url: str
    summarizer_url: str
    summarizer_trial_url: str


def get_settings() -> Settings:
    return Settings(
        app_version=os.getenv("A2A_APP_VERSION", "0.1.0"),
        log_requests=_as_bool(os.getenv("A2A_LOG_REQUESTS"), True),
        formatter_url=os.getenv("A2A_FORMATTER_URL", "http://localhost:8000"),
        formatter_trial_url=os.getenv("A2A_FORMATTER_TRIAL_URL", "http://localhost:8000/v1/format/trial"),
        schema_checker_url=os.getenv("A2A_SCHEMA_CHECKER_URL", "https://projectx402-production.up.railway.app"),
        schema_checker_trial_url=os.getenv("A2A_SCHEMA_CHECKER_TRIAL_URL", "https://projectx402-production.up.railway.app/v1/schema-check/trial"),
        classifier_url=os.getenv("A2A_CLASSIFIER_URL", "https://web-production-2d1051.up.railway.app"),
        classifier_trial_url=os.getenv("A2A_CLASSIFIER_TRIAL_URL", "https://web-production-2d1051.up.railway.app/v1/classify/trial"),
        summarizer_url=os.getenv("A2A_SUMMARIZER_URL", "https://project-summarizer-production.up.railway.app"),
        summarizer_trial_url=os.getenv("A2A_SUMMARIZER_TRIAL_URL", "https://project-summarizer-production.up.railway.app/v1/summarize/trial"),
    )
