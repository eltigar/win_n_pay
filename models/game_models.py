import os
import types
from dataclasses import dataclass, field

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from models.game_config import ALTERNATIVES, SPECIAL_CASES
from lexicon import *

# Define a file to store the id counter
GAME_ID_COUNTER_FILE = 'game_id_counter.txt'


def get_game_id() -> str:
    # Initialize last_id with 0 which will be used if the file doesn't exist
    if os.path.exists(GAME_ID_COUNTER_FILE):
        with open(GAME_ID_COUNTER_FILE, 'r') as file:
            last_id: int = int(file.read().strip())
    else:
        last_id: int = 0
    with open(GAME_ID_COUNTER_FILE, 'w') as file:
        file.write(str(last_id + 1))
    return str(last_id + 1)


@dataclass
class Game:
    player_list: list[str]
    names_dict: dict[str, str]
    langs_dict: dict[str, str]
    rounded_elos_dict: dict[str, int]
    points_to_win: int
    starting_money: int
    id: str = field(default_factory=get_game_id)

    menu: frozenset[int] = ALTERNATIVES  # field(default_factory=lambda: {0, 1, 2, 3, 4, 5})
    blocked_bet: ALTERNATIVES = None
    # winners: tuple | None = None
    win_reason: str | None = None
    winners_dict: dict[str, int] = field(init=False)
    money_dict: dict[str, int] = field(init=False)
    points_dict: dict[str, int] = field(init=False)
    turns_history: list[dict[str, int | str]] = field(init=False)
    messages_dict: dict[str, Message | None] = field(init=False)


    def __str__(self):
        return self.game_repr(lexicon_en, 100)

    def game_repr(self, lex: types.ModuleType, last_turns: int = 10) -> str:
        column_width = 10
        first_turn_to_show = max(len(self.turns_history) - last_turns + 1, 1)

        names_line1 = lex.game_repr['turn'] + " " * (column_width-2*len(lex.game_repr['turn'])) + "".join([f"{name[:column_width - 2]:^{column_width-1}}" for name in self.names_dict.values()])
        history_lines = [f"{i + first_turn_to_show:<{column_width-len(str(i+first_turn_to_show))}}" + "-".join([f"{turn.get(player_id, '-'):^{column_width}}" for player_id in self.player_list]) for i, turn in enumerate(self.turns_history[-last_turns:])]
        underscores_line = "\_" * (column_width * 2)

        names_line2 = " " * column_width + "".join([f"{name[:column_width - 2]:^{column_width-1}}" for name in self.names_dict.values()])
        #elo_line = f"{lex.game_repr['elo']:<{column_width-2*len(lex.game_repr['elo'])}}" + "".join([f"{self.rounded_elos_dict.get(player_id, 0):^{column_width}}" for player_id in self.player_list])
        points_line = f"{lex.game_repr['points']:<{column_width-2*len(lex.game_repr['points'])}}" + "".join([f"{self.points_dict.get(player_id, 0):^{column_width}}" for player_id in self.player_list])
        money_line = f"{lex.game_repr['money']:<{column_width-2*len(lex.game_repr['money'])}}" + "".join([f"{self.money_dict.get(player_id, 0):^{column_width}}" for player_id in self.player_list])

        return "\n".join(string.rstrip() for string in
                         [names_line1,
                          *history_lines,
                          underscores_line,
                          "",
                          names_line2,
                          #elo_line,
                          points_line,
                          money_line]
                         )

    def create_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(option), callback_data=str(option))
                                                      for option in ALTERNATIVES if option != self.blocked_bet]])

    def validate_bets(self, bets: list[int]):  # not needed with buttons
        for bet in self.turns_history[-1].values():
            if not isinstance(bet, int):
                return f'{bet} is not integer'
            if bet == self.blocked_bet:
                return f'bet {bet} is blocked'
            if bet not in self.menu:
                return f'{bet} not in {str(self.menu)}'
        return 'all good'

    def play_round(self) -> tuple[int, int]:  # returns (winner position, price for victory)
        bets_tuple: tuple = tuple(self.turns_history[-1].values())
        if bets_tuple[0] == bets_tuple[1]:
            return -1, bets_tuple[0]  # draw and this bet is blocked now
        if bets_tuple in SPECIAL_CASES:
            return SPECIAL_CASES[bets_tuple]
        if bets_tuple[0] > bets_tuple[1]:
            money = 0 if bets_tuple[0] - bets_tuple[1] == 1 else bets_tuple[0] - bets_tuple[1]
            return 0, money
        if bets_tuple[0] < bets_tuple[1]:
            money = 0 if bets_tuple[1] - bets_tuple[0] == 1 else bets_tuple[1] - bets_tuple[0]
            return 1, money
        raise ValueError(f"Bets values {bets_tuple} are incorrect")

    def update_state(self, results: tuple[int, int]):
        if results[0] == -1:  # draw
            self.blocked_bet = results[1]
        else:
            self.blocked_bet = None
            winner_id = self.player_list[results[0]]
            loser_id = self.player_list[1 - results[0]]
            self.points_dict[winner_id] += 1
            self.money_dict[winner_id] -= results[1]
            self.money_dict[loser_id] += results[1]

    def create_place_for_new_turn(self):
        # self.bets = {pl_id: '-' for pl_id in self.player_list}
        self.turns_history.append({pl_id: '-' for pl_id in self.player_list})

    def is_finished(self) -> bool:
        for player_id in self.player_list:
            # Firstly check for money loss
            if self.money_dict[player_id] < 0:
                # Find the other player's ID and set them as the winners
                #self.winners = tuple(self.names_dict[pid] for pid in self.player_list if pid != player_id)
                self.win_reason = "money"
                for pid in self.player_list:
                    if pid != player_id:
                        self.winners_dict[pid] = 1
                return True
        for player_id in self.player_list:
            # Only now check for points gained
            if self.points_dict[player_id] >= self.points_to_win:
                #self.winners = (self.names_dict[player_id],)
                self.win_reason = "points"
                self.winners_dict[player_id] = 1
                return True

        # If no winners or loser is found, the game continues.
        return False


    def prepare_game(self):
        self.winners_dict: dict[str, int] = {pl_id: 0 for pl_id in self.player_list}
        self.money_dict: dict[str, int] = {pl_id: self.starting_money for pl_id in self.player_list}
        self.points_dict: dict[str, int] = {pl_id: 0 for pl_id in self.player_list}
        # self.bets: dict[str, int | str] = {pl_id: '-' for pl_id in self.player_list}
        self.turns_history = [{pl_id: '-' for pl_id in self.player_list}]
        self.messages_dict: dict[str, int | None] = {pl_id: None for pl_id in self.player_list}







