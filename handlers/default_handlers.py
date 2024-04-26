import types

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery
import data
from communication import msg_repo
from handlers.markups import default_markup, setup_markup, langs_markup
from lexicon import *
import models


# Инициализируем роутер уровня модуля
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    user = data.get_user(str(message.from_user.id))
    if user is None:
        user = models.User(str(message.from_user.id), message.from_user.first_name, message.from_user.language_code)
        data.save_user(user)
    lex = lang_codes.get(user.lang_code, lang_codes['en'])
    # await message.answer(lex.commands_answers[cmds.start]['success'])  # actually greet a player with rules seems enough
    await message.answer(lex.commands_answers[cmds.rules]['success'], reply_markup=default_markup(lex))



async def process_rules(message: Message, user_id):
    user = data.get_user(user_id)
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await message.answer(text=lex.commands_answers[cmds.rules]['success'], reply_markup=default_markup(lex))

@router.message(or_f(Command(commands=cmds.rules), Command(commands=cmds.main_menu)))
async def process_rules_command(message: Message):
    await process_rules(message, str(message.from_user.id))


@router.callback_query(or_f(F.data == cmds.rules, F.data == cmds.main_menu))
async def process_rules_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await process_rules(callback_query.message, str(callback_query.from_user.id))




async def process_help(message: Message, user_id: str):
    user = data.get_user(str(user_id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    text = lex.commands_answers[cmds.help]['success']
    await message.answer(text, reply_markup=default_markup(lex))

@router.message(Command(commands=cmds.help))
async def process_help_command(message: Message):
    await process_help(message, str(message.from_user.id))

@router.callback_query(F.data == cmds.help)
async def process_help_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await process_help(callback_query.message, str(callback_query.from_user.id))





async def change_name(message: Message, user_id: str):
    user = data.get_user(user_id)
    new_name = message.text[13:].strip()
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    answers_dict = lex.commands_answers[cmds.change_name]
    if user is None:
        answer = answers_dict['fail']
        await message.answer(answer, reply_markup=default_markup(lex), parse_mode='Markdown')
    elif len(new_name) == 0 or len(new_name) < 3 or "_" in new_name:
        answer = answers_dict['fail'] + '\n' + answers_dict['current'] + user.name
        await message.answer(answer, reply_markup=default_markup(lex), parse_mode='Markdown')
    else:
        user.name = new_name
        data.save_user(user)
        answer = answers_dict['success'] + new_name
        await message.answer(answer, reply_markup=default_markup(lex), parse_mode='Markdown')

@router.message(Command(commands=cmds.change_name))
async def change_name_command(message: Message):
    await change_name(message, str(message.from_user.id))

@router.callback_query(F.data == cmds.change_name)
async def change_name_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await change_name(callback_query.message, str(callback_query.from_user.id))


@router.callback_query(F.data == cmds.change_lang)
async def change_lang_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    await callback_query.message.answer(text=lexicon_en.info_messages["langs"], reply_markup=langs_markup())

@router.callback_query(F.data.in_(lang_codes.keys()))
async def new_lang_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    user_id = str(callback_query.from_user.id)
    user = data.get_user(user_id)
    user.lang_code = callback_query.data
    data.save_user(user)
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await callback_query.message.answer(lex.commands_answers[cmds.change_lang]['success'] + user.lang_code, reply_markup=default_markup(lex), parse_mode='Markdown')


async def create_setup(message: Message, user_id: str):
    user = data.get_user(user_id)
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    if user.game_id is not None:
        await message.answer(lex.info_messages['already_in_game'], reply_markup=setup_markup(lex), parse_mode='Markdown')
    else:
        new_setup = models.Setup()
        new_setup.add_player(user_id, user.name, user.lang_code, user.get_rounded_elo())
        user.setup = new_setup
        data.save_user(user)

        answer = lex.commands_answers[cmds.new]['success'] + f"`/join {user_id}`"
        await message.answer(answer, reply_markup=setup_markup(lex), parse_mode='Markdown')

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
    user_id = str(message.from_user.id)
    user = data.get_user(user_id)
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    answers_dict = lex.commands_answers[cmds.join]
    admin_id = message.text[len('/join '):]  # The format is /join <admin_id>
    if not admin_id:
        await message.answer(answers_dict['none'])
    else:
        admin = data.get_user(admin_id)
        if admin is None or admin.setup is None:
            await message.answer(answers_dict['fail'], reply_markup=default_markup(lex))
        else:  # success
            admin.setup.add_player(user_id, message.from_user.first_name, user.lang_code, user.get_rounded_elo())
            user.setup = admin.setup
            data.save_user(admin)
            data.save_user(user)  # on pickling .setup attr becomes independent
            admin_lex = lang_codes.get(admin.lang_code, lang_codes['en']) if user else lexicon_en
            await msg_repo.send_player(message.bot, admin.id, admin_lex.commands_answers[cmds.join]['for_admin'] + user.name, keyboard=setup_markup(admin_lex))
            await message.answer(answers_dict['success'] + admin.name, reply_markup=setup_markup(lex))

@router.callback_query(F.data == cmds.join)
async def join_setup_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    user = data.get_user(str(callback_query.from_user.id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await callback_query.message.answer(lex.commands_answers[cmds.join]['none'], reply_markup=default_markup(lex))

async def repeat_game(bot: Bot, user_id: str, old_game_id: str, lex: types.ModuleType):
    old_game = data.get_completed_game(old_game_id)
    if old_game:
        new_setup = models.Setup()
        new_setup.update_from_game(old_game)
        users = [data.get_user(user_id) for user_id in new_setup.player_list]
        for user in users:
            new_setup.rounded_elos_dict[user.id] = user.get_rounded_elo()
            new_setup.names_dict[user.id] = user.name
        for user in users:
            user.setup = new_setup
            data.save_user(user)

        for user in users:
            lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
            text = lex.commands_answers[cmds.repeat]['success'] + new_setup.setup_repr(lex)
            await msg_repo.send_player(bot, user.id, text, keyboard=setup_markup(lex))
    else:
        await bot.send_message(user_id, lex.commands_answers[cmds.repeat]['fail'], reply_markup=default_markup(lex))

@router.message(Command(commands=cmds.repeat))
async def repeat_game_command(message: Message):
    old_game_id = message.text[len('/repeat '):]  # The format is /repeat <game_id>
    user = data.get_user(str(message.from_user.id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en

    if old_game_id == "":
        await message.answer(lex.commands_answers[cmds.repeat]['none'], reply_markup=default_markup(lex))
    else:
        await repeat_game(message.bot, str(message.from_user.id), old_game_id, lex)

@router.callback_query(F.data.startswith('repeat '))
async def repeat_id_game_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    game_id = callback_query.data[len('repeat '):]
    user = data.get_user(str(callback_query.from_user.id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await repeat_game(callback_query.bot, str(callback_query.from_user.id), game_id, lex)
    # await callback_query.message.answer(lex.commands_answers[cmds.repeat]['none'], reply_markup=default_markup(lex))

@router.callback_query(F.data == cmds.repeat)
async def repeat_game_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    user = data.get_user(str(callback_query.from_user.id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await callback_query.message.answer(lex.commands_answers[cmds.repeat]['none'], reply_markup=default_markup(lex))


@router.message(lambda message: True)
async def unknown_command(message: Message):
    user = data.get_user(str(message.from_user.id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await message.answer(lex.commands_answers[cmds.unknown], reply_markup=default_markup(lex))

@router.callback_query()
async def unknown_callback(message: Message):
    user = data.get_user(str(message.from_user.id))
    lex = lang_codes.get(user.lang_code, lang_codes['en']) if user else lexicon_en
    await message.answer(lex.commands_answers[cmds.unknown])