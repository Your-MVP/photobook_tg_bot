# bot/storage.py
"""Redis storage layer for user data (photos, forum topics and email).

All keys are prefixed with "user:{user_id}:..." for isolation.
Photos are stored as Telegram file_id (no local files on host).
Email is stored as simple string under user:{user_id}:email.
"""

import redisdl
from redis import asyncio as aioredis
# import redis as sync_redis
import json
from typing import List, Optional

redis = aioredis.from_url("redis://redis:6379/0")

# # Sync client for backup/restore (not used in main async flow)
# redis_sync = sync_redis.from_url("redis://redis:6379/0", decode_responses=True)

async def backup_to_json() -> str:
    """Dump ALL data to a JSON string"""
    json_text = redisdl.dumps(
        host="redis",
        port=6379,
        db=0,
        pretty=True,
        encoding="utf-8"
    )
    return json_text

async def restore_from_json(json_text: str):
    """Restore from JSON string"""
    redisdl.loads(json_text, host="redis", port=6379, db=0)


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


# === Association: User ↔ Forum Topic ===

async def set_user_topic_id(user_id: int, topic_id: int) -> None:
    """Save association between user_id and forum topic_id in Redis with expiration."""
    user_key = f"user:{user_id}:topic_id"
    await redis.set(user_key, str(topic_id), ex=30 * 24 * 60 * 60)
    topic_key = f"topic:{topic_id}:user_id"
    await redis.set(topic_key, str(user_id), ex=30 * 24 * 60 * 60)


async def get_user_topic_id(user_id: int) -> Optional[int]:
    """Get the message_thread_id of the user's forum topic (if created)."""
    key = f"user:{user_id}:topic_id"
    topic_id_bytes = await redis.get(key)
    return int(topic_id_bytes) if topic_id_bytes else None


async def get_user_id_by_topic(topic_id: int) -> Optional[int]:
    """Get user_id associated with a given forum topic_id."""
    topic_key = f"topic:{topic_id}:user_id"
    user_id_bytes = await redis.get(topic_key)
    return int(user_id_bytes) if user_id_bytes else None


# === Association: User ↔ Email ===

async def save_user_email(user_id: int, email: str) -> None:
    """
    Saves the email address for the given user ID in Redis.
    Key format: user:{user_id}:email
    No expiration — email stays forever like photo album.
    """
    key = f"user:{user_id}:email"
    await redis.set(key, email)


async def get_user_email(user_id: int) -> Optional[str]:
    """
    Retrieves the email address for the given user ID from Redis.
    Returns None if the email was not found.
    Key format: user:{user_id}:email
    """
    key = f"user:{user_id}:email"
    email_bytes = await redis.get(key)
    return email_bytes.decode("utf-8") if email_bytes else None