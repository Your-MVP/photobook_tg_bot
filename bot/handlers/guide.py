from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import config
from bot.utils import get_admin_status

router = Router()

HOW_TO_ADD_TO_FAMILY_CHAT_CALLBACK = "how_to_add_to_family_chat"

add_to_family_chat_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Как добавить бота в семейный чат",
                callback_data=HOW_TO_ADD_TO_FAMILY_CHAT_CALLBACK
            )
        ]
    ]
)

async def say_greeting(message: Message):
    """Sends a greeting message with instructions to add the bot to a family chat."""

    await message.answer(
        "👋 Привет! Я MagicMemory бот 📸 Я собираю фото в красивые фотоальбомы! Добавь меня в свой семейный чат или отправляй фотографии прямо в этом чате и я буду собирать фото для твоего нового фотоальбома.",
        reply_markup=add_to_family_chat_kb
    )

    admin_status = await get_admin_status(message.from_user)

    if admin_status in (1, 2):
        await message.answer(
            f"Как администратор, вы можете дополнительно использовать следующие команды:\n"
            f"• /info - получить информацию о вашем статусе и теме в супергруппе\n"
            f"• /force_new_topic - принудительно создать новую тему для пользователя (если возникли проблемы с текущей темой)\n"
        )


@router.callback_query(F.data == HOW_TO_ADD_TO_FAMILY_CHAT_CALLBACK)
async def process_add_to_family_chat(callback: CallbackQuery):
    """Handle callback from the 'Add bot to family chat' button.

    Sends the instructional video with explanatory text in Russian.
    """
    await callback.answer()
    video = FSInputFile(config.VIDEO_ADD_TO_CHAT_PATH)
    caption = (
        "Чтобы добавить бота в семейный чат:\n"
        "1. Откройте семейный чат в Telegram.\n"
        "2. Нажмите на имя чата → «Добавить участников».\n"
        "3. Найдите бота и добавьте его.\n"
        "4. Разрешите доступ к сообщениям и фото.\n\n"
        "Теперь вся семья может присылать фотографии боту для общей фотокниги!"
    )
    await callback.message.answer_video(
        video=video,
        caption=caption
    )