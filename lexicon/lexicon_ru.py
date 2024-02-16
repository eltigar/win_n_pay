game_terms: dict[str, str] = {
    "money": "деньги",
    "points": "очки"
}

setup_representation: dict[str, str] = {
    "players": "Игроки: ",
    "points": "Очков нужно набрать для победы: ",
    "money": "Денег на старте игры: "

}

commands_answers: dict[str, str | dict] = {
    # default
    '/start': "Вы успешно запустили бота!\nНажмите /help для получения списка доступных команд",
    '/rules': "*Правила игры Win&Pay:*\nКаждый кон игроки выбирают по числу от 0 до 5. "
              "Выбравший наибольшее число получает победное очко, но должен заплатить за него сумму, равную разнице "
              "между числами. Если числа одинаковые, кон переигрывается, а игроки обязаны поменять число. Исключения:\n"
              "- если разница между числами равна 1 — победа бесплатная\n"
              "- если против 5 попался 0 — он 'превращается' в 10 (и выигрывает ценой в 5)\n\n"
              "Побеждает игрок, который первым набрал необходимое количество победных очков. "
              "Однако, если в какой-то момент у игрока не хватает денег на оплату победы, он проигрывает немедленно.",
    '/help': "*Список доступных команд:*\n"
             "/start - Запуск бота\n"
             "/rules - Правила игры\n"
             "/help - Доступные команды\n"
             "`/change_name` - Смена имени пользователя\n"
             "/new - Создание новой игры\n"
             "/join - Присоединение к игре\n"
             "`/repeat` - Повторное присоединение к игре\n"
             "\n*При подготовке к игре:*\n"
             "/leave - Покидание игры\n"
             "`/set_points` - Установка очков для победы\n"
             "`/set_money` - Установка начального количества денег\n"
             "/show\_joined - Показать список игроков\n"
             "/play - Начало игры\n"
             "\n*В процессе игры:*\n"
             "/abort - Прерывание игры",
    '/change_name': {
        "current": "Ваше текущее имя ",
        "success": "Ваше имя успешно изменено на ",
        "fail": "Чтобы изменить имя, введите команду `/change_name ...`, заменив троеточие на новое имя"
    },
    '/new': 'Новая игра создана. Скопируйте нажатием: ',
    '/join': {
        "success": "Вы успешно присоединились к игре с участником ",
        "fail": "Игра не найдена",
        "none": "Вы не ввели номер",
        "for_admin": "В игру добавился пользователь "
    },
    '/repeat': {
        "success": "Вы добавлены в игру:\n",
        "fail": "Игра не найдена. Вы можете создать новую с помощью /new",
        "none": "Вы не ввели номер"
    },
    # in setup
    '/leave': {
        '2': "Вы успешно покинули игру ",
        '2 for other': "Игру покинул ",
        '1': "Вы покинули игру и в ней никого не осталось"
    },
    '/set_points': {
        'success': "Обновлено количество очков для победы.\nТеперь оно равно ",
        'fail_nan': "Количество очков должно быть целым числом.\nВы ввели: ",
        'fail_value': "Количество очков должно быть от 1 до 100"
    },
    '/set_money': {
        'success': "Обновлено стартовое количество денег.\nТеперь оно равно ",
        'fail_nan': "Стартовое количество денег должно быть целым числом.\nВы ввели: ",
        'fail_value': "Количество денег должно быть от 5 до 25"
    },
    '/show_joined': "Список игроков: ",
    '/play': {
        'success': "Игра начинается!\n",
        'fail': "Игра не может быть начата с количеством игроков ",
    },

    # in game
    "/abort": {
        "success": "Игра была отменена",
        "fail": "Не получилось отменить игру"
    },
    "unexpected": "Вы находитесь в игре.\nЧтобы прервать игру, пришлите команду `/abort`",
    'unknown': "Неожиданная команда.\nСписок доступных команд: /help"
}

info_messages = {
    "waiting": "⌛️_Ждем ход соперника_⌛️",
    "completed": {
        "points": "Игра завершена!\nПобедил {winners}, первым набрав {points} очков",
        "money": "Игра завершена!\nПобедил {winners}, его соперник {opponent} обанкротился"
    },
    "offer_repeat": "Если вы хотите повторить игру, отправьте `/repeat {game_id}`"
}
