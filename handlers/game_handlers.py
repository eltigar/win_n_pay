from aiogram import Router
from aiogram.filters import Command, BaseFilter
from aiogram.types import CallbackQuery, Message

import data
import models
from lexicon import lex, cmds
from communication import msg_repo
from models import ALTERNATIVES
from models.elo_calculation import update_elo
from handlers.markups import repeat_markup

# Инициализируем роутер уровня модуля
router = Router()
str_alternatives = tuple(str(a) for a in ALTERNATIVES)


class StartedFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict:
        user_id = str(message.from_user.id)
        user = data.get_user(user_id)
        if user is None or user.game_id is None:
            return False
        game = data.get_game(user.game_id)
        if game is None or user.id not in game.player_list:
            print("Something wrong in game-user sync")
            return False
        return {'user': user, 'game': game}


router.message.filter(StartedFilter())


class StartedCallbackFilter(BaseFilter):
    async def __call__(self, callback_query: CallbackQuery) -> bool or dict:
        user_id = str(callback_query.from_user.id)
        user = data.get_user(user_id)
        if user is None or user.game_id is None:
            return False
        game = data.get_game(user.game_id)
        if game is None or user.id not in game.player_list:
            print("Something wrong in game-user sync")
            return False
        return {'user': user, 'game': game}


router.callback_query.filter(StartedCallbackFilter())

@router.message(Command(commands=cmds.abort))
async def process_abort_command(message: Message, user: models.User, game: models.Game):
    answers_dict = lex.commands_answers[cmds.abort]
    # check if admin?
    try:
        data.save_aborted_game(game)
        data.remove_game(game)
        for user_id in game.player_list:
            user = data.get_user(user_id)
            user.game_id = None
            data.save_user(user)
    except Exception:
        await message.answer(text=answers_dict['fail'])
    else:
        await msg_repo.update_msg_list(message.bot, game.messages_dict, str(game), None)
        await msg_repo.send_many_players(message.bot, game.player_list, answers_dict['success'])


@router.callback_query(lambda callback_query: callback_query.data in str_alternatives)
async def process_turn(callback: CallbackQuery, user: models.User, game: models.Game):
    if game is None:
        return
    # validate_input()  # not needed since there are buttons
    bet = int(callback.data)
    if bet == game.blocked_bet:
        await callback.answer(lex.info_messages['abuse'], show_alert=True)
        return

    game.turns_history[-1][str(callback.from_user.id)] = bet
    # placeholder to catch overlay if player is able to change vote

    if "-" in game.turns_history[-1].values():
        data.save_game(game)
        await msg_repo.update_msg_player(callback.bot, user.id, callback.message.message_id, str(game) + '\n' + lex.info_messages['waiting'], None)
    else:
        game.update_state(game.play_round())
        if game.is_finished():
            users = tuple(data.get_user(user_id) for user_id in game.player_list)
            new_elos = update_elo(users[0].elo, users[1].elo, first_player_score=game.winners_dict[game.player_list[0]])
            for user, new_elo in zip(users, new_elos):
                user.elo = new_elo
                game.rounded_elos_dict[user.id] = user.get_rounded_elo()
                user.game_id = None
                data.save_user(user)

            data.save_completed_game(game)
            data.remove_game(game)

            winners_str = ', '.join([game.names_dict[pid] for pid in game.player_list if game.winners_dict[pid] == 1])
            losers_str = ', '.join([game.names_dict[pid] for pid in game.player_list if game.winners_dict[pid] == 0])
            elo_info = ', '.join([game.names_dict[pid] + ": " + str(game.rounded_elos_dict[pid]) for pid in game.player_list])
            text = lex.info_messages['completed'][game.win_reason].format(game_id=game.id, winners=winners_str, points=game.points_to_win, opponent=losers_str, elo=elo_info)

            await msg_repo.update_msg_list(callback.bot, game.messages_dict, str(game), None)
            await msg_repo.send_many_players(callback.bot, game.player_list, text, keyboard=repeat_markup(game.id))
            # await msg_repo.send_many_players(callback.bot, game.player_list, lex.info_messages["offer_repeat"].format(game_id=game.id))
        else:  # game is continuing
            # updated_markup = game.create_markup()
            str_game = str(game)  # to have last bets in it
            game.create_place_for_new_turn()

            data.save_game(game)
            await msg_repo.update_msg_list(callback.bot, game.messages_dict, str_game, game.create_markup())


@router.message()
async def process_unexpected_message(message: Message):
    await message.reply(lex.commands_answers[cmds.unexpected], parse_mode='Markdown')
    await message.delete()

@router.callback_query()
async def process_wrong_in_game_callback(callback: CallbackQuery):
    await callback.answer(lex.info_messages['already_in_game'], show_alert=True)

