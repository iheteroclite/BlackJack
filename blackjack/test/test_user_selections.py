"""Tests to ensure specification compliance for game options.

To run cli tests: $ python3 -m unittest discover test
"""

__version__ = 0.40
__author__ = 'iheteroclite'

from unittest import mock
from unittest import TestCase

import blackjack
import library.io
from src.people import Dealer, Player


class UserSelectionTestCase(TestCase):
    @mock.patch('blackjack.player_choice', create=True)

    def test_user_choice_game_setup(self, mocked_input):
        input_lists = [[4, 11, 3],
                       [1, 1, 7],
                       [2, 'Player chooses', 8],
                       [3, 11, 4],
                       [5, 'Player chooses', 6],
                       [5, 11, 5]]
        for inputs in input_lists:

            player_input = inputs[0]
            ace_input = inputs[1]
            deck_input = inputs[2]
            mocked_input.side_effect = [player_input, ace_input, deck_input]
            players, dealer, deck, num_decks, min_decks, ace, ace_choice = blackjack.game_setup()

            with self.subTest(player_input=player_input, ace=ace_input, deck=deck_input):
            # Test people
                for player in players:
                    with self.subTest(players):
                        self.assertTrue(isinstance(player, Player))
                self.assertEqual(len(players), player_input)
                self.assertTrue(isinstance(dealer, Dealer))

                # Test deck
                # Number of decks is correctly set
                self.assertEqual(num_decks, deck_input)
                # The number of cards in the deck is correct
                # (after 2 are drawn for each player and dealer)
                self.assertEqual((len(deck.cards) + len(players)*2 + 2)/ 52, deck_input)
                # The minimum deck size is either 1 or 2 52-card decks
                self.assertTrue(min_decks in [1, 2])

                # Test ace
                # Ace is equal to inputted value
                self.assertTrue(ace in [1, 11])
                # Ace choice is either True or False
                self.assertTrue(ace_choice in [True, False])
