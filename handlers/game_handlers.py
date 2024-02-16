from aiogram import Router, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import CallbackQuery, Message

import data
import models
from lexicon import lex
from communication import msg_repo

# Инициализируем роутер уровня модуля
router = Router()


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


@router.message(Command(commands='abort'))
async def process_abort_command(message: Message, user: models.User, game: models.Game):
    answers_dict = lex.commands_answers['/abort']
    # check if admin?
    try:
        data.save_aborted_game(game)
        data.remove_game(game)
        await msg_repo.send_many_players(message.bot, game.player_list, answers_dict['success'])
    except Exception:
        await message.answer(text=answers_dict['fail'])


@router.callback_query()
async def process_turn(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    user = data.get_user(user_id)
    game = data.get_game(user.game_id)
    # validate_input()  # not needed since there are buttons
    game.bets[str(callback.from_user.id)] = int(callback.data)
    # placeholder to catch overlay if player is able to change vote
    if '-' in game.bets.values():
        data.save_game(game)
        await msg_repo.update_msg_player(callback.bot, int(user_id), callback.message.message_id, str(game) + '\n' + lex.info_messages['waiting'], None)
    else:
        game.update_state(game.play_round())
        if game.is_finished():
            for user_id in game.player_list:
                user = data.get_user(user_id)
                user.game_id = None
                data.save_user(user)
            data.save_completed_game(game)
            data.remove_game(game)

            await msg_repo.update_msg_list(callback.bot, game.messages_dict, str(game), None)
            text = lex.info_messages['completed'][game.win_reason].format(winners=', '.join(game.winners),
                                                                          points=game.points_to_win,
                                                                          opponent=', '.join([game.names_dict[pl] for pl in game.player_list if pl not in game.winners]))
            await msg_repo.send_many_players(callback.bot, game.player_list, text)
            await msg_repo.send_many_players(callback.bot, game.player_list, lex.info_messages["offer_repeat"].format(game_id=game.id))
        else:
            # updated_markup = game.create_markup()
            str_game = str(game)  # to have last bets in it
            game.reset_bets()
            data.save_game(game)
            await msg_repo.update_msg_list(callback.bot, game.messages_dict, str_game, game.create_markup())


@router.message()
async def process_unexpected_message(message: Message):
    await message.reply(lex.commands_answers['unexpected'], parse_mode='Markdown')
    await message.delete()
