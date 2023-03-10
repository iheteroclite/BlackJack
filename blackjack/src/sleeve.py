"""The sleeve holds all hidden cards that the user may use when cheating.

Every cheat needs a long sleeve, and this is yours!

During a game, if a player decies to cheat they would hide cards up their
sleeve, then swap them with cards later in the game. The cards that the player
used are now marked.
"""

__version__ = 1.00
__author__ = 'iheteroclite'
__all__ = []

from random import randint

from library.io import card_string, player_choice
from src.deck import faces, suits, Card


class Sleeve:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.hide_cards()

    def __str__(self):
        return f'{self.name}, Your sleeve hides:\n' + card_string(self.cards)

    def hide_cards(self):
        num_in_sleeve = player_choice('sleeved cards', 1, [1, 2, 3])

        for i in range(num_in_sleeve):
            query = f'{self.name}, Select sleeve card {i + 1}'

            # Player chooses the card value, and the suit is pseudorandom
            card_face = player_choice(query, 3, options=faces)
            card_suit = suits[randint(0, len(suits) - 1)]

            self.cards.append(Card(card_suit, card_face, cheat_card=True))

    def mark_cheat_cards(self):
        for card in self.cards:
            card.cheat_card = True
