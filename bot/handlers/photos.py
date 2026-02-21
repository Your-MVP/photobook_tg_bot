from aiogram import Router, F
from aiogram.types import Message
from bot.storage import add_photo_to_user
import aiofiles
import os

router = Router()

@router.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = f"data/{message.from_user.id}/{file.file_unique_id}.jpg"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await message.bot.download_file(file.file_path, file_path)
    add_photo_to_user(message.from_user.id, file_path)
    await message.answer(f"Фото добавлено ({len(get_user_photos(message.from_user.id))} в книге).")