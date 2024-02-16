from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import data
from communication import msg_repo
from lexicon import lex
import models
# Инициализируем роутер уровня модуля
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if data.get_user(str(message.from_user.id)) is None:
        new_user = models.User(str(message.from_user.id), message.from_user.first_name)
        data.save_user(new_user)
    await message.answer(lex.commands_answers['/start'])
    await message.answer(lex.commands_answers['/rules'])

@router.message(Command(commands='rules'))
async def process_rules_command(message: Message):
    await message.answer(text=lex.commands_answers['/rules'])

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    text = lex.commands_answers['/help']
    await message.answer(text)


@router.message(Command(commands='change_name'))
async def change_name_command(message: Message):
    user_id = str(message.from_user.id)
    user = data.get_user(user_id)
    new_name = message.text[13:].strip()
    answers_dict = lex.commands_answers['/change_name']
    if len(new_name) == 0 or len(new_name) < 3:
        answer = answers_dict['fail'] + '\n' + answers_dict['current'] + user.name
        await message.answer(answer, parse_mode='Markdown')
    else:
        user.name = new_name
        data.save_user(user)
        answer = answers_dict['success'] + new_name
        await message.answer(answer, parse_mode='Markdown')


@router.message(Command(commands='new'))
async def create_setup(message: Message):
    user_id = str(message.from_user.id)
    new_setup = models.Setup()
    new_setup.add_player(user_id, message.from_user.first_name)

    user = data.get_user(user_id)
    user.setup = new_setup
    data.save_user(user)

    answer = lex.commands_answers['/new'] + f"`/join {user_id}`"
    await message.answer(answer, parse_mode='Markdown')

@router.message(Command(commands='join'))  # vulnerability for targeted attack
async def join_game_command(message: Message):
    answers_dict = lex.commands_answers['/join']
    admin_id = message.text[len('/join '):]  # The format is /join <admin_id>
    if not admin_id:
        status = 'none'
    else:
        admin = data.get_user(admin_id)
        if admin is None or admin.setup is None:
            status = 'fail'
        else:  # success
            user_id = str(message.from_user.id)
            admin.setup.add_player(user_id, message.from_user.first_name)
            user = data.get_user(user_id)
            user.setup = admin.setup
            data.save_user(admin)
            data.save_user(user)  # on pickling .setup attr becomes independent
            await msg_repo.send_player(message.bot, admin.id, answers_dict['for_admin'] + user.name)
            status = 'success'
    if status == 'success':
        await message.answer(answers_dict[status] + admin.name)
    else:
        await message.answer(answers_dict[status])

@router.message(Command(commands='repeat'))
async def repeat_game_command(message: Message):
    old_game_id = message.text[len('/repeat '):]  # The format is /repeat <game_id>
    old_game = data.get_completed_game(old_game_id)
    if old_game:
        new_setup = models.Setup()
        new_setup.update_from_game(old_game)
        for user_id in new_setup.player_list:
            user = data.get_user(user_id)
            user.setup = new_setup
            data.save_user(user)
        text = lex.commands_answers['/repeat']['success'] + str(new_setup)
        await msg_repo.send_many_players(message.bot, new_setup.player_list, text)
    else:
        await message.answer(lex.commands_answers['/repeat']['fail'])


@router.message(lambda message: True)
async def unknown_command(message: Message):
    await message.answer(lex.commands_answers['unknown'])
