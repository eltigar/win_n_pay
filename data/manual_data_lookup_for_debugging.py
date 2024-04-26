import os
import pickle
from models.user_models import User

# Пути к файлам для хранения данных
users_PATH = "users.pickle"
users_old_PATH = "users_old.pickle"
games_PATH = "games.pickle"
setup_PATH = "setups.pickle"
completed_games_PATH = "completed_games.pickle"
aborted_games_PATH = "aborted_games.pickle"

file_path = users_old_PATH


if os.path.isfile(file_path):
    with open(file_path, "rb") as f:
        data: dict = pickle.load(f)
    for item in data.values():
        print(item)
    #print(data)
