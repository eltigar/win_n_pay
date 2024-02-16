game_terms: dict[str, str] = {
    "money": "money",
    "points": "points"
}

setup_representation: dict[str, str] = {
    "players": "Players: ",
    "points": "Points needed to win: ",
    "money": "Starting money: "
}

commands_answers: dict[str, str | dict] = {
    '/start': "You've successfully started the bot!\nPress /help to get the list of available commands",
    '/rules': "*Rules of the Win&Pay game:*\nEach turn, players choose a number from 0 to 5. "
              "The one who picks the highest number gets a winning point but has to pay an amount equal to the difference "
              "between the numbers. If the numbers are the same, the turn is replayed, and players must change their number. Exceptions:\n"
              "- if the difference between numbers is 1 — the victory is free\n"
              "- if against 5 there's a 0 — it 'transforms' into 10 (and wins at the cost of 5)\n\n"
              "The player who first scores the required number of winning points wins. "
              "However, if a player runs out of money at any point, they lose immediately.",
    '/help': "*List of available commands:*\n"
             "/start - Start the bot\n"
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
    '/change_name': {
        "current": "Your current name ",
        "success": "Your name has been successfully changed to ",
        "fail": "To change your name, enter the command `/change_name ...`, replacing the ellipsis with the new name"
    },
    '/new': 'A new game has been created. Copy by pressing: ',
    '/join': {
        "success": "You've successfully joined the game with participant ",
        "fail": "Game not found",
        "none": "You didn't enter a number",
        "for_admin": "A user has joined the game "
    },
    '/repeat': {
        "success": "You've been added to the game:\n",
        "fail": "Game not found. You can create a new one using /new",
        "none": "You didn't enter a number"
    },
    '/leave': {
        '2': "You've successfully left the game ",
        '2 for other': "Player left the game ",
        '1': "You've left the game, and there's no one left"
    },
    '/set_points': {
        'success': "The number of points to win has been updated.\nIt's now ",
        'fail_nan': "The number of points must be an integer.\nYou entered: ",
        'fail_value': "The number of points must be from 1 to 100"
    },
    '/set_money': {
        'success': "The starting amount of money has been updated.\nIt's now ",
        'fail_nan': "The starting amount of money must be an integer.\nYou entered: ",
        'fail_value': "The amount of money must be from 5 to 25"
    },
    '/show_joined': "List of players: ",
    '/play': {
        'success': "The game starts!\n",
        'fail': "The game cannot be started with the number of players ",
    },
    "/abort": {
        "success": "The game has been aborted",
        "fail": "Failed to abort the game"
    },
    "unexpected": "You are in a game.\nTo abort the game, send the command `/abort`",
    'unknown': "Unexpected command.\nList of available commands: /help"
}

info_messages = {
    "waiting": "⌛️_Waiting for the opponent's move_⌛️",
    "completed": {
        "points": "The game is over!\nThe winner is {winners}, first to score {points} points",
        "money": "The game is over!\nThe winner is {winners}, their opponent {opponent} went bankrupt"
    },
    "offer_repeat": "If you want to repeat the game, send `/repeat {game_id}`"
}
