__version__ = 0.36
__author__ = 'iheteroclite'

import unittest
import random

from src.deck import Deck, Card, suits, faces
from src.people import Player
from blackjack import check_twenty_one
from library.statistics import chance_of_blackjack_totals
from library.hypergeometric_distribution import chance_n_blackjack_total
from library.statistics import chance_with_fixed_percent
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

    def test_chance_n_blackjack_total_calculation(self):
        deck = Deck()
        # Take 5 hands from deck
        player = Player(deck, 'player1')
        for i in range(5):
            check_twenty_one(player.hand)
            if player.hand.state == 'blackjack':
                player.probabilities[-1]['blackjack'] = True
            player.reset(deck)

        n_bjs = sum([1 for result in player.probabilities if result['blackjack']])

        player.probabilities.pop(-1)
        P_n, P_at_least_n = chance_n_blackjack_total(player.probabilities, n_bjs)
        self.assertLess(n_bjs , 5)
        self.assertGreater(n_bjs, -1)
        self.assertEqual(len(player.probabilities), 5)
        self.assertTrue(P_n)

        self.assertGreater(P_n, 0)
        self.assertGreater(P_at_least_n, 0)
        self.assertLess(P_n, 1.001)
        self.assertLess(P_at_least_n, 1.001)

    def test_chance_n_blackjack_total_zero_with_no_ace(self):
        deck = Deck()
        for card in deck.cards:
            card.face = 3

        # Take 5 hands from deck
        player = Player(deck, 'player1')
        for i in range(5):
            check_twenty_one(player.hand)
            if player.hand.state == 'blackjack':
                player.probabilities[-1]['blackjack'] = True
            player.reset(deck)

        player.probabilities.pop(-1)
        print('player probs in test_statistics', player.probabilities)
        P_n, P_at_least_n = chance_n_blackjack_total(player.probabilities, 1)

        self.assertEqual(P_n, 0)
        self.assertEqual(P_at_least_n, 0)

    def test_chance_n_blackjack_total_50_50_ace_ten(self):
        deck = Deck()
        for i, card in enumerate(deck.cards):
            if i % 2:
                card.face = faces[0]
                card.value = 11
            else:
                card.face = 10
                card.value = 10

            with self.subTest(card_no=i,card=card):
                self.assertTrue(card.face in [faces[0], 10])
                self.assertTrue(card.value in [10,11])

        # Take 10 hands from deck
        player = Player(deck, 'player1')
        for i in range(12):
            check_twenty_one(player.hand)
            if player.hand.state == 'blackjack':
                player.probabilities[-1]['blackjack'] = True
            player.reset(deck)

        player.probabilities.pop(-1)
        print('player probs in test_statistics', player.probabilities)

        # Probability of getting one blackjack in 50/50 ace/ten deck is ~0.5
        x = 0
        for i in range(10):
            P_n, P_at_least_n = chance_n_blackjack_total([player.probabilities[i]], 1)
            # if i % 2:
            #     x += 1
            # P_n1, P_at_least_n1 = chance_n_blackjack_total(player.probabilities, x)

            with self.subTest(i=i, x=x):
                self.assertLess(x, 6)
                self.assertGreater(x, -1)
                self.assertEqual(round(P_n, 1), 0.5)
                self.assertEqual(round(P_at_least_n, 1), 0.5)
                # self.assertEqual(round(P_n1, 1), 0.5)
                # self.assertEqual(round(P_at_least_n1, 1), 0.5)

    def test_chance_n_blackjack_total_pulling_bj_each_draw(self):
        """Check known probability to draw 4 sets of blackjacks.

        As the probability of drawing n_bjs blackjacks each turn varies,
        as the number and value of cards and (possibly) also the number
        of tens/aces varies each turn, calculating probability of having
        drawn n_bjs over multiple rounds is a very complex problem.

        I have therefore modelled my formula in Mathematica, which is
        documented in the project documentation. I have used the output

        """
        # deck1 is a dummy deck for players to draw cards from
        deck1 = Deck()
        # deck2 will have an ace and 10 value removed each turn, for probability
        deck2 = Deck()

        tens_removed = 0
        aces_removed = 0
        # Get player to draw 4 times, and change their hand to blackjack
        # Then remove blackjack cards from deck2, calculating P(b) with deck2
        player = Player(deck1, 'player1')
        for i in range(4):
            remove_ace = True
            remove_ten = True
            for card in deck2.cards:
                if remove_ace and card.value in [11,1]:
                    deck2.cards.remove(card)
                    aces_removed += 1
                    remove_ace = False
                if remove_ten and card.value == 10:
                    deck2.cards.remove(card)
                    tens_removed += 1
                    remove_ten = False
            player.hand.cards = [Card('♣', 'Ace', 11), Card('♣', 10)]
            check_twenty_one(player.hand)
            if player.hand.state == 'blackjack':
                player.probabilities[-1]['blackjack'] = True
            deck2_chance = chance_of_single_blackjack(deck2)
            player.probabilities[-1]['probability'] = deck2_chance
            player.reset(deck1)

        # Get probability for final draw
        deck2_chance = chance_of_single_blackjack(deck2)
        player.probabilities[-1]['probability'] = deck2_chance

        self.assertEqual(len(deck2.cards), 44)
        self.assertEqual(aces_removed, 4)
        self.assertEqual(tens_removed, 4)

        deck2.cards.pop(0)
        deck2.cards.pop(0)

        self.assertEqual(len(deck1.cards), len(deck2.cards))

