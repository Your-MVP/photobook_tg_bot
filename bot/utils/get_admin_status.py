from bot.config import config


from aiogram.enums import ChatMemberStatus
from aiogram.types import User


from typing_extensions import Literal


async def get_admin_status(user: User) -> Literal[2, 1, 0]:
    """Detect if the user is an admin."""
    admins = await user.bot.get_chat_administrators(config.SUPERGROUP_CHAT_ID)

    for admin in admins:
        if user.id == admin.user.id:
            if admin.status == ChatMemberStatus.CREATOR:
                return 2
            return 1

    return 0
