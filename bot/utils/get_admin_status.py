from bot.config import config


from aiogram.enums import ChatMemberStatus
from aiogram.types import Message


from typing_extensions import Literal


async def get_admin_status(message: Message) -> Literal[2, 1, 0, -1]:
    """Detect if the user is an admin."""
    if config.SUPERGROUP_CHAT_ID:
        admins = await message.bot.get_chat_administrators(config.SUPERGROUP_CHAT_ID)

        for admin in admins:
            if message.from_user.id == admin.user.id:
                if admin.status == ChatMemberStatus.CREATOR:
                    return 2
                return 1

        await message.answer("Вы не являетесь администратором.")
        return 0

    await message.answer("Супергруппа для хранения тем не настроена. Пожалуйста, обратитесь к администратору бота.")
    return -1