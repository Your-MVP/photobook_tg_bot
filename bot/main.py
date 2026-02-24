import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config  # предполагаю, что config здесь импортируется
from bot.handlers import router  # или откуда берутся роутеры/handlers


async def main() -> None:
    # Initialize Bot with default properties
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)  # или dp.include_routers(...) если несколько

    # ... остальной код (если есть skip_updates, etc.)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())