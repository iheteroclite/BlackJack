__version__ = 0.36
__author__ = 'iheteroclite'

from random import randint

from src.deck import faces, suits, Card
from src.hand import Hand
from src.sleeve import Sleeve
from library.statistics import chance_of_natural_blackjack
from library.statistics import chance_at_least_result
from library.statistics import chance_of_blackjack_totals
from library.statistics import chance_with_fixed_percent
from library.io import player_choice


class People:
    """SuperClass the Player and Dealer SubClasses."""

    def __init__(self, deck, name):
        self.name = name
        self.hands = [Hand(deck)]  # List of player hands
        self.hand = self.hands[0]  # Current hand in play
        # In the case of the dealer, these count all player's wins
        self.blackjack_wins = 0
        self.even_wins = 0
        self.losses = 0            # Includes bust, surrender, and loss
        self.pushes = 0
        # TODO: change the name games to rounds for consistency
        self.games = 0             # Number of rounds played

    def reset(self, deck):
        self.hands = [Hand(deck)]
        self.hand = self.hands[0]

    def __str__(self, name, scored, multiple, bj_chance='', even_chance=''):
        wins = self.blackjack_wins + self.even_wins

        return ('_' * 52
                + f'\n{name}, over {self.games} rounds {scored}:'
                + f'\nWins: {wins} '
                + f'({round(100 * wins / (self.games * multiple), 1)} %) '
                + f'with {self.blackjack_wins} blackjack {bj_chance}'
                + f'and {self.even_wins} even payouts {even_chance}\n'
                + f'Losses: {self.losses}       Pushes: {self.pushes}')


class Player(People):
    """Players are users.

    Player extends the People superclass.
    """

    def __init__(self, deck, name):
        """Initialise Player.

        Store the probability of getting blackjack for every round as dict:
        {
            'probability' = prob,
            'blackjack' = False
        }
        where prob is a number, the probability of drawing blackjack for that
        hand.
        Calculate probability of blackjack BEFORE drawing cards.
        """
        prob = chance_of_natural_blackjack(deck)
        self.probabilities = [{
            'probability': prob,
            'blackjack': False
        }]
        super().__init__(deck, name)
        self.cheater = False
        # Sleeve is the cards up a player's sleeve (for cheating)
        self.sleeve = None
        self.chance_bj = 0
        self.chance_even = 0
        self.tot_chance_bj = 0
        self.tot_chance_even = 0

    def __str__(self):
        # Strings to add for displaying player probabilities
        bj = ''
        even = ''
        # TODO: make this do both?
        # for chance in [bj, 'chance_even']:
        #     if self[chance]:
        #         perc = round((self[chance] * 100), 1)
        #         tot_perc = round((self['tot_' + chance] * 100), 1)

        if self.chance_bj:
            bj_perc = round((self.chance_bj * 100), 1)
            tot_bj_perc = round((self.tot_chance_bj * 100), 1)

            bj = (f'(at {bj_perc} % chance)\n' + ' '*16
                  + f'[with {tot_bj_perc} % chance of at '
                  + f'least {self.blackjack_wins}]\n' + ' '*16)

        if self.chance_even:
            even_perc = round((self.chance_even * 100), 1)
            tot_even_perc = round((self.tot_chance_even * 100), 1)

            even = (f'(at {even_perc} % chance)\n' + ' '*16
                    + f'[with {tot_even_perc} % chance of at '
                    + f'least {self.even_wins}]')

        return super().__str__(self.name, 'you have scored', 1, bj, even)

    def reset(self, deck):
        prob = chance_of_natural_blackjack(deck)
        self.probabilities.append({
            'probability': prob,
            'blackjack': False
        })
        super().reset(deck)

    def calculate_probability(self):
        # Probability of getting exactly this many bj/win in rounds so far
        # TODO*: probability of this hand getting what it got
        # self.chance_bj = 1 - self.probabilities[-1]['probability']
        self.chance_bj = chance_of_blackjack_totals(self.probabilities)
        self.chance_even = chance_with_fixed_percent(self.even_wins,
                                                     self.games)
        # Probability of getting at least this many bj/win in rounds so far
        self.tot_chance_bj = chance_of_blackjack_totals(self.probabilities,
                                                        at_least=True)
        self.tot_chance_even = chance_at_least_result(self.even_wins,
                                                      self.games)

    def hide_cards(self):
        """Hide cards up player's sleeve so they can use them to cheat."""
        self.sleeve = Sleeve(self.name)
        print(self.sleeve)

    def cheat(self):
        pass


class Dealer(People):
    r"""Dealer is an automated Dealer

    Dealer extends the People superclass.
    An instance of Dealer counts all even or blackjack wins,
    pushes and losses of every player at the table as a tally.
    """

    def __init__(self, num_players, deck, name="Dealer"):
        super().__init__(deck, name)
        self.hand.dealer = True
        self.num_players = num_players

    def __str__(self):
        return super().__str__('All players', 'scored a total of',
                               self.num_players)

    def set_coeff(self):
        """Set the cheat coefficient.

        The cheat coefficient cheat_coeff represents the maximum chance of the
        dealer catching a player when they cheat."""
        dealers = {
            'Big Brother': 0.6,
            'Casino Cat': 0.4,
            'Sharp-Eyed Stacy': 0.3,
            'Happy Harry': 0.2,
            'Grandma Gertrude': 0.1,
            'Blind Bob': 0.05,
        }
        self.cheat_coeff = dealers[self.name]
