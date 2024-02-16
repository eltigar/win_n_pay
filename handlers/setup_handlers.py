#  setup_handlers
from dataclasses import asdict

from aiogram import Router
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message
import models
import data
from models.game_config import NUM_PLAYERS
from communication import msg_repo
from lexicon import lex


# Инициализируем роутер уровня модуля
router = Router()

class SetupFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool or dict:
        user_id = str(message.from_user.id)
        user = data.get_user(user_id)
        if user is None or user.setup is None:
            return False
        return {'user': user}


router.message.filter(SetupFilter())


# new and join command are handled in default handlers


@router.message(Command(commands='leave'))
async def leave_game_command(message: Message, user: models.User):
    answers_dict = lex.commands_answers['/leave']
    match len(user.setup.player_list):
        case 2:
            user.setup.remove_player(user.id)
            other_user_id = user.setup.player_list[0]
            other_user = data.get_user(other_user_id)
            other_user.setup = user.setup
            user.setup = None  # only resets setup for user
            data.save_user(user)
            await message.answer(answers_dict['2'] + other_user.id)
            data.save_user(other_user)
            await msg_repo.send_player(message.bot, other_user_id, answers_dict['2 for other'] + user.name)
        case 1:
            user.setup = None
            data.save_user(user)
            await message.answer(answers_dict['1'])
        case _:
            raise ValueError('Setup maintenance broken: not 1 or 2 players in list')


@router.message(Command(commands='set_points'))
async def set_points_command(message: Message, user: models.User):
    answers_dict = lex.commands_answers['/set_points']
    points_str = message.text[len('/set_points '):]  # The format is /set_points <points>
    try:
        points = int(points_str)
        if 1 <= points <= 100:
            user.setup.points_to_win = points
            for other_user_id in user.setup.player_list:
                if other_user_id != user.id:
                    other_user = data.get_user(other_user_id)
                    other_user.setup = user.setup
                    data.save_user(other_user)
            data.save_user(user)
            await msg_repo.send_many_players(message.bot, user.setup.player_list, answers_dict['success'] + points_str)
        else:
            await message.answer(answers_dict['fail_value'])
    except ValueError:
        await message.answer(answers_dict['fail_nan'] + points_str)


@router.message(Command(commands='set_money'))
async def set_money_command(message: Message, user: models.User):
    answers_dict = lex.commands_answers['/set_money']
    money_str = message.text[len('/set_money '):]  # The format is /set_money <money>
    try:
        money = int(money_str)
        if 5 <= money <= 25:
            user.setup.starting_money = money
            for other_user_id in user.setup.player_list:
                if other_user_id != user.id:
                    other_user = data.get_user(other_user_id)
                    other_user.setup = user.setup
                    data.save_user(other_user)
            data.save_user(user)
            await msg_repo.send_many_players(message.bot, user.setup.player_list, answers_dict['success'] + money_str)
        else:
            await message.answer(answers_dict['fail_value'])
    except ValueError:
        await message.answer(answers_dict['fail_nan'] + money_str)

@router.message(Command(commands='show_joined'))
async def show_joined_command(message: Message, user: models.User):
    await message.answer(lex.commands_answers['/show_joined'] + ', '.join(user.setup.names_dict.values()))

@router.message(Command(commands='play'))
async def play_game(message: Message, user: models.User):
    answers_dict = lex.commands_answers['/play']
    if len(user.setup.player_list) != NUM_PLAYERS:  # 2 for now
        await message.answer(answers_dict['fail'])
    else:
        new_game = models.Game(**asdict(user.setup))
        for other_user_id in user.setup.player_list:
            if other_user_id != user.id:
                other_user = data.get_user(other_user_id)
                other_user.game_id = new_game.id
                other_user.setup = None
                data.save_user(other_user)
        user.game_id = new_game.id
        setup_str = str(user.setup)
        user.setup = None
        data.save_user(user)
        new_game.prepare_game()
        await msg_repo.send_many_players(message.bot, new_game.player_list, answers_dict['success'] + setup_str)
        for player in new_game.player_list:
            main_message = await message.bot.send_message(player, str(new_game), reply_markup=new_game.create_markup())
            new_game.messages_dict[player] = main_message.message_id
        data.save_game(new_game)



""" # all logic is now in /leave command
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