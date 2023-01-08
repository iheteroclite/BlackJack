"""Tests to ensure specification compliance for people classes.

To run cli tests: $ python3 -m unittest discover test
"""

__version__ = 0.40
__author__ = 'iheteroclite'

import unittest

from src.deck import Deck, Card, suits, faces
from src.hand import Hand
from src.people import Player, Dealer
from blackjack import check_twenty_one, score_hand


class PeopleTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        self.deck = Deck()

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_player_auto_names(self):
        num_players = 4
        players = ''
        for i in range(num_players):
            player_str = f'Player {i + 1}'
            player = Player(self.deck, player_str)
            players += player.name
        self.assertEqual(players, 'Player 1Player 2Player 3Player 4')


