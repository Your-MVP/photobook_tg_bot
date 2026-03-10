import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, Update

class CatchAllMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        # Ловим только сообщения (можно расширить на Update, если нужно)
        if isinstance(event, Message):
            logging.info(
                f"CatchAll MIDDLEWARE: Получено! "
                f"Тип: {event.content_type} | "
                f"Фото: {bool(event.photo)} | "
                f"От: {event.from_user.id} | "
                f"Чат: {event.chat.id} | "
                f"Thread: {getattr(event, 'message_thread_id', None)}"
            )
            print(f"TEST CatchAll MIDDLEWARE: {event.content_type} от {event.from_user.id}")

        # Обязательно передаём дальше
        return await handler(event, data)