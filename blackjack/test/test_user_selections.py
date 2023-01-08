"""Tests to ensure specification compliance for game options.

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
        pass

    def tearDown(self):  # this method will be run after each tests
        pass