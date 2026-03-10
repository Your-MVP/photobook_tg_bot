import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, Update

class CatchAllMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        # Catch only messages (can be extended to Update if needed)
        if isinstance(event, Message):
            logging.info(
                f"CatchAll MIDDLEWARE: Получено! "
                f"Тип: {event.content_type} | "
                f"Фото: {bool(event.photo)} | "
                f"От: {event.from_user.id} | "
                f"Чат: {event.chat.id} | "
                f"Thread: {getattr(event, 'message_thread_id', None)}"
            )

        return await handler(event, data)