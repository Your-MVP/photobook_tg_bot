from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states import BookStates
from bot.storage import add_photo_to_user, clear_user_photos, get_user_photos
from bot.utils.pdf_generator import generate_pdf

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(BookStates.creating)
    await message.answer("👋 Добро пожаловать! Присылайте фото для фотокниги. /build — собрать PDF, /clear — очистить.")

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