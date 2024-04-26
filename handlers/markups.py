from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon import *

default_commands = [[cmds.new], [cmds.join, cmds.repeat], [cmds.change_name, cmds.change_lang], [cmds.rules]]

setup_commands = [[cmds.play], [cmds.leave, cmds.show_joined], [cmds.set_money, cmds.set_points]]

# repeat_commands = [[cmds.repeat], [cmds.main_menu]]



def default_markup(lex=lexicon_en) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lex.commands_answers[command]['button_text'],
                                                                       callback_data=str(command))
                                                  for command in row] for row in default_commands])

def langs_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=code, callback_data=code)
                                                 for code in lang_codes]])


def setup_markup(lex=lexicon_en) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lex.commands_answers[command]['button_text'],
                                                                        callback_data=str(command))
                                                  for command in row] for row in setup_commands])


def repeat_markup(game_id, lex=lexicon_en) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lex.commands_answers[cmds.repeat]['button_text'],
                                                                        callback_data=str(cmds.repeat_id).format(game_id))],
                                                 [InlineKeyboardButton(text=lex.commands_answers[cmds.main_menu]['button_text'],
                                                                        callback_data=str(cmds.main_menu))]])
