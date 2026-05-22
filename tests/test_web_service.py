from __future__ import annotations

import re

from web_parsing_bot.web.service import CODE_ALPHABET, CODE_LENGTH


def test_login_get_renders_form(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<form" in response.data


def test_login_with_valid_credentials_redirects_to_index(client):
    response = client.post(
        "/login",
        data={"username": "tester", "password": "hunter2"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_with_invalid_credentials_returns_401(client):
    response = client.post("/login", data={"username": "tester", "password": "wrong"})
    assert response.status_code == 401


def test_index_redirects_to_login_when_anonymous(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_index_renders_for_authenticated_user(client):
    client.post("/login", data={"username": "tester", "password": "hunter2"})
    response = client.get("/")
    assert response.status_code == 200
    assert b"tester" in response.data
    assert b"generateBtn" in response.data


def test_generate_code_requires_authentication(client):
    response = client.get("/generate_code")
    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}


def test_generate_code_returns_code_with_expected_shape(client):
    client.post("/login", data={"username": "tester", "password": "hunter2"})
    response = client.get("/generate_code")
    assert response.status_code == 200
    payload = response.get_json()
    code = payload["code"]
    assert len(code) == CODE_LENGTH
    assert re.fullmatch(rf"[{re.escape(CODE_ALPHABET)}]+", code)


def test_logout_clears_session(client):
    client.post("/login", data={"username": "tester", "password": "hunter2"})
    client.get("/logout")
    response = client.get("/generate_code")
    assert response.status_code == 401
