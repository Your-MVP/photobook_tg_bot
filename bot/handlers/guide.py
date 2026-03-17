from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import config

router = Router()

HOW_TO_ADD_TO_FAMILY_CHAT_CALLBACK = "how_to_add_to_family_chat"
PUT_PHOTO_HERE_CALLBACK = "put_photo_here"
ADDED_TO_FAMILY_CHAT_CALLBACK = "added_to_family_chat"
ADDED_TO_FAMILY_CHAT2_CALLBACK = "added_to_family_chat2"
ADDED_TO_FAMILY_CHAT3_CALLBACK = "added_to_family_chat3"

add_to_family_chat_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👨‍👩‍👧 Добавить бота в семейный чат",
                callback_data=HOW_TO_ADD_TO_FAMILY_CHAT_CALLBACK
            ),
            # InlineKeyboardButton(
            #     text="📷 Загрузить фото сюда",
            #     callback_data=PUT_PHOTO_HERE_CALLBACK
            # )
        ]
    ]
)

added_to_family_chat_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Дальше",
                callback_data=ADDED_TO_FAMILY_CHAT_CALLBACK
            )
        ]
    ]
)

added_to_family_chat2_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Дальше",
                callback_data=ADDED_TO_FAMILY_CHAT2_CALLBACK
            )
        ]
    ]
)

added_to_family_chat3_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Понятно",
                callback_data=ADDED_TO_FAMILY_CHAT3_CALLBACK
            )
        ]
    ]
)


async def suggest_family_chat(message: Message):
    """Sends a greeting message with instructions to add the bot to a family chat."""

    await message.answer(
        "Теперь давай решим, как удобнее собирать фото для фотокниг.\n"
        "Если у тебя есть семейный чат, я могу автоматически забирать оттуда все новые фото.\n"
        "Периодически буду собирать из них готовые фотокниги и присылать тебе варианты альбомов — ты просто иногда открываешь меня и видишь новые классные книги 💛\n"
        "Если семейного чата нет, просто загружай фото сюда — можно сразу большой пачкой, я сам всё отсортирую и предложу макет фотокниги.",
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
        "Чтобы добавить меня в семейный чат:\n"
        "1️⃣ Открой семейный чат в Telegram.\n"
        "2️⃣ Нажми на название чата → «Добавить участников».\n"
        "3️⃣ Найди @MagicMemory_bot и добавь меня.\n"
        "4️⃣ Разреши доступ к сообщениям и фото.\n"
        "Готово! Теперь вся семья сможет присылать фотографии, а я буду собирать из них общие фотокниги 📚💛"
    )
    await callback.message.answer_video(
        video=video,
        caption=caption,
        reply_markup=added_to_family_chat_kb
    )


@router.callback_query(F.data == ADDED_TO_FAMILY_CHAT_CALLBACK)
async def process_added_to_family_chat(callback: CallbackQuery):
    """Handle callback from the 'Added bot to family chat' button.

    Sends the instructional video with explanatory text in Russian.
    """
    await callback.answer()
    video = FSInputFile(config.VIDEO_ADDED_TO_CHAT_PATH)
    caption = (
        f"Если ты всё сделал(а) по инструкции, чат уже подключён ✅\n"
        f"Теперь я буду автоматически собирать все новые фото из этого чата.\n"
        f"А ещё ты можешь просто загрузить сюда любое количество фотографий с телефона — не нужно их заранее сортировать.\n"
        f"Я сам уберу дубли и размытые кадры, придумаю темы и соберу для тебя от одного до нескольких черновых альбомов. Потом мы вместе доведём их до идеала ✨"
    )
    await callback.message.answer_video(
        video=video,
        caption=caption,
        reply_markup=added_to_family_chat2_kb
    )


@router.callback_query(F.data == ADDED_TO_FAMILY_CHAT2_CALLBACK)
async def process_added_to_family_chat2(callback: CallbackQuery):
    """Handle callback from the 'Added bot to family chat' button.

    Sends the instructional video with explanatory text in Russian.
    """
    await callback.answer()
    photo = FSInputFile(config.IMAGE_ALBUM_PATH)
    caption = (
        f"Чтобы первый альбом появился быстрее, присылай фото не только в семейный чат, но и прямо сюда 📸\n"
        f"Мне нужно минимум 21–30 фотографий, чтобы собрать первую фотокнигу, но можно и целую тысячу — я сам всё отсортирую и выберу лучшие.\n"
        f"Я автоматически соберу снимки из чата и из этого диалога, уберу неудачные кадры и сделаю из них готовый альбом."
    )
    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=added_to_family_chat3_kb
    )


@router.callback_query(F.data == ADDED_TO_FAMILY_CHAT3_CALLBACK)
async def process_added_to_family_chat(callback: CallbackQuery):
    """Handle callback from the 'Added bot to family chat' button.

    Sends the instructional video with explanatory text in Russian.
    """
    await callback.answer()
    video = FSInputFile(config.VIDEO_ALBUM_EXAMPLE_PATH)
    caption = (
        f"Я уже начал работу над твоей фотокнигой 🚀\n"
        f"В следующем сообщении ты получишь свой персональный альбом в электронном виде и сможешь внести правки.\n"
        f"Если у тебя появятся вопросы или пожелания, смело пиши их сюда в чат.\n"
        f"Я могу отвечать с небольшой задержкой, потому что параллельно обрабатываю большие массивы фотографий и подбираю для тебя лучшие варианты альбомов — но я обязательно вернусь с ответом 💌"
    )
    await callback.message.answer_video(
        video=video,
        caption=caption,
    )
