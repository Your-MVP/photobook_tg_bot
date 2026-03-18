# bot/handlers/commands.py
"""Command handlers for the Photobook Bot.

Includes /start with automatic forum topic creation and forwarding of user messages to their topic.
"""


import logging

from aiogram import Router, F
from aiogram.types import Message

from bot.storage import (
    get_user_topic_id,
)
from bot.config import config

router = Router()

@router.message(F.chat.type == "private", ~F.photo)
async def forward_text_to_topic(message: Message):
    """Forwards text messages from private chats to the user's topic."""
    if message.text and message.text.startswith("/"):
        return  # commands should be handled by separate handlers

    topic_id = await get_user_topic_id(message.from_user.id)
    if topic_id is None or not config.SUPERGROUP_CHAT_ID:
        return
    try:
        await message.forward(
            chat_id=config.SUPERGROUP_CHAT_ID,
            message_thread_id=topic_id,
        )
    except Exception as e:
        logging.error(f"[FORWARD ERROR] User {message.from_user.id}: {e}")

