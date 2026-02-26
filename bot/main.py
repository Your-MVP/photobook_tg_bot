"""Main entry point for the Photobook Telegram Bot MVP v0.1.0.

Starts the bot with polling using aiogram 3.x (compatible with 3.7+).
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.handlers import router


async def main() -> None:
    """Initialize and start the bot.

    Uses HTML parse mode and starts polling.
    """
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)

    # Optional: drop pending updates on start
    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("✅ Photobook Bot started successfully")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    asyncio.run(main())