# bot/handlers/commands.py
"""Command handlers for the Photobook Bot.

Includes /start with automatic forum topic creation and forwarding of user messages to their topic.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from bot.states import BookStates
from bot.storage import (
    get_user_photos,
    clear_user_photos,
    get_user_topic_id,
    set_user_topic_id,
)
from bot.utils.pdf_generator import generate_pdf
from bot.config import config

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start: create personal forum topic in supergroup if not exists.

    Надёжная ассоциация: thread_id хранится в Redis по ключу user:{id}:topic_id.
    """
    await state.set_state(BookStates.creating)

    topic_id = await get_user_topic_id(message.from_user.id)

    if topic_id is None and config.SUPERGROUP_CHAT_ID:
        try:
            full_name = message.from_user.full_name
            username_part = f" (@{message.from_user.username})" if message.from_user.username else ""
            topic_name = f"👤 Пользователь {message.from_user.id}{username_part} — {full_name}"

            forum_topic = await message.bot.create_forum_topic(
                chat_id=config.SUPERGROUP_CHAT_ID,
                name=topic_name[:128],
                icon_color=0x2E7D32,
            )
            topic_id = forum_topic.message_thread_id
            await set_user_topic_id(message.from_user.id, topic_id)

            await message.bot.send_message(
                chat_id=config.SUPERGROUP_CHAT_ID,
                message_thread_id=topic_id,
                text=(
                    f"<b>Новый пользователь запустил бота</b>\n"
                    f"ID: <code>{message.from_user.id}</code>\n"
                    f"Имя: {full_name}\n"
                    f"Username: @{message.from_user.username or '—'}"
                ),
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"[WARNING] Не удалось создать тему для {message.from_user.id}: {e}")

    await message.answer(
        "Добро пожаловать в Photobook Bot!\n\n"
        "Присылайте фото для фотокниги. "
        "После загрузки используйте /build для создания PDF или /clear для очистки."
    )


@router.message(Command("build"))
async def cmd_build(message: Message):
    """Build PDF from user's photos (on-the-fly from Telegram file_ids)."""
    photos = await get_user_photos(message.from_user.id)
    if not photos:
        await message.answer("Нет фото для книги.")
        return

    pdf_bytes = await generate_pdf(message.bot, photos)
    await message.answer_document(
        document=BufferedInputFile(pdf_bytes, filename=f"photobook_{message.from_user.id}.pdf"),
        caption="Ваша фотокнига готова! 📖",
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    """Clear user's photo list."""
    await clear_user_photos(message.from_user.id)
    await message.answer("Список фото очищен.")


@router.message(F.chat.type == "private", ~F.photo)
async def forward_text_to_topic(message: Message):
    """Форвардит текстовые сообщения пользователя в его персональную тему."""
    if message.text and message.text.startswith("/"):
        return  # команды обрабатываются отдельными хендлерами

    topic_id = await get_user_topic_id(message.from_user.id)
    if topic_id is None or not config.SUPERGROUP_CHAT_ID:
        return
    try:
        await message.forward(
            chat_id=config.SUPERGROUP_CHAT_ID,
            message_thread_id=topic_id,
        )
    except Exception as e:
        print(f"[FORWARD ERROR] User {message.from_user.id}: {e}")