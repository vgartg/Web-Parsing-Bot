"""Flask companion service that issues codes for the Telegram bot to scrape."""

from .service import create_app

__all__ = ["create_app"]
