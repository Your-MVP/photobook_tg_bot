# bot/handlers/photos.py
"""Handlers for processing user photos.

Stores only Telegram file_id (no local files on host) and forwards to user's topic.
"""

from aiogram import Router, F
from aiogram.types import Message

from bot.storage import add_photo_to_user, get_user_topic_id
from bot.config import config

router = Router()


@router.message(F.photo)
async def handle_photo(message: Message):
    """Обрабатывает фото: сохраняет file_id и форвардит в персональную тему."""
    await message.answer("Вижу фото. Обрабатываю... 📸")

    user_id = message.from_user.id
    file_id = message.photo[-1].file_id
    await add_photo_to_user(user_id, file_id)
    await message.answer("Фото добавлено в ваш альбом! 📸")

    # Форвардинг в тему супергруппы
    topic_id = await get_user_topic_id(user_id)
    if topic_id is not None and config.SUPERGROUP_CHAT_ID:
        try:
            await message.forward(
                chat_id=config.SUPERGROUP_CHAT_ID,
                message_thread_id=topic_id,
            )
            await message.answer("Фото добавлено для модерации! 📸")
        except Exception as e:
            print(f"[FORWARD ERROR] User {user_id}: {e}")

    await message.answer("Фото обработано! 📸")

@router.message(F.chat.id == -1003727275411)
async def debug_all(message: Message):
    print(f"DEBUG: Получено! Тип: {message.content_type} | Фото: {bool(message.photo)} | От: {message.from_user.id}")
    if message.from_user.id == message.bot.id:
        return  # ignore bot's own messages
    await message.answer("Бот видит это сообщение!") 