NUM_PLAYERS = 2

if NUM_PLAYERS == 2:
    ALTERNATIVES = frozenset((0, 1, 2, 3, 4, 5))
    SPECIAL_CASES: dict[tuple[int, int], tuple[int, int]] = {
                (0, 5): (0, 5),
                (5, 0): (1, 5)
            }
    STARTING_MONEY: int = 10
    TARGET_POINTS: int = 10
