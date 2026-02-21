from redis import asyncio as aioredis
import json
import os

redis = aioredis.from_url("redis://redis:6379/0")

async def add_photo_to_user(user_id: int, path: str):
    key = f"user:{user_id}:photos"
    photos = await redis.get(key) or "[]"
    photos_list = json.loads(photos)
    photos_list.append(path)
    await redis.set(key, json.dumps(photos_list))

def get_user_photos(user_id: int):
    # Для простоты синхронный вызов в MVP; в проде — async
    import asyncio
    key = f"user:{user_id}:photos"
    photos = asyncio.run(redis.get(key)) or b"[]"
    return json.loads(photos.decode())

def clear_user_photos(user_id: int):
    asyncio.run(redis.delete(f"user:{user_id}:photos"))