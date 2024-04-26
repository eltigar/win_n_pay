#  setup_handlers
import types
from dataclasses import asdict

from aiogram import Router, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message, CallbackQuery
import models
import data
import models.game_config as cfg
from communication import msg_repo
from handlers.markups import setup_markup, default_markup
from lexicon import *


# Инициализируем роутер уровня модуля
router = Router()

class SetupFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool or dict:
        user_id = str(message.from_user.id)
        user = data.get_user(user_id)
        if user is None or user.setup is None:
            return False
        lex = lang_codes.get(user.lang_code, lang_codes['en'])
        return {'user': user, 'lex': lex}


router.message.filter(SetupFilter())


class SetupCallbackFilter(BaseFilter):
    async def __call__(self, callback_query: CallbackQuery) -> bool or dict:
        user_id = str(callback_query.from_user.id)
        user = data.get_user(user_id)
        if user is None or user.setup is None:
            return False
        lex = lang_codes.get(user.lang_code, lang_codes['en'])
        return {'user': user, 'lex': lex}

router.callback_query.filter(SetupCallbackFilter())

# new and join command are handled in default handlers


async def leave_game(message: Message, user: models.User, lex: types.ModuleType):
    answers_dict = lex.commands_answers[cmds.leave]
    match len(user.setup.player_list):
        case 2:
            user.setup.remove_player(user.id)
            other_user_id = user.setup.player_list[0]
            other_user = data.get_user(other_user_id)
            other_user.setup = user.setup
            user.setup = None  # only resets setup for user

            data.save_user(user)
            data.save_user(other_user)

            await message.answer(answers_dict['2'] + other_user.id, reply_markup=default_markup(lex))
            lex = lang_codes.get(other_user.lang_code, lang_codes['en']) if user else lexicon_en
            await msg_repo.send_player(message.bot, other_user_id, lex.commands_answers[cmds.leave]['2 for other'] + user.name, keyboard=setup_markup(lex))
        case 1:
            user.setup = None
            data.save_user(user)
            await message.answer(answers_dict['1'], reply_markup=default_markup(lex))
        case _:
            raise ValueError('Setup maintenance broken: not 1 or 2 players in list')

@router.message(Command(commands=cmds.leave))
async def leave_game_command(message: Message, user: models.User, lex: types.ModuleType):
    await leave_game(message, user, lex)

@router.callback_query(F.data == cmds.leave)
async def leave_game_callback(callback_query: CallbackQuery, user: models.User, lex: types.ModuleType):
    await callback_query.message.delete_reply_markup()
    await leave_game(callback_query.message, user, lex)


@router.message(Command(commands=cmds.set_points))
async def set_points_command(message: Message, user: models.User, lex: types.ModuleType):
    answers_dict = lex.commands_answers[cmds.set_points]
    points_str = message.text[len('/set_points '):]  # The format is /set_points <points>
    try:
        points = int(points_str)
    except ValueError:
        await message.answer(answers_dict['fail_nan'] + points_str, reply_markup=setup_markup(lex))
    else:
        if cfg.MIN_POINTS <= points <= cfg.MAX_POINTS:
            user.setup.points_to_win = points
            data.save_user(user)
            await msg_repo.send_player(message.bot, user.id,
                                       lex.commands_answers[cmds.set_points]['success'] + points_str,
                                       keyboard=setup_markup(lex))
            for other_user_id in user.setup.player_list:
                if other_user_id != user.id:
                    other_user = data.get_user(other_user_id)
                    other_user.setup = user.setup
                    data.save_user(other_user)
                    lex = lang_codes.get(other_user.lang_code, lang_codes['en']) if user else lexicon_en
                    await msg_repo.send_player(message.bot, other_user.id,
                                               lex.commands_answers[cmds.set_points]['success'] + points_str,
                                               keyboard=setup_markup(lex))
        else:
            await message.answer(answers_dict['fail_value'])


@router.callback_query(F.data == cmds.set_points)
async def set_points_callback(callback_query: CallbackQuery, lex: types.ModuleType):
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(lex.commands_answers[cmds.set_points]['fail_none'])


@router.message(Command(commands=cmds.set_money))
async def set_money_command(message: Message, user: models.User, lex: types.ModuleType):
    answers_dict = lex.commands_answers[cmds.set_money]
    money_str = message.text[len('/set_money '):]  # The format is /set_money <money>
    try:
        money = int(money_str)
    except ValueError:
        await message.answer(answers_dict['fail_nan'] + money_str, reply_markup=setup_markup(lex))
    else:
        if cfg.MIN_MONEY <= money <= cfg.MAX_MONEY:
            user.setup.starting_money = money
            data.save_user(user)
            await msg_repo.send_player(message.bot, user.id,
                                       lex.commands_answers[cmds.set_money]['success'] + money_str,
                                       keyboard=setup_markup(lex))
            for other_user_id in user.setup.player_list:
                if other_user_id != user.id:
                    other_user = data.get_user(other_user_id)
                    other_user.setup = user.setup
                    data.save_user(other_user)
                    lex = lang_codes.get(other_user.lang_code, lang_codes['en']) if user else lexicon_en
                    await msg_repo.send_player(message.bot, other_user.id,
                                               lex.commands_answers[cmds.set_money]['success'] + money_str,
                                               keyboard=setup_markup(lex))

        else:
            await message.answer(answers_dict['fail_value'])

@router.callback_query(F.data == cmds.set_money)
async def set_money_callback(callback_query: CallbackQuery, lex: types.ModuleType):
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(lex.commands_answers[cmds.set_money]['fail_none'])

@router.message(Command(commands=cmds.show_joined))
async def show_joined_command(message: Message, user: models.User, lex: types.ModuleType):
    await message.answer(lex.commands_answers[cmds.show_joined]['success'] + ', '.join(user.setup.names_dict.values()),
                         reply_markup=setup_markup(lex))

@router.callback_query(F.data == cmds.show_joined)
async def show_joined_command(callback_query: CallbackQuery, user: models.User, lex: types.ModuleType):
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(lex.commands_answers[cmds.show_joined]['success'] + ', '.join(user.setup.names_dict.values()),
                                        reply_markup=setup_markup(lex))

async def play_game(message: Message, user: models.User, lex: types.ModuleType):
    answers_dict = lex.commands_answers[cmds.play]
    if len(user.setup.player_list) != cfg.NUM_PLAYERS:  # 2 for now
        await message.answer(answers_dict['fail'] + str(len(user.setup.player_list)), reply_markup=setup_markup(lex))
    else:
        new_game = models.Game(**asdict(user.setup))
        setup = user.setup

        users = [data.get_user(user_id) for user_id in user.setup.player_list]
        for user in users:
            user.game_id = new_game.id
            user.setup = None
            data.save_user(user)
            new_game.names_dict[user.id] = user.name
            setup.names_dict[user.id] = user.name  # for the correct representation further

        new_game.prepare_game()
        # new_game.langs_dict = {user.id: user.lang_code for user in users}  # already was set on joining the setup
        new_game.rounded_elos_dict = {user.id: user.get_rounded_elo() for user in users}

        data.save_game(new_game)
        for user in users:
            lex = lang_codes.get(new_game.langs_dict[user.id], lang_codes['en']) if user else lexicon_en
            await msg_repo.send_player(message.bot, user.id, lex.commands_answers[cmds.play]['success'] + setup.setup_repr(lex))
            main_message = await message.bot.send_message(user.id, new_game.game_repr(lex), reply_markup=None)
            new_game.messages_dict[user.id] = main_message.message_id
            # show alternatives buttons
            await msg_repo.update_msg_player(message.bot, user.id, new_game.messages_dict[user.id], new_game.game_repr(lex), new_game.create_markup())
        data.save_game(new_game)  # to save messages id's


@router.message(Command(commands=cmds.play))
async def play_game_command(message: Message, user: models.User, lex: types.ModuleType):
    await play_game(message, user, lex)

@router.callback_query(F.data == cmds.play)
async def play_game_callback(callback_query: CallbackQuery, user, lex: types.ModuleType):
    await callback_query.message.delete_reply_markup()
    await play_game(callback_query.message, user, lex)

""" # all commented logic is now in /leave command
@router.message(Command(commands='kick'))
async def kick_player_command(message: Message):
    user_id_to_kick = message.text[len('/kick '):]
    if len(user_id_to_kick) < 3:
        await message.answer(f"Error: user ID was not provided")
    else:
        await message.answer(game_service.kick_player(str(message.from_user.id), user_id_to_kick))


@router.message(Command(commands='cancel'))
async def cancel_game_command(message: Message):
    answer = game_service.cancel_game(str(message.from_user.id))
    await message.answer(answer)
"""