from __future__ import annotations

import pytest

from web_parsing_bot.config import WebConfig
from web_parsing_bot.web.service import create_app


@pytest.fixture()
def web_config() -> WebConfig:
    return WebConfig(
        secret_key="test-secret",
        login="tester",
        password="hunter2",
        host="127.0.0.1",
        port=3000,
        debug=False,
    )


@pytest.fixture()
def client(web_config: WebConfig):
    app = create_app(web_config)
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client
