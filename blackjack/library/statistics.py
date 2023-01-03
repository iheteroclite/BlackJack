__version__ = 0.36
__author__ = 'iheteroclite'

from math import erf, prod, comb

from src.deck import faces


def chance_of_being_caught_with_normal_dist(c_max, m, sd, w):
    """Calulate the chance of being caught cheating (between 0 and 1).

    Assumes chance of winning follows a normal distribution, with a mean of
    m and standard deviation of sd. There may be more commonly accepted
    formulae, but this is one created by the author, iheteroclite, to simulate
    a distribution tending to a maximum chance, which decreases significantly
    when the player performs badly (assuming the dealer wouldn't mind whilst
    they profit from the cheat).

    Arguments:
    -- c_max = maximum chance of being caught that can be returned
    -- m = the mean of the normal distribution of winning
    -- sd = standard deviation from mean of the normal distribution
    -- w = current win rate (wins/games_played)
           can be the chance of being caught from a blackjack win, even win,
           or both wins together (depending on use-case)
    """
    # Calculate chance coefficient, coef
    coef = c * sqrt(2) * sd
    chance = coef * (erf((w - m) / (sqrt(2) * sd)) - erf(m / (sqrt(2) * sd)))
    return chance


def chance_of_blackjack_totals(results):
    """Calculate the chance of getting the results you have over every game.

    Returns the chance of getting as many blackjacks as you have following a
    Binomeal Distribution.

    A Binomeal Distribution is the probability curve of a repeated boolean
    result where the distribution is the multiplicative product of the
    Probability(blackjack) x Probablity(not blackjack) x combinations

    To calculate the combinations, use the choose function:
        D!
    ___________ ,
    B! (D - B)!
    where:
    B = number of blackjacks you have got so far (denoted bj_count)
    D = the number of initial deals so far (denoted deck_count)

    takes in a list of each hand result (results) as a dictionary in the form:
    {
        'probability': 4.8,
        'blackjack': True,
    }
    where 'probability' is the chance of getting blackjack for that hand,
    and 'blackjack' is a bool where True means the user got blackjack on that
    hand.
    """

    # Get array of probabilities for every time user got blackjack
    bj_wins = [r['probability'] for r in results if r['blackjack']]

    # Get an array of 1-prob for every time user did not get blackjack
    not_bj = [1 - r['probability'] for r in results if not r['blackjack']]

    deal_count = len(results)
    bj_count = len(bj_wins)

    return prod(bj_wins) * prod(not_bj) * comb(deal_count, bj_count)


def chance_of_natural_blackjack(deck):
    """Calculate the probability of getting blackjack from specific deck.

    Using the formula:
        aces   tens
    P = ---- * ---- * 2
         N      N-1
    where:
    aces = total number of aces in the deck
    tens = total number of tens in the deck
    N = total number of cards in the deck
    """
    cards = len(deck.cards)
    aces = 0
    tens = 0
    for card in deck.cards:
        if card.face == faces[0]:
            aces += 1
        elif card.value == 10:
            tens += 1

    prob_draw_ace = aces / cards
    prob_draw_ten = tens / (cards - 1)

    return prob_draw_ace * prob_draw_ten * 2


def chance_with_fixed_percent(wins, rounds, expected=0.3742):
    """Calculate chance of wins after games with expected probability.

    Arguments:
    -- wins = number of wins for a particular player or player group
    -- rounds = total number of rounds played by player(s)
    -- expected = the fixed probability of getting a win

    This is used to calculate the chance of getting the amount of even wins
    (wins) that the player has. Even wins means a win that pays out at even
    odds (1:2), so any win that is not a natural/blackjack.

    The default expected probability is for even wins, taken as a standard
    0.4222 chance of winning, minus 0.048 chance of getting blackjack, so:
    chance_win - chance_blackjack = chance_even_odds_win

    Can be used to determine chance of push, win etc, where there is an
    approximate fixed expected change of that result (win/push).
    """
    prob_loss = (1 - expected)**(rounds - wins)
    return expected**wins * prob_loss * comb(rounds, wins)


def caught(player):
    """Check if the player has been caught (or assumed) cheating.

    """
    return False


def punishment(player):
    pass
