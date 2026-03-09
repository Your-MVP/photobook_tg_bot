from aiogram.types import Message


def get_topic_name(message: Message) -> str:
    """Helper to generate topic name for a user."""
    full_name = message.from_user.full_name
    username_part = f" (@{message.from_user.username})" if message.from_user.username else ""
    return f"👤 Пользователь {message.from_user.id}{username_part} — {full_name}"