"""Allow `python -m web_parsing_bot` to launch the Telegram bot."""

from .bot import run


def main() -> None:
    run()


if __name__ == "__main__":
    main()
