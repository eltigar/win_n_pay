from dataclasses import dataclass, field

import models
from models.game_config import TARGET_POINTS, STARTING_MONEY
from lexicon import lex

"""
import os

# Define a file to store the id counter
SETUP_ID_COUNTER_FILE = 'setup_id_counter.txt'


def get_setup_id():
    # Initialize last_id with 0 which will be used if the file doesn't exist
    if os.path.exists(SETUP_ID_COUNTER_FILE):
        with open(SETUP_ID_COUNTER_FILE, 'r') as file:
            last_id: int = int(file.read().strip())
    else:
        last_id: int = 0
    with open(SETUP_ID_COUNTER_FILE, 'w') as file:
        file.write(str(last_id + 1))
    return last_id + 1
"""

@dataclass
class Setup:
    # id: str = field(default_factory=get_setup_id)
    player_list: list[str] = field(default_factory=list)
    names_dict: dict[str, str] = field(default_factory=dict)
    points_to_win: int = TARGET_POINTS
    starting_money: int = STARTING_MONEY

    def __str__(self):
        players_line = lex.setup_representation['players'] + str(', '.join(self.names_dict.values()))
        points_line = lex.setup_representation['points'] + str(self.points_to_win)
        money_line = lex.setup_representation['money'] + str(self.starting_money)
        return players_line + '\n' + points_line + '\n' + money_line

    def update_starting_money(self, new_validated_money: int):
        self.starting_money = new_validated_money

    def update_points_to_win(self, new_validated_points: int):
        self.points_to_win = new_validated_points

    def update_from_game(self, game: models.Game):
        self.player_list = game.player_list
        self.names_dict = game.names_dict
        self.points_to_win = game.points_to_win
        self.starting_money = game.starting_money

    def add_player(self, player_id: str, name: str):
        self.player_list.append(player_id)
        self.names_dict[player_id] = name

    def remove_player(self, player_id: str):
        try:
            self.player_list.remove(player_id)
            self.names_dict.pop(player_id)
        except ValueError:
            print("Player not found in Setup object")


if __name__ == '__main__':
    testing = True
    if testing:
        setup1 = Setup()
        setup2 = Setup()
        print(setup1, setup2)
