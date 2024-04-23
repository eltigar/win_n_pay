DEFAULT_ELO = 1500 * 100
C_VALUE = 332
K_VALUE = 75

# Constants are adjusted to give:
# approximately 50 points for a win against an opponent 100 points ahead,
# approximately 25 points for a win against an opponent 100 points behind,
# approximately 5 points for a 93.3% win chance (380 points behind).
# win prob to elo diff: 50%-0, 60%-60, 66.6&-100, 75%-160, 80%-200, 90%-320,95%-425, 99%-666


def expected_score(rating1, rating2, C=C_VALUE):
    """
    Calculate the expected score based on Elo ratings, with ratings represented as integer particles.
    Constant C adjusts sensitivity to rating differences, determined to best fit your system's dynamics.

    :param rating1: Elo rating of player 1 (in particles, e.g., 150000 for 1500.00)
    :param rating2: Elo rating of player 2 (in particles)
    :param C: Sensitivity constant for rating difference
    :return: Expected score for player 1
    """
    return 1 / (1 + 10 ** ((rating2 - rating1) / (C * 100)))  # Adjust for particles


def elo_shift(rating1, rating2, first_player_score, K=K_VALUE):
    """
    Calculate the Elo shift for both players given a match result.
    Shift value is returned as integer particles.

    :param rating1: Elo rating of player 1 before the game (in particles)
    :param rating2: Elo rating of player 2 before the game (in particles)
    :param winner_position: Match result from player 1's perspective (0 = win, 1 = loss, -1 = draw)
    :param K: K-factor, determines maximum Elo shift magnitude
    :return: Elo shift for both players as integer particles
    """
    result = first_player_score
    E = expected_score(rating1, rating2)
    #print(E)
    rating_shift = K * 100 * (result - E)  # Shift calculated in 1/100th of a point
    return round(rating_shift)


def update_ratings(rating1, rating2, rating_shift):
    """
    Updates and rounds Elo ratings for both players based on the Elo shift.

    :param rating2: Current Elo rating of player 1 (in particles)
    :param rating2: Current Elo rating of player 2 (in particles)
    :param rating_shift: Calculated Elo shift from the match (in particles)
    :return: Updated and rounded Elo ratings for both players
    """
    new_rating1 = rating1 + rating_shift
    new_rating2 = rating2 - rating_shift
    return new_rating1, new_rating2


def update_elo(elo1: int, elo2: int, first_player_score: int) -> tuple[int, int]:
    rating_shift = elo_shift(elo1, elo2, first_player_score)
    return update_ratings(elo1, elo2, rating_shift)



# Example usage
if __name__ == "__main__":
    player1_rating = 100000  # 1500.00 in particles
    player2_rating = 90000  # 1600.00 in particles
    first_player_score = 1  # Player 1 wins
    print(update_elo(player1_rating, player2_rating, first_player_score))

