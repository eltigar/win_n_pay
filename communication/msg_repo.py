from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup


async def send_player(bot: Bot, player: str, text: str, keyboard: InlineKeyboardMarkup = None):
    await bot.send_message(player, text, reply_markup=keyboard)

async def send_many_players(bot: Bot, players: list[str], text: str, keyboard: InlineKeyboardMarkup = None):
    for player in players:
        await send_player(bot, player, text, keyboard=keyboard)

async def update_msg_player(bot: Bot, user_id: int, message_id: int, updated_text: str, updated_markup: InlineKeyboardMarkup | None):
    message: Message = await bot.edit_message_text(updated_text, chat_id=user_id, message_id=message_id, reply_markup=updated_markup)


async def update_msg_list(bot: Bot, messages_dict: dict[str, int], updated_text: str, updated_markup):
    for user_id, message_id in messages_dict.items():
        await update_msg_player(bot, int(user_id), message_id, updated_text, updated_markup)
