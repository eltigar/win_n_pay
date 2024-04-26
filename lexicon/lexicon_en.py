from lexicon.string_constants import cmds
from models.game_config import MIN_MONEY, MAX_MONEY, MIN_POINTS, MAX_POINTS

game_terms: dict[str, str] = {
    "money": "money",
    "points": "points"
}

setup_representation: dict[str, str] = {
    "players": "Players: ",
    "elo": "Elo rating: ",
    "points": "Points needed to win: ",
    "money": "Starting money: "
}

game_repr: dict[str, str] = {
    "turn": "Turn",
    "state": "Game state:",
    "elo": "🧠",
    "points": "🏆",
    "money": "💰"
}

commands_answers: dict[str, str | dict] = {
    cmds.start: {
        'success': "You've successfully started the bot!\nPress /help to get the list of available commands",
        'button_text': "Start"
    },
    cmds.rules: {
        'success': "*Rules of the Win&Pay game:*\nEach turn, players choose a number from 0 to 5. "
              "The one who picks the highest number gets a winning point but has to pay an amount equal to the difference "
              "between the numbers. If the numbers are the same, the turn is replayed, and players must change their number. Exceptions:\n"
              "- if the difference between numbers is 1 — the victory is free\n"
              "- if against 5 there's a 0 — it 'transforms' into 10 (and wins at the cost of 5)\n\n"
              "The player who first scores the required number of winning points wins. "
              "However, if a player runs out of money at any point, they lose immediately.",
        'button_text': "Rules"
    },
    cmds.help: {
        'success': "*List of available commands:*\n"
             "/rules - Game rules\n"
             "/help - Available commands\n"
             "`/change_name` - Change your name\n"
             "/new - Create a new game\n"
             "/join - Join a game\n"
             "`/repeat` - Rejoin a game\n"
             "\n*When preparing for a game:*\n"
             "/leave - Leave the game\n"
             "`/set\_points` - Set points needed to win\n"
             "`/set\_money` - Set the starting amount of money\n"
             "/show\_joined - Show the list of players\n"
             "/play - Start the game\n"
             "\n*During the game:*\n"
             "/abort - Abort the game",
        'button_text': "Help"
    },
    cmds.change_name: {
        "current": "Your current name ",
        "success": "Your name has been successfully changed to ",
        "fail": "To change your name enter the command `/change_name ...`, replacing the ellipsis with the new name. You may only use letters, not special symbols.",
        'button_text': "Change name",
    },
    cmds.change_lang: {
        "current": "Your current language ",
        "success": "Your new language is ",
        "info": "English: en\nРусский: ru",
        'button_text': "Change language🌐",
    },
    cmds.new: {
        'success': 'A new game has been created. Copy by pressing: ',
        'button_text': "New game"
    },
    cmds.join: {
        "success": "You've successfully joined the game with participant ",
        "fail": "Game not found",
        "none": "To join a game enter the command `/join ...`, replacing the ellipsis with the player's ID",
        "for_admin": "A user has joined the game: ",
        'button_text': "Join a game",
    },
    cmds.repeat: {
        "success": "You've been added to the game:\n",
        "fail": "Game not found. You can create a new one using /new",
        "none": "To repeat a game enter the command `/repeat ...`, replacing the ellipsis with the game's ID",
        'button_text': "Repeat game",
    },
    cmds.main_menu: { # rules is used after main menu command
    #    "success": "Вы добавлены в игру:\n",
    #    "fail": "Игра не найдена. Вы можете создать новую с помощью /new",
    #    "none": "Чтобы повторить игру, введите команду `/repeat ...`, заменив троеточие на ID игры",
        'button_text': "Main menu"
    },
    cmds.leave: {
        '2': "You've successfully left the game with player ",
        '2 for other': "Player left the game: ",
        '1': "You've left the game, and there's no one left",
        'button_text': "Leave game",
    },
    cmds.set_points: {
        'success': "The number of points to win has been updated.\nIt's now ",
        'fail_none': f"To set the vicory points enter the command `/set_points ...`, replacing the ellipsis with the intended amount. That should be a number between {MIN_POINTS} and {MAX_POINTS}",
        'fail_nan': "The number of points must be an integer.\nYou entered: ",
        'fail_value': "The number of points must be from 1 to 100",
        'button_text': "Set points",
    },
    cmds.set_money: {
        'success': "The starting amount of money has been updated.\nIt's now ",
        'fail_none': f"To set the starting money enter the command `/set_money ...`, replacing the ellipsis with the intended amount. That should be a number between {MIN_MONEY} and {MAX_MONEY}",
        'fail_nan': "The starting amount of money must be an integer.\nYou entered: ",
        'fail_value': "The amount of money must be from 5 to 25",
        'button_text': "Set money",
    },
    cmds.show_joined: {
        'success': "List of players: ",
        'button_text': "Start"
    },
    cmds.play: {
        'success': "The game starts!\n",
        'fail': "The game cannot be started with the number of players ",
        'button_text': "Start game",
    },
    cmds.abort: {
        "success": "The game has been aborted",
        "fail": "Failed to abort the game",
        'button_text': "Abort game",  # should not be displayed normally
    },
    cmds.unexpected: "You are in a game.\nTo abort the game, send the command `/abort`",
    cmds.unknown: "Unexpected command.\nList of available commands: /help"
}

info_messages = {
    "waiting": "⌛️_Waiting for the opponent's move_⌛️",
    "langs": "English: en\nРусский: ru",
    "completed": {
        "points": "The game {game_id} is over!\nThe winner is {winners}, first to score {points} points.\nUpdated elo: {elo}.",
        "money": "The game is over!\nThe winner is {winners}, their opponent {opponent} went bankrupt.\nUpdated elo: {elo}."
    },
    "offer_repeat": "If you want to repeat the game, send `/repeat {game_id}`",
    "already_in_game": "You are already in the game.\nSend /abort command to abort the game.",
    "abuse": "Consider visiting https://quizondo.com/quizzes/am-i-abusive/",
}
