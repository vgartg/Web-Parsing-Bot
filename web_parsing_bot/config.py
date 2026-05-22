"""Environment configuration loaded once at startup."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class ConfigError(RuntimeError):
    """Raised when a required environment variable is missing."""


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ConfigError(f"Environment variable {name} is required")
    return value


@dataclass(frozen=True)
class BotConfig:
    telegram_bot_token: str
    web_service_url: str
    web_service_login: str
    web_service_password: str
    chromedriver_path: str | None

    @classmethod
    def from_env(cls) -> BotConfig:
        return cls(
            telegram_bot_token=_require("TELEGRAM_BOT_TOKEN"),
            web_service_url=os.environ.get("WEB_SERVICE_URL", "http://localhost:3000"),
            web_service_login=_require("WEB_SERVICE_LOGIN"),
            web_service_password=_require("WEB_SERVICE_PASSWORD"),
            chromedriver_path=os.environ.get("CHROMEDRIVER_PATH") or None,
        )


@dataclass(frozen=True)
class WebConfig:
    secret_key: str
    login: str
    password: str
    host: str
    port: int
    debug: bool

    @classmethod
    def from_env(cls) -> WebConfig:
        return cls(
            secret_key=os.environ.get("FLASK_SECRET_KEY", "fallback-secret-key-for-development"),
            login=os.environ.get("WEB_SERVICE_LOGIN", "test_user"),
            password=os.environ.get("WEB_SERVICE_PASSWORD", "test_password"),
            host=os.environ.get("WEB_SERVICE_HOST", "127.0.0.1"),
            port=int(os.environ.get("WEB_SERVICE_PORT", "3000")),
            debug=os.environ.get("FLASK_DEBUG", "0") == "1",
        )
