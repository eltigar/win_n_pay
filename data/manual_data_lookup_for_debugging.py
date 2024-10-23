import os
import pickle
from models.user_models import User

# Пути к файлам для хранения данных
users_PATH = "users.pickle"
users_old_PATH = "old_users.pickle"
games_PATH = "games.pickle"
setup_PATH = "setups.pickle"
completed_games_PATH = "completed_games.pickle"
aborted_games_PATH = "aborted_games.pickle"
local_path = "C:/Users/ibrau/Repositories/volumes_data/win_n_pay/data/"

file_path = local_path + completed_games_PATH

if os.path.isfile(file_path):
    with open(file_path, "rb") as f:
        data: dict = pickle.load(f)
    for item in data.values():
        print(item)



# update script
if os.path.isfile(file_path) and False:
    with open(file_path, "rb") as f:
        data: dict = pickle.load(f)
    for item in data.values():
        item.lang_code = 'ru'  # which parameter to add
        print(item)
    try:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"Error saving object: {e}")
