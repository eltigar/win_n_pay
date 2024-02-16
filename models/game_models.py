import os
from dataclasses import dataclass, field

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from models.game_config import ALTERNATIVES, SPECIAL_CASES

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
    points_to_win: int
    starting_money: int
    id: str = field(default_factory=get_game_id)

    menu: frozenset[int] = ALTERNATIVES  # field(default_factory=lambda: {0, 1, 2, 3, 4, 5})
    blocked_bet: ALTERNATIVES = None
    winners: tuple | None = None
    win_reason: str | None = None
    money_dict: dict[str, int] = field(init=False)
    points_dict: dict[str, int] = field(init=False)
    bets: dict[str, int] = field(init=False)
    messages_dict: dict[str, Message | None] = field(init=False)

    def __str__(self) -> str:
        lines = ["Игроки:    " + "   ".join(self.names_dict.values()),
                 "Очки:        " + "   ".join(
                     f"{self.points_dict.get(player_id, 0):>5}" for player_id in self.player_list),
                 "Деньги:     " + "   ".join(
                     f"{self.money_dict.get(player_id, 0):>5}" for player_id in self.player_list),
                 "Посл. ход:  " + "   ".join(f"{self.bets.get(player_id, '-'):>5}" for player_id in self.player_list)]
        return "\n".join(lines)

    def create_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=str(option), callback_data=str(option))
                                                      for option in ALTERNATIVES if option != self.blocked_bet]])

    def validate_bets(self, bets: list[int]):  # not needed with buttons
        for bet in self.bets.values():
            if not isinstance(bet, int):
                return f'{bet} is not integer'
            if bet == self.blocked_bet:
                return f'bet {bet} is blocked'
            if bet not in self.menu:
                return f'{bet} not in {str(self.menu)}'
        return 'all good'

    def play_round(self) -> tuple[int, int]:
        bets_tuple: tuple = tuple(self.bets.values())
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

    def reset_bets(self):
        self.bets = {pl_id: '-' for pl_id in self.player_list}

    def is_finished(self) -> bool:
        for player_id in self.player_list:
            # Check for money loss
            if self.money_dict[player_id] < 0:
                # Find the other player's ID and set them as the winners
                self.winners = tuple(self.names_dict[pid] for pid in self.player_list if pid != player_id)
                self.win_reason = "money"
                return True
            # Check for points win
            elif self.points_dict[player_id] >= self.points_to_win:
                self.winners = (self.names_dict[player_id],)
                self.win_reason = "points"
                return True

        # If no winners or loser is found, the game continues.
        return False

    def prepare_game(self):
        self.money_dict: dict[str, int] = {pl_id: self.starting_money for pl_id in self.player_list}
        self.points_dict: dict[str, int] = {pl_id: 0 for pl_id in self.player_list}
        self.bets: dict[str, int | str] = {pl_id: '-' for pl_id in self.player_list}
        self.messages_dict: dict[str, int | None] = {pl_id: None for pl_id in self.player_list}







