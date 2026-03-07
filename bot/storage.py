# bot/storage.py
"""Redis storage layer for user data (photos and forum topics).

All keys are prefixed with "user:{user_id}:..." for isolation.
Photos are stored as Telegram file_id (no local files on host).
"""

from redis import asyncio as aioredis
import json
from typing import List, Optional

redis = aioredis.from_url("redis://redis:6379/0")


async def add_photo_to_user(user_id: int, file_id: str) -> None:
    """Add Telegram photo file_id to user's album (no local storage)."""
    key = f"user:{user_id}:photos"
    photos = await redis.get(key) or b"[]"
    photos_list: List[str] = json.loads(photos)
    photos_list.append(file_id)
    await redis.set(key, json.dumps(photos_list))


async def get_user_photos(user_id: int) -> List[str]:
    """Get list of Telegram photo file_ids for user (async version)."""
    key = f"user:{user_id}:photos"
    photos = await redis.get(key) or b"[]"
    return json.loads(photos)


async def clear_user_photos(user_id: int) -> None:
    """Clear user's photo album."""
    await redis.delete(f"user:{user_id}:photos")


# === Ассоциация пользователя ↔ форум-тема ===

async def get_user_topic_id(user_id: int) -> Optional[int]:
    """Получить message_thread_id темы пользователя (если создана)."""
    key = f"user:{user_id}:topic_id"
    topic_id_bytes = await redis.get(key)
    return int(topic_id_bytes) if topic_id_bytes else None


async def set_user_topic_id(user_id: int, topic_id: int) -> None:
    """Сохранить message_thread_id темы (TTL 30 дней)."""
    key = f"user:{user_id}:topic_id"
    await redis.set(key, str(topic_id), ex=30 * 24 * 60 * 60)