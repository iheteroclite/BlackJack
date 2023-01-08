__version__ = 0.40
__author__ = 'iheteroclite'

import unittest

from src.deck import Deck, Card
from src.people import Player
from blackjack import check_twenty_one


class ProbabilitiesTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        self.deck = Deck()
        self.player = Player(self.deck, 'player')

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_probabilities_update_after_blackjack(self):
        # TODO: remove repitition

        self.player.hand.cards = [Card('♣', 'Ace', 9),
                                  Card('♣', 10),
                                  Card('♣', 2)]
        self.player.hand.state = 'playing'
        check_twenty_one(self.player)
        self.player.reset(self.deck)
        self.player.hand.cards = [Card('♣', 'Ace', 11),
                                  Card('♣', 10)]
        check_twenty_one(self.player)
        self.player.reset(self.deck)
        self.player.hand.cards = [Card('♣', 'Ace', 9),
                                  Card('♣', 2)]
        check_twenty_one(self.player)
        self.player.reset(self.deck)
        self.player.hand.cards = [Card('♣', 'Ace', 11),
                                  Card('♣', 10)]
        check_twenty_one(self.player)
        self.player.reset(self.deck)

        bjs = [1 for prob in self.player.probabilities if prob['blackjack']]
        bj_count = len(bjs)

        self.assertEqual(bj_count, 2)
        self.assertEqual(len(self.player.probabilities), 5)
