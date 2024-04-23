import os
import pickle

# Пути к файлам для хранения данных
users_PATH = "users.pickle"
games_PATH = "games.pickle"
setup_PATH = "setups.pickle"
completed_games_PATH = "completed_games.pickle"
aborted_games_PATH = "aborted_games.pickle"

file_path = users_PATH


if os.path.isfile(file_path):
    with open(file_path, "rb") as f:
        data: dict = pickle.load(f)
    print(data)
