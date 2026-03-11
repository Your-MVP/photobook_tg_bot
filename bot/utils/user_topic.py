import logging

from aiogram.types import Message, User

from bot.config import config
from bot.storage import get_user_topic_id, set_user_topic_id


def get_topic_name(user: User) -> str:
    """Helper to generate topic name for a user."""
    full_name = user.full_name
    # username_part = f" (@{message.from_user.username})" if message.from_user.username else ""
    username_part = f"@{user.username}" if user.username else ""
    # return f"👤 Пользователь {message.from_user.id}{username_part} — {full_name}"
    return f"👤 {username_part} — {full_name} (id: {user.id})"


async def create_user_topic(user: User, info_text: str) -> int:
    """Create a forum topic for the user in the supergroup and store the topic_id."""
    forum_topic = await user.bot.create_forum_topic(
                chat_id=config.SUPERGROUP_CHAT_ID,
                name=get_topic_name(user)[:128],
            )
    topic_id = forum_topic.message_thread_id
    await set_user_topic_id(user.id, topic_id)

    await user.bot.send_message(
        chat_id=config.SUPERGROUP_CHAT_ID,
        message_thread_id=topic_id,
        text=(
            info_text +
            f"ID: <code>{user.id}</code>\n"
            f"Имя: {user.full_name}\n"
            f"Username: @{user.username or '—'}\n"
            f"ID темы: <code>{topic_id}</code>"
        ),
        parse_mode="HTML",
    )
    return topic_id


async def get_user_topic_id_safe(user: User) -> int:
    """Get user's topic_id if exists, otherwise create one."""
    topic_id = await get_user_topic_id(user.id)
    if topic_id is None:
        try:
            topic_id = await create_user_topic(user, "<b>Новый пользователь запустил бота</b>\n")

        except Exception as e:
            logging.error(f"Не удалось создать тему для {user.id}: {e}")

    return topic_id
