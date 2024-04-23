NUM_PLAYERS = 2   # the only implemented case now

if NUM_PLAYERS == 2:
    ALTERNATIVES = frozenset((0, 1, 2, 3, 4, 5))
    SPECIAL_CASES: dict[tuple[int, int], tuple[int, int]] = {
                (0, 5): (0, 5),
                (5, 0): (1, 5)
            }
    MIN_MONEY: int = 5
    DEFAULT_MONEY: int = 10
    MAX_MONEY: int = 25

    MIN_POINTS: int = 1
    DEFAULT_POINTS: int = 10
    MAX_POINTS: int = 100
