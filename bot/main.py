import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.config import Config
from bot.handlers import commands, photos


async def main():
    config = Config()
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    storage = RedisStorage.from_url(config.redis_url)
    dp = Dispatcher(storage=storage)

    dp.include_router(commands.router)
    dp.include_router(photos.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())