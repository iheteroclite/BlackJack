__version__ = 1.00
__author__ = 'iheteroclite'

import unittest
import random

from src.deck import Deck, Card, faces
from library.statistics import chance_of_blackjack_totals
from library.statistics import chance_with_fixed_percent
from library.statistics import chance_at_least_mean_blackjack
from library.statistics import chance_of_single_blackjack


class StatisticsTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        pass

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_chance_of_blackjack_totals_less_than_unexpected(self):
        """Check maximum input probability is not exceeded."""
        probs = range(1, 10, 1)
        trues = [1, 0] * 5
        results = [{
                   'probability': prob / 10,
                   'blackjack': true
                   } for prob, true in zip(probs, trues)]
        self.assertGreater(0.05, chance_of_blackjack_totals(results))

    def test_chance_of_blackjack_totals_greater_than_zero(self):
        probs = range(1, 10, 1)
        results = [{
                   'probability': prob / 100,
                   'blackjack': random.getrandbits(1),
                   } for prob in probs]
        self.assertGreater(chance_of_blackjack_totals(results), 0)

    def test_chance_with_fixed_percent_calculation(self):
        """Test the formula for calculating chance using a fixed percentage."""
        even = chance_with_fixed_percent(wins=5, rounds=10, prob_win=0.5)
        self.assertAlmostEqual(even, 0.24609374)

    def test_chance_with_fixed_percent_zero(self):
        """Check if expected percentage is 0%, the chance of 50% wins is 0."""
        zero = chance_with_fixed_percent(wins=5, rounds=10, prob_win=0)
        self.assertEqual(zero, 0)

    def test_chance_of_blackjack_zero_if_no_aces(self):
        """Check chance of blackjack for deck without aces is 0."""
        deck = Deck()
        deck.cards = [Card('♣', random.randrange(2, 10)) for x in range(52)]
        self.assertEqual(0, chance_of_single_blackjack(deck=deck))

    def test_chance_of_blackjack_zero_if_no_tens(self):
        """Check chance of blackjack for deck without aces is 0."""
        deck = Deck()
        deck.cards = [Card('♣', random.randrange(2, 9)) for x in range(52)]
        # Add an ace:
        deck.cards.append(Card('♣', faces[0]))
        self.assertEqual(0, chance_of_single_blackjack(deck=deck))

    def test_chance_of_blackjack_four_point_eight(self):
        """Check the chance of blackjack for newly shuffled deck is 4.8%."""
        probs = [0.047, 0.048]
        for n in range(1, 8):
            deck = Deck(n)
            with self.subTest(n_decks=n):
                chance = round(chance_of_single_blackjack(deck), 3)
                self.assertTrue(chance in probs)

    def test_chance_blackjack_totals_unity(self):
        results = [{
                   'probability': 1,
                   'blackjack': random.getrandbits(1),
                   } for i in range(10)]

        chance = chance_at_least_mean_blackjack(results)
        self.assertEqual(chance, 1)

    def test_chance_at_least_mean_blackjack_half(self):
        bjs = [True, False] * 5
        probs = [1, 0] * 5
        results = [{
                   'probability': probs[i],
                   'blackjack': bjs[i],
                   } for i in range(10)]

        chance = chance_at_least_mean_blackjack(results)

        self.assertGreater(chance, 0.5)

    def test_chance_at_least_mean_blackjack_one_bj(self):
        results = [{
                   'probability': 0.048,
                   'blackjack': False,
                   } for i in range(5)]

        results[0]['blackjack'] = True

        chance = chance_at_least_mean_blackjack(results)

        self.assertLess(chance, 0.999)
        self.assertGreater(chance, 0.001)

    def test_chance_at_least_mean_blackjack__fixed_50_percent_bj(self):
        results = [{
                   'probability': 0.5,
                   'blackjack': False,
                   } for i in range(5)]

        results[0]['blackjack'] = True

        chance = chance_at_least_mean_blackjack(results)

        self.assertLess(chance, 0.999)
        self.assertGreater(chance, 0.001)

    def test_chance_at_least_mean_blackjack_two_bj(self):
        results = [{
                   'probability': 0.048,
                   'blackjack': False,
                   } for i in range(10)]

        results[0]['blackjack'] = True
        results[-1]['blackjack'] = True

        chance = chance_at_least_mean_blackjack(results)

        self.assertLess(chance, 0.999)
        self.assertGreater(chance, 0.001)
