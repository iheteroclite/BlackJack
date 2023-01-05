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

# Statistics for blackjack wins, modelled as a binomeal distribution with a
# variable percentage change of winning (which depends on the number of 10/Ace
# in the deck, and number of previous blackjack wins)


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


def chance_of_blackjack_totals(results, at_least=False):
    """Calculate the chance of getting the results you have over every game.

    Returns the chance of getting as many blackjacks as you have following a
    Binomeal Distribution.

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
    not_bjs = [1 - r['probability'] for r in results if not r['blackjack']]

    # TODO*: change deal_count to rounds for consistency
    deal_count = len(results)
    bj_count = len(bj_wins)

    if at_least:
        return chance_at_least_blackjack_totals(deal_count, bj_count,
                                                bj_wins, not_bjs)

    return binomeal(deal_count, bj_count, bj_wins, not_bjs)


def binomeal(deal_count, bj_count, bj_wins, not_bjs):
    """Calculate probability of a result using a Binomeal Distribution.

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
    """
    return prod(bj_wins) * prod(not_bjs) * comb(deal_count, bj_count)


def chance_at_least_blackjack_totals(deal_count, bj_count, bj_wins, not_bjs):
    """Chance of at least bj_count many blackjacks in these deal_counts rounds.

    If you do 2 rounds, with 1 blackjack, returns the total chance of getting
    either 1 or 2 blackjacks, but not 0 blackjacks.

    Calculated by: 1 - sum([chance_0,... chance_n])
    where:
    chance_0 is the chance of getting 0 blackjacks
    chance_n is the chance of getting n blackjack, with n = bj_count - 1

    Arguments:
    -- deal_count = number of rounds
    -- bj_count = number of blackjack wins
    -- bj_wins = a list of a percentage chance of blackjack for each hand where
                 the player got blackjack
    -- not_bjs = a list of the percentage chance of blackjack for each hand
                 where the player did not get blackjack

    Similar to chance_at_least_result()
    """
    # Sum the probability of getting each number of bj's less than bj_count
    sum_chances = 0

    for i in range(bj_count - 1):
        # Swap bj percentages into the not_bj percentage list
        new_not_bjs = not_bjs + bj_wins[:i]
        sum_chances += binomeal(deal_count, bj_count, bj_wins[i:], new_not_bjs)

    return 1 - sum_chances


# Statistics for 'even odds' wins (not blackjack), modelled as a binomial
# distribution with a fixed chance of winning a round.

def chance_with_fixed_percent(wins, rounds, prob_win=0.3742):
    """Calculate chance of wins after games with expected probability.

    Arguments:
    -- wins = number of wins for a particular player or player group
    -- rounds = total number of rounds played by player(s)
    -- prob_win = the fixed probability of getting a single win

    In a binomeal distribution, 1 - prob_win is the probability of a single
    loss. The probability mass function is:

                rounds
    f(wins) = (  wins  ) p^wins (1 - p)^(rounds - wins) ,

    where:
    p = prob_win, the fixed probability of a single win

    This is used to calculate the chance of getting the amount of even wins
    (wins) that the player has. Even wins means a win that pays out at even
    odds (1:2), so any win that is not a natural/blackjack. It assumes that the
    wins follow a binomeal distribution.

    The default probability of winning is for even wins, taken as a standard
    0.4222 chance of winning, minus 0.048 chance of getting blackjack, so:
    chance_win - chance_blackjack = chance_even_odds_win

    Can be used to determine chance of push, win etc, where there is an
    approximate fixed expected change of that result (win/push).
    """
    # TODO: this returns just the probability of that score, I'd like to return
    # the probability of AT LEAST that score, or a +- sd
    prob_loss = (1 - prob_win)**(rounds - wins)
    return prob_win**wins * prob_loss * comb(rounds, wins)


def standard_dev_fixed_percent(rounds, prob_win):
    """Calculate the standard deviation of a binomial distribution."""

    return sqrt(rounds * prob_win * (1 - prob_win))


def chance_at_least_result(wins, rounds):
    """Calculate the chance of getting at least wins many wins in these rounds.

    If you do 2 rounds, with 1 win, return the total chance of getting either
    1 or 2 wins, but not 0 wins.

    Calculated by: 1 - sum([chance_0,... chance_n])
    where:
    chance_0 is the chance of getting 0 wins
    chance_n is the chance of getting n wins, with n = actual wins - 1
    """

    chances = [chance_with_fixed_percent(w, rounds) for w in range(wins)]
    return 1 - sum(chances)
