from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from bot.states import BookStates
from bot.storage import add_photo_to_user, clear_user_photos, get_user_photos
from bot.utils.pdf_generator import generate_pdf
from bot.config import config

router = Router()

# Inline keyboard with the required button (appears in /start message)
add_to_family_chat_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить бота в семейный чат",
                callback_data="add_to_family_chat"
            )
        ]
    ]
)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(BookStates.creating)
    await message.answer(
        "Добро пожаловать! Присылайте фото для фотокниги. /build — собрать PDF, /clear — очистить.",
        reply_markup=add_to_family_chat_kb
    )

@router.message(Command("build"))
async def cmd_build(message: Message):
    photos = get_user_photos(message.from_user.id)
    if not photos:
        await message.answer("Нет фото для книги.")
        return
    pdf_path = generate_pdf(message.from_user.id, photos)
    await message.answer_document(document=open(pdf_path, "rb"), caption="Ваша фотокнига готова!")

@router.message(Command("clear"))
async def cmd_clear(message: Message):
    clear_user_photos(message.from_user.id)
    await message.answer("Список фото очищен.")

@router.callback_query(F.data == "add_to_family_chat")
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