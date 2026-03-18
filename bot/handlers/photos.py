# bot/handlers/photos.py
"""Handlers for processing user photos.

Stores only Telegram file_id (no local files on host) and forwards to user's topic.
"""

import logging

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import Message

from bot.storage import add_photo_to_user, get_user_topic_id
from bot.config import config
from bot.utils.get_admin_status import get_admin_status
from bot.utils.user_topic import get_user_topic_id_safe

router = Router()


async def common_handle_photo(message: Message, file_id: str):
    """Common logic to handle a photo: save file_id and forward to user's topic."""
    user = None
    topic_id = None

    if message.chat.type == ChatType.PRIVATE:
        user = message.from_user
        topic_id = await get_user_topic_id_safe(message.from_user)

    if message.chat.type != ChatType.PRIVATE:
        chat_id = message.chat.id
        admins = await message.bot.get_chat_administrators(chat_id)

        for admin in admins:

            topic_id = await get_user_topic_id(admin.user.id)
            if topic_id is not None:
                user = admin.user
                break

    if topic_id is not None:
        try:
            # await message.answer("Собираюсь добавить фото в альбом... 📸")
            await add_photo_to_user(user.id, file_id)
            # await message.answer("Фото добавлено в ваш альбом! 📸")

            await message.forward(
                chat_id=config.SUPERGROUP_CHAT_ID,
                message_thread_id=topic_id,
            )
            # await message.answer("Фото добавлено для модерации! 📸")
        except Exception as e:
            logging.error(f"[FORWARD ERROR] User {user.id}: {e}")
        await message.answer("Готово! 📸")
    else:
        await message.answer("Не могу найти вашу фотокнигу в своих записях. Просьба к ответственному отправить мне команду /start тут или мне напрямую и снова отправить фото. 🙏")


@router.message(F.photo)
async def handle_photo(message: Message):
    """Обрабатывает фото: сохраняет file_id и форвардит в персональную тему."""
    await message.answer("Вижу сжатое фото. Добавляю в альбом... 📸")

    await common_handle_photo(message, message.photo[-1].file_id)
    await message.answer("💡Совет: отправляйте фото как документ (файл), без сжатия, чтобы не терять качество фотографии... 👍")


@router.message(F.document, F.document.mime_type.startswith("image/"))
async def handle_document_photo(message: Message):
    """Обработка документов-изображений"""
    logging.info(f"DEBUG: Получено! Тип: {message.content_type} | Фото: {bool(message.photo)} | От: {message.from_user.id}")
    await message.answer("Вижу документ-фото в оригинальном качестве. Добавляю в альбом... 📸")

    await common_handle_photo(message, message.document.file_id)


@router.message()
async def debug_all(message: Message):
    # logging.info("Photobook Bot started successfully")
    logging.info(f"DEBUG: Получено! Тип: {message.content_type} | Фото: {bool(message.photo)} | От: {message.from_user.id}")
    if message.from_user.id == message.bot.id:
        return  # ignore bot's own messages

    admin_status = await get_admin_status(message.from_user)
    if admin_status in (1, 2):
        await message.answer("Бот видит это сообщение!")