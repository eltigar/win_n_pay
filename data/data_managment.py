import os
import pickle

import models.setup_models

# Пути к файлам для хранения данных
users_PATH = "data/users.pickle"
games_PATH = "data/games.pickle"
setup_PATH = "data/setups.pickle"
completed_games_PATH = "data/completed_games.pickle"
aborted_games_PATH = "data/completed_games.pickle"


def save_object(obj: models.User | models.Game | models.setup_models.Setup, file_path: str) -> None:
    try:
        data: dict = {}
        if os.path.isfile(file_path):  # Проверка существования файла без создания директории
            with open(file_path, "rb") as f:
                data: dict = pickle.load(f)
        data[obj.id] = obj
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"Error saving object: {e}")

def get_object(obj_id: str, file_path: str) -> models.User | models.Game | models.setup_models.Setup | None:
    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            data: dict = pickle.load(f)
            return data.get(obj_id)
    return None

def remove_object(obj: models.User | models.Game | models.setup_models.Setup, file_path: str) -> bool:
    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            data: dict = pickle.load(f)
        try:
            data.pop(obj.id)
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
            return True
        except KeyError:
            print('Object not found')
            return False
    return False


def save_user(user: models.User) -> None:
    return save_object(user, users_PATH)

def get_user(user_id: str) -> models.User | None:
    return get_object(user_id, users_PATH)


def save_game(game: models.Game) -> None:
    return save_object(game, games_PATH)

def get_game(game_id: str) -> models.Game | None:
    return get_object(game_id, games_PATH)

def remove_game(game: models.Game) -> bool:
    return remove_object(game, games_PATH)


def save_completed_game(game: models.Game) -> None:
    return save_object(game, completed_games_PATH)

def get_completed_game(game_id: str) -> models.Game | None:
    return get_object(game_id, completed_games_PATH)


def save_aborted_game(game: models.Game) -> None:
    return save_object(game, aborted_games_PATH)

def get_aborted_game(game_id: str) -> models.Game | None:
    return get_object(game_id, aborted_games_PATH)


def save_setup(setup: models.setup_models.Setup) -> None:
    return save_object(setup, completed_games_PATH)

def get_setup(setup_id: str) -> models.setup_models.Setup | None:
    return get_object(setup_id, setup_PATH)
