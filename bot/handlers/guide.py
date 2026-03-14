from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import config
from bot.handlers.ask_email import ask_email
from bot.utils.get_admin_status import get_admin_status

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


async def suggest_family_chat(message: Message):
    """Sends a greeting message with instructions to add the bot to a family chat."""

    await message.answer(
        "Теперь ты можешь добавь меня в свой семейный чат или отправляй фотографии мне напрямую и я буду собирать фото для твоей новой фотокниги.",
        reply_markup=add_to_family_chat_kb
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