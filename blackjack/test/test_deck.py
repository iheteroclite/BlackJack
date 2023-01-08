"""Tests to ensure specification compliance and test functionality.

To run cli tests: $ python3 -m unittest discover test
"""

__version__ = 0.40
__author__ = 'iheteroclite'

import unittest

from src.deck import Deck, Card, suits, faces
from src.hand import Hand
from src.people import Player, Dealer
from blackjack import check_twenty_one, score_hand


class DeckTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        self.deck = Deck()

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_number_of_cards(self):
        decks = [Deck(d) for d in range(1, 8)]
        # check there's up to 8 decks in the deck
        for no_of_decks in range(1, 8):
            deck = Deck(no_of_decks)
            number_of_cards = len(deck.cards)
            with self.subTest(no_of_decks=no_of_decks):
                self.assertEqual(number_of_cards, 52 * no_of_decks)

    def test_cards_integer_value(self):
        for card in self.deck.cards:
            with self.subTest(fail_card=f"{card.suit}, {card.face}"):
                self.assertTrue((1 <= card.value <= 11)
                                and (card.value % 1 == 0))

    def test_number_deck_cards_after_draws(self):
        num_players = 2
        hands = [Hand(self.deck) for x in range(num_players)]
        self.deck.draw()
        self.assertEqual(len(self.deck.cards), 47)

    def test_number_card_worth_its_value(self):
        card_values = [Card(suits[0], face=x).value for x in range(2, 10)]
        self.assertEqual(card_values, [2, 3, 4, 5, 6, 7, 8, 9])

    def test_king_queen_jack_worth_ten(self):
        card_values = [Card(suits[1], face).value for face in faces[10:]]
        self.assertEqual(card_values, [10] * 3)

    def test_suit_inconsequential_to_face(self):
        suit_list = [Card(suits[0], face).face
                     for suit in suits for face in faces]
        self.assertEqual(suit_list, faces * 4)

    def test_suit_inconsequential_to_value(self):
        suit_list = [Card(suits[0], face).value
                     for suit in suits for face in faces]
        self.assertEqual(suit_list,
                         [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4)

    def test_card_ace_value_one_or_eleven(self):
        # TODO: make this use subTest
        aces = [Card(suits[1], faces[0])]
        aces.append(Card(suits[1], faces[0], 1))
        aces.append(Card(suits[1], faces[0], 11))
        for i, x in enumerate([1, 11, 1]):
            aces[i].set_ace_value(x)
            with self.subTest(ace=(f'index {i}, value {x}')):
                self.assertEqual(aces[i].value, x)

    def test_deck_ace_value_one_or_eleven(self):
        # make a deck with ace_value=1, and a deck for ace_val=11
        # test they have correct ace values
        truth = [0] * 3
        values = [11, 1, 11]
        decks = [Deck(), Deck(1, values[1]), Deck(1, values[2])]
        for i, deck in enumerate(decks):
            for card in deck.cards:
                truth[i] += 1 if (card.face == 'Ace'
                                  and card.value == values[i]) else 0
        self.assertEqual(truth, [4] * 3)


if __name__ == '__main__':
    unittest.main()
