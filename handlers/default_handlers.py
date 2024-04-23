from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery
import data
from communication import msg_repo
from handlers.markups import default_markup, setup_markup
from lexicon import lex, cmds
import models



# Инициализируем роутер уровня модуля
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if data.get_user(str(message.from_user.id)) is None:
        new_user = models.User(str(message.from_user.id), message.from_user.first_name)
        data.save_user(new_user)
    # await message.answer(lex.commands_answers[cmds.start]['success'])  # actually greet a player with rules seems enough
    await message.answer(lex.commands_answers[cmds.rules]['success'], reply_markup=default_markup())



async def process_rules(message: Message):
    await message.answer(text=lex.commands_answers[cmds.rules]['success'], reply_markup=default_markup())

@router.message(or_f(Command(commands=cmds.rules), Command(commands=cmds.main_menu)))
async def process_rules_command(message: Message):
    await process_rules(message)


@router.callback_query(or_f(F.data == cmds.rules, F.data == cmds.main_menu))
async def process_rules_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await process_rules(callback_query.message)




async def process_help(message: Message):
    text = lex.commands_answers[cmds.help]['success']
    await message.answer(text, reply_markup=default_markup())

@router.message(Command(commands=cmds.help))
async def process_help_command(message: Message):
    await process_help(message)

@router.callback_query(F.data == cmds.help)
async def process_help_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await process_help(callback_query.message)





async def change_name(message: Message):
    user_id = str(message.from_user.id)
    user = data.get_user(user_id)
    new_name = message.text[13:].strip()
    answers_dict = lex.commands_answers[cmds.change_name]
    if user is None:
        answer = answers_dict['fail']
        await message.answer(answer, reply_markup=default_markup(), parse_mode='Markdown')
    elif len(new_name) == 0 or len(new_name) < 3:
        answer = answers_dict['fail'] + '\n' + answers_dict['current'] + user.name
        await message.answer(answer, reply_markup=default_markup(), parse_mode='Markdown')
    else:
        user.name = new_name
        data.save_user(user)
        answer = answers_dict['success'] + new_name
        await message.answer(answer, reply_markup=default_markup(), parse_mode='Markdown')

@router.message(Command(commands=cmds.change_name))
async def change_name_command(message: Message):
    await change_name(message)

@router.callback_query(F.data == cmds.change_name)
async def change_name_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await change_name(callback_query.message)


async def create_setup(message: Message, user_id: str):
    user = data.get_user(user_id)
    if user.game_id is not None:
        await message.answer(lex.info_messages['already_in_game'], reply_markup=setup_markup(), parse_mode='Markdown')
    else:
        new_setup = models.Setup()
        new_setup.add_player(user_id, user.name, user.get_rounded_elo())
        user.setup = new_setup
        data.save_user(user)

        answer = lex.commands_answers[cmds.new]['success'] + f"`/join {user_id}`"
        await message.answer(answer, reply_markup=setup_markup(), parse_mode='Markdown')

@router.message(Command(commands=cmds.new))
async def create_setup_command(message: Message):
    user_id = str(message.from_user.id)
    await create_setup(message, user_id)

@router.callback_query(F.data == cmds.new)
async def create_setup_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    user_id = str(callback_query.from_user.id)
    await create_setup(callback_query.message, user_id)




@router.message(Command(commands=cmds.join))  # vulnerability for targeted attack
async def join_setup_command(message: Message):
    answers_dict = lex.commands_answers[cmds.join]
    admin_id = message.text[len('/join '):]  # The format is /join <admin_id>
    if not admin_id:
        await message.answer(answers_dict['none'])
    else:
        admin = data.get_user(admin_id)
        if admin is None or admin.setup is None:
            await message.answer(answers_dict['fail'], reply_markup=default_markup())
        else:  # success
            user_id = str(message.from_user.id)
            user = data.get_user(user_id)
            admin.setup.add_player(user_id, message.from_user.first_name, user.get_rounded_elo())
            user.setup = admin.setup
            data.save_user(admin)
            data.save_user(user)  # on pickling .setup attr becomes independent
            await msg_repo.send_player(message.bot, admin.id, answers_dict['for_admin'] + user.name)
            await message.answer(answers_dict['success'] + admin.name, reply_markup=setup_markup())

@router.callback_query(F.data == cmds.join)
async def join_setup_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(lex.commands_answers[cmds.join]['none'], reply_markup=default_markup())

async def repeat_game(bot: Bot, user_id: str, old_game_id: str):
    old_game = data.get_completed_game(old_game_id)
    if old_game:
        new_setup = models.Setup()
        new_setup.update_from_game(old_game)
        users = [data.get_user(user_id) for user_id in new_setup.player_list]
        for user in users:
            new_setup.rounded_elos_dict[user.id] = user.get_rounded_elo()
        for user in users:
            user.setup = new_setup
            data.save_user(user)

        text = lex.commands_answers[cmds.repeat]['success'] + str(new_setup)
        await msg_repo.send_many_players(bot, new_setup.player_list, text, keyboard=setup_markup())
    else:
        await bot.send_message(user_id, lex.commands_answers[cmds.repeat]['fail'], reply_markup=default_markup())

@router.message(Command(commands=cmds.repeat))
async def repeat_game_command(message: Message):
    old_game_id = message.text[len('/repeat '):]  # The format is /repeat <game_id>
    if old_game_id == "":
        await message.answer(lex.commands_answers[cmds.repeat]['none'], reply_markup=default_markup())
    else:
        await repeat_game(message.bot, str(message.from_user.id), old_game_id)

@router.callback_query(F.data.startswith('repeat '))
async def repeat_id_game_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    game_id = callback_query.data[len('repeat '):]
    await repeat_game(callback_query.bot, str(callback_query.from_user.id), game_id)
    # await callback_query.message.answer(lex.commands_answers[cmds.repeat]['none'], reply_markup=default_markup())

@router.callback_query(F.data == cmds.repeat)
async def repeat_game_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(lex.commands_answers[cmds.repeat]['none'], reply_markup=default_markup())


@router.message(lambda message: True)
async def unknown_command(message: Message):
    await message.answer(lex.commands_answers[cmds.unknown], reply_markup=default_markup())

@router.callback_query()
async def unknown_callback(message: Message):
    await message.answer(lex.commands_answers[cmds.unknown])