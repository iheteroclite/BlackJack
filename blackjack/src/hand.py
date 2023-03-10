"""Class for the hand of player and the dealer in the game of blackjack.
"""

__version__ = 1.00
__author__ = 'iheteroclite'
__all__ = []

from library.io import card_string


class Hand:
    def __init__(self, deck, dealer=False):
        self.cards = deck.draw(2)
        self.dealer = dealer
        self.state = 'draw'     # records blackjack, twenty-one, bust
        self.success = 'tbd'

    def __str__(self):
        print('Hand contains:')
        return card_string(self.cards)

    def get_total(self):
        return sum([card.value for card in self.cards])

    # Keeping hit as a hand method, so game can be extended for multiple hands
    def hit(self, deck):
        self.state = 'playing'
        self.cards += deck.draw()

    def stand(self, condition='stand'):
        self.state = condition
