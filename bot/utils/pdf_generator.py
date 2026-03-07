# bot/utils/pdf_generator.py
"""PDF generator for Photobook Bot MVP.

Generates PDF on-the-fly from Telegram file_ids using only temporary files in /tmp.
Photos are NEVER saved permanently on the host — only in Telegram.
"""

import img2pdf
import tempfile
from aiogram import Bot
from typing import List


async def generate_pdf(bot: Bot, photo_file_ids: List[str]) -> bytes:
    """Generate PDF bytes from list of Telegram photo file_ids.

    Downloads photos to temporary directory (auto-deleted after generation).
    Zero permanent disk usage for user photos.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_image_paths: List[str] = []
        for idx, file_id in enumerate(photo_file_ids):
            file_info = await bot.get_file(file_id)
            temp_path = f"{tmp_dir}/photo_{idx}.jpg"
            await bot.download_file(file_info.file_path, temp_path)
            temp_image_paths.append(temp_path)

        # img2pdf returns bytes directly
        pdf_bytes: bytes = img2pdf.convert(temp_image_paths)
        return pdf_bytes