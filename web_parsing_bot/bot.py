"""Telegram bot entry point that orchestrates the Selenium parser."""

from __future__ import annotations

import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .config import BotConfig
from .parser import fetch_code

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Используй /get_code для получения секретного кода.")


def _make_get_code_handler(config: BotConfig):
    async def get_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        wait_message = await update.message.reply_text("Запускаю бота для получения кода...")

        loop = asyncio.get_event_loop()
        code = await loop.run_in_executor(None, fetch_code, config)

        await wait_message.delete()

        if code:
            await update.message.reply_text(f"SUCCESS : Ваш код: `{code}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("FAILURE : Не удалось получить код")

    return get_code_command


def build_application(config: BotConfig) -> Application:
    application = Application.builder().token(config.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("get_code", _make_get_code_handler(config)))
    return application


def run() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    config = BotConfig.from_env()
    application = build_application(config)
    application.run_polling()
