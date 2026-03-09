# bot/handlers/commands.py
"""Command handlers for the Photobook Bot.

Includes /start with automatic forum topic creation and forwarding of user messages to their topic.
"""

from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter, Command
from aiogram.types import CallbackQuery, ChatMemberUpdated, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message, BufferedInputFile
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
        "👋 Привет! Я MagicMemory бот 📸 Я собираю фото в красивые фотоальбомы! Добавь меня в свой семейный чат или отправляй фотографии прямо в этом чате и я буду собирать фото для твоего нового фотоальбома.",
        reply_markup=add_to_family_chat_kb
    )


@router.message(Command("info"))
async def cmd_info(message: Message):
    """Display helpful information."""
    if config.SUPERGROUP_CHAT_ID:
        admins = await message.bot.get_chat_administrators(config.SUPERGROUP_CHAT_ID)
        # owner = None

        for admin in admins:
            if message.from_user.id == admin.user.id:
                reply_text = "Вы являетесь администратором супергруппы."
                full_name = message.from_user.full_name
                username_part = f" (@{message.from_user.username})" if message.from_user.username else ""
                topic_name = f"👤 Пользователь {message.from_user.id}{username_part} — {full_name}"

                if admin.status == ChatMemberStatus.CREATOR:
                    reply_text = reply_text + " Вы также являетесь владельцем супергруппы."
                    # owner = admin
                await message.answer(f"{topic_name}\n{reply_text}")
                return

        await message.answer("Вы не являетесь администратором.")
        return

    await message.answer(
        "Не задано супергруппы для хранения тем. Пожалуйста, обратитесь к администратору бота."
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


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def on_bot_added(event: ChatMemberUpdated):
    """Обработчик добавления бота в группу"""
    chat = event.chat
    chat_id = chat.id
    chat_title = chat.title or "Без названия"
    chat_username = chat.username or "отсутствует"

    # Сообщение для группы
    group_message = (
        f"👋 Привет! Я бот.\n"
        f"📋 ID этой группы: <code>{chat_id}</code>\n\n"
        f"• Название: {chat_title}\n"
        f"• Username: @{chat_username}\n"
        f"• Тип: {chat.type}\n"
        f"• Время: {event.date}"
    )

    await event.bot.send_message(
        chat_id=chat_id,
        text=group_message,
        parse_mode="HTML"
    )


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