# Web-Parsing-Bot

A small pet project I built to practice web parsing end-to-end: a Flask service
hands out one-time codes through a login-gated UI, and a Telegram bot drives a
headless browser to log in, click the button, and read the code back to the
user

[![CI](https://github.com/vgartg/Web-Parsing-Bot/actions/workflows/ci.yml/badge.svg)](https://github.com/vgartg/Web-Parsing-Bot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE.txt)

## Features

- Flask service with login + dashboard + a `/generate_code` endpoint that
  returns a fresh 16-character alphanumeric code
- Telegram bot that runs Chrome headless via Selenium, fills the login form,
  clicks the generate button, and reads the result out of the DOM
- Env-driven configuration: every credential, URL, port, and debug flag lives
  in `.env`
- Pytest suite covering the Flask routes (login, redirects, generate, logout)
- Single CI workflow that lints with ruff and runs the test suite on Python
  3.11 and 3.12

## Project layout

```
.
├── web_parsing_bot/          # Python package — both halves of the project
│   ├── __init__.py
│   ├── __main__.py           # entry point for `python -m web_parsing_bot`
│   ├── bot.py                # Telegram bot wiring (handlers + Application)
│   ├── config.py             # env loading via python-dotenv
│   ├── parser.py             # Selenium routines: log in, click, scrape
│   └── web/
│       ├── service.py        # Flask app factory + routes
│       ├── templates/        # login.html, index.html
│       └── static/           # css + js for the UI
├── bin/                      # convenience launchers (bash + .cmd for Windows)
├── tests/                    # pytest specs for the Flask service and config
├── .env.example              # documented env vars
├── pyproject.toml
├── requirements.txt
└── .github/workflows/ci.yml
```

The bot is the product — the Flask service exists so the bot has something
realistic to parse, and the two halves are deliberately kept in one package so
they share `config.py` and version metadata

## Requirements

- Python 3.11 or newer
- Google Chrome installed locally (Selenium Manager downloads a matching
  chromedriver automatically on first run — see the `CHROMEDRIVER_PATH` env
  var if you prefer a pinned binary)
- A Telegram bot token from `@BotFather`

## Configuration

Copy `.env.example` to `.env` and fill in the values:

| Variable              | Required | Description                                                              |
| --------------------- | -------- | ------------------------------------------------------------------------ |
| `TELEGRAM_BOT_TOKEN`  | yes      | Token issued by `@BotFather` for your bot                                |
| `WEB_SERVICE_LOGIN`   | yes      | Login the bot uses to authenticate against the Flask service             |
| `WEB_SERVICE_PASSWORD`| yes      | Password paired with `WEB_SERVICE_LOGIN`                                 |
| `WEB_SERVICE_URL`     | no       | Base URL of the Flask service (default `http://localhost:3000`)          |
| `WEB_SERVICE_HOST`    | no       | Host the Flask service binds to (default `127.0.0.1`)                    |
| `WEB_SERVICE_PORT`    | no       | Port the Flask service listens on (default `3000`)                       |
| `FLASK_SECRET_KEY`    | no       | Secret key for Flask sessions (default value is for development only)    |
| `FLASK_DEBUG`         | no       | Set to `1` to enable Flask debug mode                                    |
| `CHROMEDRIVER_PATH`   | no       | Path to a chromedriver binary if you don't want Selenium Manager to pick |

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

## Running

Two processes, two terminals — the Flask service first, then the bot:

```bash
# Terminal 1: Flask service on http://localhost:3000
./bin/run-web              # Linux / macOS
bin\run-web.cmd            # Windows

# Terminal 2: Telegram bot (long-polls Telegram and drives Chrome)
./bin/run-bot              # Linux / macOS
bin\run-bot.cmd            # Windows
```

Once both are up, open Telegram and talk to your bot:

| Command     | What it does                                                  |
| ----------- | ------------------------------------------------------------- |
| `/start`    | Prints the welcome message                                    |
| `/get_code` | Launches Chrome, logs into the Flask service, returns a code  |

## Testing

```bash
./bin/test                 # Linux / macOS
bin\test.cmd               # Windows
```

The suite mocks nothing fancy — it uses Flask's built-in test client to hit
every route and asserts on status codes, redirects, and the response payloads

## Linting

```bash
ruff check .
ruff format --check .
```

Ruff is configured in `pyproject.toml` with a 120-character line length and a
small set of pyflakes / pyupgrade / bugbear / isort rules

## Continuous integration

Every push and pull request triggers `.github/workflows/ci.yml`, which runs
`ruff check`, `ruff format --check`, and `pytest` on a matrix of Python 3.11
and 3.12

## Security notes

This is a pet project meant for local experimentation. The default Flask
secret key, the default credentials in `.env.example`, and the open CORS
posture on `/generate_code` are all deliberately permissive. If you point this
at anything that matters, change every default and put the service behind a
real reverse proxy with TLS
