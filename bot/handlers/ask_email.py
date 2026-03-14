# bot/handlers/ask_email.py
# This file contains the Router with handlers for requesting and validating user's email address using FSM.

from aiogram import Dispatcher, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from bot.handlers.guide import suggest_family_chat
from bot.storage import save_user_email

import re

# Simple regex-based email validation function
def is_valid_email(email: str) -> bool:
    # Basic pattern to check for valid email format (user@domain.tld)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Define FSM states for the email collection process
class EmailForm(StatesGroup):
    # State when the bot is waiting for the user's email input
    waiting_for_email = State()

# Create router for email-related handlers
router = Router()

async def ask_email(message: Message, dispatcher: Dispatcher):
    other_state = await dispatcher.fsm.get_context(
        bot=message.bot,
        chat_id=message.from_user.id,
        user_id=message.from_user.id
    )
    await other_state.set_state(EmailForm.waiting_for_email)
    # Ask the user to provide their email address
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text="Пожалуйста, введите ваш адрес электронной почты."
    )
    # Set the state to wait for email input
    await other_state.set_state(EmailForm.waiting_for_email)

@router.message(EmailForm.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    # Get the trimmed user input
    email = message.text.strip()

    if is_valid_email(email):
        await save_user_email(message.from_user.id, email)
        # Thank the user for the correct email and finish the process
        await message.answer("Спасибо! Ваш адрес электронной почты принят.")
        # Clear the state as the task is completed
        await state.clear()

        await suggest_family_chat(message)  # Suggest adding to family chat after successful email input
    else:
        # Inform the user that the email is incorrect and keep the state active
        await message.answer("Адрес электронной почты введен неправильно. Пожалуйста, попробуйте еще раз.")
        # The state remains "waiting_for_email" so the user can retry immediately