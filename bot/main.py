"""Main entry point for the Photobook Telegram Bot MVP v0.1.0.

Starts the bot with polling using aiogram 3.x (compatible with 3.7+).
"""

import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.handlers import router


async def main() -> None:
    """Initialize and start the bot.

    Uses HTML parse mode and starts polling.
    """
    # Startup validation: ensure required static video file exists
    video_path = Path(config.VIDEO_ADD_TO_CHAT_PATH)
    if not video_path.is_file():
        logging.critical(f"Video file not found: {video_path}. "
                         "Please place add_to_family_chat.mp4 in bot/assets/videos/ "
                         "and rebuild the container.")
        raise FileNotFoundError(f"Missing required video file: {video_path}")

    if not config.BOT_TOKEN:
        logging.critical("BOT_TOKEN is not set in the environment. Please set it in the .env file.")
        raise ValueError("Missing BOT_TOKEN in configuration")

    if not config.SUPERGROUP_CHAT_ID:
        logging.critical("SUPERGROUP_CHAT_ID is not set in the environment. Please set it in the .env file.")
        raise ValueError("Missing SUPERGROUP_CHAT_ID in configuration")

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)

    # # Optional: drop pending updates on start
    # await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Photobook Bot: start polling...")
    await dp.start_polling(bot)
    logging.info("Photobook Bot: polling started successfully")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    asyncio.run(main())