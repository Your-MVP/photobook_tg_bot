# bot/handlers/photos.py
"""Handlers for processing any unhandled messages that don't match other filters.
"""

import logging

from aiogram import Router
from aiogram.types import Message

from bot.utils.get_admin_status import get_admin_status

router = Router()


@router.message()
async def debug_all(message: Message):
    # logging.info("Photobook Bot started successfully")
    logging.info(f"DEBUG: Got message: {message.content_type} | From: {message.from_user.id} | Chat: {message.chat.id} | Text: {message.text}")
    if message.from_user.id == message.bot.id:
        return  # ignore bot's own messages

    admin_status = await get_admin_status(message.from_user)
    if admin_status in (1, 2):
        await message.answer("Бот видит это сообщение!")