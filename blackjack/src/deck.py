"""Classes required for creating a deck and populating it with cards.

This is made specifically for the game of blackjack, where aces can be
worth 1 or 11.
"""

__version__ = 1.00
__author__ = 'iheteroclite'
__all__ = []

from random import shuffle

suits = ['\033[91m♦\033[00m', '♣', '\033[91m♥\033[00m', '♠']
faces = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
         'Jack', 'Queen', 'King']


class Card:
    def __init__(self, suit, face, ace_value=11, cheat_card=False):
        self.suit = suit
        self.face = face
        self.value = 0
        self.cheat_card = cheat_card
        try:
            self.value = int(self.face)
        except:
            if self.face == faces[0]:
                if ace_value == 1:
                    self.value = 1
                else:
                    self.value = ace_value
            elif self.face in faces[10:]:
                self.value = 10

    def __str__(self):
        return f'{self.face} of {self.suit}'

    def set_ace_value(self, ace_value):
        self.value = ace_value


class Deck:
    def __init__(self, n_decks=1, ace=11):
        if n_decks > 8:
            n_decks = 8
        self.cards = [Card(s, f, ace) for s in suits for f in faces] * n_decks
        self.shuffle_deck()

    def shuffle_deck(self):
        shuffle(self.cards)

    def draw(self, n_cards=1):
        return [self.cards.pop(0) for c in range(n_cards)]
