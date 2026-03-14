from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import config

router = Router()

HOW_TO_ADD_TO_FAMILY_CHAT_CALLBACK = "how_to_add_to_family_chat"
ADDED_TO_FAMILY_CHAT_CALLBACK = "added_to_family_chat"
ADDED_TO_FAMILY_CHAT2_CALLBACK = "added_to_family_chat2"
ADDED_TO_FAMILY_CHAT3_CALLBACK = "added_to_family_chat3"

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
        f"Если вы все сделали по инструкции, то ваш чат уже добавлен в нашего бота и ИИ начнет с этого момента собирать все появляющиеся фото в добавленном вами чате.\n"
        f"Выберите и загрузите любое количество фотографий с телефона (не сортируя).\n"
        f"Я их отсортирую сам, уберу дубли, а также фото с плохим качеством, придумаю темы альбомов и соберу для вас от 1 до нескольких альбомов, а потом помогу внести правки в него."
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
        f"Чтобы ускорить процесс создания и получения первого альбома вы можете прислать в ваш семейный чат дополнительные фото.\n\n"
        f"Как только соберется достаточно фотографий для создания альбома (обычно от 50-100 штук нужно), мой ИИ сформирует альбом и я пришлю его вам для ознакомления и внесения правок."
        f"Со мной можно общаться и управлять созданием альбомов очень просто - через голосовое/текстовое управление."
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
        f"Я уже начал работу и в следующем сообщении вы уже получите ваш персонализированный фотоальбом в электронном виде и сможете внести в него дополнительно правки.\n"
        f"Также вы можете писать в чат сюда любые ваши вопросы и хотя я пока не умею автоматически отвечать на сообщения (функция в процессе реализации) я учту все ваши комментарии для создания альбомов. "
        f"Вы можете, например, заранее сами указать желаемую тему для создания нового альбома или придумать надпись на обложку или же указать на каком человеке мне сделать акцент при выборе фотографий. "
        f"В любом случае, даже без этого, я придумаю и пришлю вам ваш альбом 🚀"
    )
    await callback.message.answer_video(
        video=video,
        caption=caption,
    )
