# bot.py
from aiogram import Bot, Dispatcher
from environs import Env

from handlers import game_handlers, setup_handlers, default_handlers

# Setup environment configurations
path_to_env = "win_n_pay.env"
env = Env()  # Создаем экземпляр класса Env
env.read_env(path_to_env)  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

BOT_TOKEN = env('BOT_TOKEN')
ADMIN_ID = env.int('ADMIN_ID')

# Initialize the bot and dispatcher
bot = Bot(BOT_TOKEN, parse_mode='Markdown')
dp = Dispatcher()


# Register routers (handlers) with the dispatcher
dp.include_router(game_handlers.router)
dp.include_router(setup_handlers.router)
dp.include_router(default_handlers.router)

