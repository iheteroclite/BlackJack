__version__ = 0.36
__author__ = 'iheteroclite'

from src.hand import Hand
from library.statistics import chance_of_natural_blackjack
from library.statistics import chance_with_fixed_percent


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
        # Store the probability of getting blackjack for every round as dict:
        # {
        #     'probability' = 0.048,
        #     'blackjack' = False
        # }
        # Calculate probability of blackjack BEFORE drawing cards
        prob = chance_of_natural_blackjack(deck)
        self.probabilities = [{
            'probability': prob,
            'blackjack': False
        }]
        super().__init__(deck, name)
        # Sleeve is the cards up a player's sleeve (for cheating)
        self.sleeve = None
        self.chance_bj = None
        self.chance_even = None

    def __str__(self):
        # Strings to add for displaying player probabilities
        if self.chance_bj:
            bj_perc = round((self.chance_bj * 100), 1)
            bj = f'(at {bj_perc} % chance)' + '\n' + ' ' * 16
        else:
            bj = ''

        if self.chance_even:
            even_perc = round((self.chance_even * 100), 1)
            even = f'(at {even_perc} % chance)'
        else:
            even = ''

        return super().__str__(self.name, 'you have scored', 1, bj, even)

    def reset(self, deck):
        prob = chance_of_natural_blackjack(deck)
        self.probabilities.append({
            'probability': prob,
            'blackjack': False
        })
        super().reset(deck)

    def calculate_probability(self):
        self.chance_bj = self.probabilities[-1]['probability']
        self.chance_even = chance_with_fixed_percent(self.even_wins,
                                                     self.games)

    def hide_cards():
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
