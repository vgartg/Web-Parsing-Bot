"""Minimal Flask service: login form, dashboard, and a code-generation endpoint."""

from __future__ import annotations

import random
import string

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from ..config import WebConfig

CODE_ALPHABET = string.ascii_uppercase + string.digits
CODE_LENGTH = 16


def create_app(config: WebConfig | None = None) -> Flask:
    cfg = config or WebConfig.from_env()
    app = Flask(__name__)
    app.secret_key = cfg.secret_key
    app.config["WEB_USERS"] = {cfg.login: cfg.password}

    @app.route("/")
    def index():
        if "username" in session:
            return render_template("index.html", username=session["username"])
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            users = app.config["WEB_USERS"]
            if users.get(username) == password:
                session["username"] = username
                return redirect(url_for("index"))
            return "Неверные логин или пароль", 401
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for("login"))

    @app.route("/generate_code")
    def generate_code():
        if "username" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        code = "".join(random.choices(CODE_ALPHABET, k=CODE_LENGTH))
        return jsonify({"code": code})

    return app


def main() -> None:
    cfg = WebConfig.from_env()
    app = create_app(cfg)
    app.run(host=cfg.host, port=cfg.port, debug=cfg.debug)


if __name__ == "__main__":
    main()
