from __future__ import annotations

import pytest

from web_parsing_bot.config import BotConfig, ConfigError, WebConfig


def test_bot_config_reads_required_env_vars(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tg-token")
    monkeypatch.setenv("WEB_SERVICE_LOGIN", "tester")
    monkeypatch.setenv("WEB_SERVICE_PASSWORD", "hunter2")
    monkeypatch.delenv("WEB_SERVICE_URL", raising=False)
    monkeypatch.delenv("CHROMEDRIVER_PATH", raising=False)

    config = BotConfig.from_env()

    assert config.telegram_bot_token == "tg-token"
    assert config.web_service_login == "tester"
    assert config.web_service_password == "hunter2"
    assert config.web_service_url == "http://localhost:3000"
    assert config.chromedriver_path is None


def test_bot_config_raises_when_token_missing(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setenv("WEB_SERVICE_LOGIN", "tester")
    monkeypatch.setenv("WEB_SERVICE_PASSWORD", "hunter2")

    with pytest.raises(ConfigError):
        BotConfig.from_env()


def test_web_config_defaults_to_port_3000(monkeypatch):
    monkeypatch.delenv("WEB_SERVICE_PORT", raising=False)
    monkeypatch.delenv("WEB_SERVICE_HOST", raising=False)
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)
    monkeypatch.delenv("FLASK_DEBUG", raising=False)
    monkeypatch.delenv("WEB_SERVICE_LOGIN", raising=False)
    monkeypatch.delenv("WEB_SERVICE_PASSWORD", raising=False)

    config = WebConfig.from_env()

    assert config.port == 3000
    assert config.host == "127.0.0.1"
    assert config.debug is False
    assert config.login == "test_user"
    assert config.password == "test_password"
