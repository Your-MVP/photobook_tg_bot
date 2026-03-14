# bot/handlers/commands.py
"""Command handlers for the Photobook Bot.

Includes /start with automatic forum topic creation and forwarding of user messages to their topic.
"""


import logging

from aiogram import Dispatcher, Router, F
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated, Message, BufferedInputFile

from bot.handlers.ask_email import ask_email
from bot.handlers.guide import suggest_family_chat
from bot.utils.user_topic import create_user_topic, get_topic_name, get_user_topic_id_safe
from bot.storage import (
    backup_to_json,
    get_user_email,
    get_user_id_by_topic,
    get_user_photos,
    clear_user_photos,
    get_user_topic_id,
)
from bot.utils.get_admin_status import get_admin_status
from bot.utils.pdf_generator import generate_pdf
from bot.config import config

router = Router()

async def say_greeting(message: Message, dispatcher: Dispatcher):
    """Sends a greeting message with instructions to add the bot to a family chat."""

    await message.answer(
        "👋 Привет! Я MagicMemory бот - я собираю фото в красивые фотоальбомы 📚!",
    )

    admin_status = await get_admin_status(message.from_user)

    if admin_status in (1, 2):
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=
                f"Как администратор, вы можете дополнительно использовать следующие команды:\n"
                f"• /info - получить информацию о вашем статусе и теме в супергруппе\n"
                f"• /force_new_topic - принудительно создать новую тему для пользователя (если возникли проблемы с текущей темой)\n"
        )

    email = await get_user_email(message.from_user.id)
    await message.reply(f"Ваш полученный адрес электронной почты: {email}")
    if email is None:
        await ask_email(message, dispatcher)
    else:
        await suggest_family_chat(message)


@router.message(Command("start"))
async def cmd_start(message: Message, dispatcher: Dispatcher):
    """Handle /start: create personal forum topic in supergroup if not exists."""
    logging.info(f"Start command: Получено! Тип: {message.content_type} | Фото: {bool(message.photo)} | От: {message.from_user.id}")
    await get_user_topic_id_safe(message.from_user)
    await say_greeting(message, dispatcher)

@router.message(Command("dump_redis"))
async def cmd_dump_redis(message: Message):
    """Handle /dump_redis: dump all Redis data to JSON."""
    admin_status = await get_admin_status(message.from_user)

    if admin_status in (1, 2):
        json_text = await backup_to_json()
        await message.reply(f"Данные Redis (JSON):\n{json_text}")


@router.message(Command("load_redis"))
async def cmd_load_redis(message: Message):
    """Handle /load_redis: load Redis data from JSON."""
    admin_status = await get_admin_status(message.from_user)

    if admin_status in (1, 2):
        await message.reply(f"Восстановление из JSON пока не реализовано в этом примере.")


@router.message(Command("info"))
async def cmd_info(message: Message):
    """Display helpful information."""
    user = message.from_user
    admin_status = await get_admin_status(user)

    bot = message.bot

    if admin_status in (1, 2):
        reply_text = "Вы являетесь администратором бота и его супергруппы."

        if admin_status == 2:
            reply_text = reply_text + "\nВы также являетесь владельцем супергруппы."
        await bot.send_message(chat_id=user.id, text=f"{get_topic_name(user)}\n{reply_text}")

        topic_id = await get_user_topic_id(user.id)
        if topic_id:
            await bot.send_message(chat_id=user.id, text=f"У вас уже есть тема в супергруппе с ID: {topic_id}")
        else:
            await bot.send_message(chat_id=user.id, text="У вас пока нет темы в супергруппе.")
    else:
        await bot.send_message(chat_id=user.id, text="Вы не являетесь администратором бота.")
        return

    email = await get_user_email(user.id)
    email_info = "Адрес электронной почты не указан. Пожалуйста, используйте команду /start для его ввода."
    if email is not None:
        email_info = f"Ваш адрес электронной почты: {email}"
    await bot.send_message(chat_id=user.id, text=email_info)


@router.message(Command("force_new_topic"))
async def cmd_force_new_topic(message: Message):
    """Force create a new topic for the user."""
    admin_status = await get_admin_status(message.from_user)

    if admin_status in (1, 2):
        topic_id = await get_user_topic_id(message.from_user.id)
        try:
            if topic_id:
                await message.bot.delete_forum_topic(config.SUPERGROUP_CHAT_ID, topic_id)
        except Exception as e:
            logging.warning(f"Не удалось удалить тему для {message.from_user.id}: {e}")
        try:
            topic_id = await create_user_topic(message, "<b>Пересоздание темы для пользователя</b>\n")
        except Exception as e:
            logging.warning(f"Не удалось создать тему для {message.from_user.id}: {e}")
    else:
        await message.reply("Вы не являетесь администратором.")
        return


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
    """Handle the event when the bot is added to a group. Send a greeting and notify admins in user's topic."""

    group_reply = "👋 Привет всем! Я бот, который помогает создавать фотоальбомы."

    chat = event.chat
    chat_id = chat.id
    chat_title = chat.title or "Без названия"
    chat_username = chat.username or "отсутствует"
    group_details += (
        f"\n"
        f"📋 ID: <code>{chat_id}</code>\n"
        f"• Название: {chat_title}\n"
        f"• Username: @{chat_username}\n"
        f"• Тип: {chat.type}\n"
        f"• Время: {event.date}"
    )

    admin_status = await get_admin_status(event.from_user)
    if admin_status in (1, 2):
        chat = event.chat
        chat_id = chat.id
        chat_title = chat.title or "Без названия"
        chat_username = chat.username or "отсутствует"
        group_reply += (
            f"\nДанные группы, куда добавлен бот:\n\n{group_details}"
        )

    await event.bot.send_message(
        chat_id=chat_id,
        text=group_reply,
        parse_mode="HTML"
    )

    topic_id = await get_user_topic_id_safe(event.from_user)
    if topic_id is None:
        return

    try:
        topic_reply = (
            f"Бот был добавлен в группу:\n\n{group_details}"
        )
        await event.bot.send_message(
            chat_id=config.SUPERGROUP_CHAT_ID,
            message_thread_id=topic_id,
            text=topic_reply
        )
    except Exception as e:
        logging.error(f"Ошибка при уведомлении пользователя {event.from_user.id} о добавлении бота в группу: {e}")


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
        logging.error(f"[FORWARD ERROR] User {message.from_user.id}: {e}")


@router.message(F.chat.type != "private", F.chat.id == config.SUPERGROUP_CHAT_ID)
async def forward_from_topic(message: Message):
    """Forward messages from the forum topic back to the user (if still valid)."""
    # await message.answer("Сообщение получено в группе, обрабатываем...")
    if message.from_user.id == message.bot.id:
        return  # ignore bot's own messages

    if message.text and message.text.startswith("/"):
        return  # commands in group are not forwarded

    if message.chat.id == config.SUPERGROUP_CHAT_ID and message.is_topic_message:
        topic_id = message.message_thread_id
        user_id = await get_user_id_by_topic(topic_id)
        if user_id is None:
            await message.answer("Эта тема пользователя уже не актуальна.")
            return
        await message.copy_to(user_id)

