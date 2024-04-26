from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup


async def send_player(bot: Bot, player: str, text: str, keyboard: InlineKeyboardMarkup = None):
    await bot.send_message(player, text, reply_markup=keyboard)

# not in use to support multilangs
async def send_many_players(bot: Bot, players: list[str], text: str, keyboard: InlineKeyboardMarkup = None):
    for player in players:
        await send_player(bot, player, text, keyboard=keyboard)

async def update_msg_player(bot: Bot, user_id: str, message_id: int, updated_text: str, updated_markup: InlineKeyboardMarkup | None):
    message: Message = await bot.edit_message_text(updated_text, chat_id=user_id, message_id=message_id, reply_markup=updated_markup)


# not in use to support multilangs
async def update_msg_list(bot: Bot, messages_dict: dict[str, int], updated_text: str, updated_markup):
    for user_id, message_id in messages_dict.items():
        try:
            await update_msg_player(bot, user_id, message_id, updated_text, updated_markup)
        except TelegramBadRequest:
            await send_player(bot, user_id, updated_text, updated_markup)

# not completed
"""
# Attempts to remove the keyboard from last messages sent by the bot in a specific chat.
async def remove_keyboard(bot: Bot, user_id: str):
    messages = await bot. get_chat_history(user_id, limit=10)
    # Find the last message sent by the bot
    for message in messages:
        if message.from_user and message.from_user.id == bot.id:
            # Attempt to remove the keyboard
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id, reply_markup=None)
            return True


    try:
        # Fetch recent messages from the chat
        messages = await bot.get_chat_history(chat_id, limit=10)
        # Find the last message sent by the bot
        for message in messages:
            if message.from_user and message.from_user.id == bot.id:
                # Attempt to remove the keyboard
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id, reply_markup=None)
                return True
        return False  # No messages from the bot were found in the last few messages
    except (MessageNotModified, MessageToDeleteNotFound):
        # Handling exceptions if the message was not modified or could not be found
        return False
"""
