"""Tests to ensure specification compliance and test scores.

To run cli tests: $ python3 -m unittest discover test
"""

__version__ = 0.40
__author__ = 'iheteroclite'

import unittest

from src.deck import Deck, Card, suits, faces
from src.hand import Hand
from src.people import Player, Dealer
from blackjack import check_twenty_one, score_hand

class PlayAndScoreTestCase(unittest.TestCase):
    def setUp(self):  # this method will be run before each test
        self.deck = Deck()

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_receive_1_card_when_hit(self):
        my_hand = Hand(self.deck)
        old_hand_len = len(my_hand.cards)
        my_hand.hit(self.deck)
        self.assertEqual(len(my_hand.cards), (old_hand_len + 1))

    def test_score_updated_correctly_when_receive_card(self):
        """Calulate score after the dealer's turn.

        Uses the hand.get_score() method to calculate score.
        """
        hand = Hand(self.deck)

        hand.cards += [Card(suits[2], 7)]
        first_score = hand.get_total()
        hand.cards += [Card(suits[2], 'Jack')]
        self.assertEqual(hand.get_total(), (first_score + 10))

    def test_21_or_less_is_valid_hand(self):
        poss_scores = [i for i in range(1, 20)]
        player = Player(self.deck, 'Sash')
        for j, score in enumerate(poss_scores):
            player.hand.cards = [Card(suits[0], 1), Card(suits[1], score)]
            check = check_twenty_one(player)
            if player.hand.state in ['blackjack', 21]:
                check = False
            with self.subTest(score=score):
                self.assertFalse(check)

    def test_22_or_more_invalid_hand_bust(self):
        poss_scores = [i for i in range(2, 19)]
        player = Player(self.deck, 'Ali')
        for j, score in enumerate(poss_scores):
            player.hand.cards = [Card(suits[0], 10), Card(suits[0], 10),
                                 Card(suits[1], score)]
            check_twenty_one(player)
            with self.subTest(score=score + 20):
                self.assertIs(player.hand.state, 'bust')

    def test_king_and_ace_equals_blackjack(self):
        player = Player(self.deck, 'Alex')
        player.hand.cards = [Card(suits[0], 'King'), Card(suits[0], 'Ace')]
        check_twenty_one(player)
        self.assertEqual(player.hand.state, 'blackjack')

    def test_king_queen_ace_equals_21(self):
        player = Player(self.deck, 'Jo')
        player.hand.cards = [Card(suits[0], 'King'), Card(suits[0], 'Queen'),
                             Card(suits[0], 'Ace', 1)]
        player.hand.state = 'playing'
        check_twenty_one(player)
        self.assertEqual(player.hand.state, 21)

    def test_nine_ace_ace_equals_21(self):
        """Assumes the program accurately sets the ace value."""
        player = Player(self.deck, 'Sam')
        player.hand.cards = [Card(suits[0], 9), Card(suits[0], 'Ace'),
                             Card(suits[0], 'Ace', 1)]
        player.hand.state = 'playing'
        check_twenty_one(player)
        self.assertEqual(player.hand.state, 21)

    def test_correctly_set_selected_ace_vale(self):
        """Make a deck of aces, then test its value is 52 when ace is 1."""
        self.deck.cards = [Card(suits[0], faces[0], 1)] * 52
        self.assertEqual(sum([card.value for card in self.deck.cards]), 52)

    def test_win_loss_blackjack_push_updated(self):
        """Test that the player's score tallies are updated.

        Winning even odds, winning blackjack, losing, and pushing should
        be updated by exactly 1 each time that players wins/loses/pushes
        case[0] = player score
        case[1] = dealer score
        case[2] = result
        """
        cases = [['blackjack', '17', 'blackjack_wins'],
                 [21, 17, 'even_wins'],
                 [17, 21, 'losses'],
                 [18, 18, 'pushes']]
        player = Player(self.deck, 'player')
        dealer = Dealer(1, self.deck, 'dealer')
        for case in cases:
            init_score = getattr(player, case[2])
            player.hand.state = case[0]
            dealer.hand.state = case[1]
            score_hand(player, dealer)
            with self.subTest(player=case[0], dealer=case[1]):
                self.assertEqual(getattr(player, case[2]), init_score + 1)

    def test_new_player_has_two_cards(self):
        player = Player(self.deck, 'Bri')
        self.assertEqual(len(player.hand.cards), 2)

    def test_player_win_lose_conditions(self):
        """Test the accuracy of game scoring.

        Run the following tests:
        -- dealer blackjack beats player 21
        -- dealer bust beats player bust
        -- player blackjack ties dealer blackjack
        -- player blackjack beats dealer blackjack
        -- 19 beats 18
        -- 18 loses to 19
        -- dealer bust, player can win blackjack
        -- dealer bust, player can win even odds
        """
        player = Player(self.deck, 'Ash')
        dealer = Dealer(1, self.deck, 'dealer')
        # List [player.hand.state, dealer.hand.state, expected_result]
        tests = [[21, 'blackjack', 'loses'],
                 ['bust', 'bust', 'loses'],
                 ['blackjack', 'blackjack', 'pushes'],
                 ['blackjack', 21, 'wins blackjack'],
                 [19, 18, 'wins even'],
                 [18, 19, 'loses'],
                 ['blackjack', 'bust', 'wins blackjack'],
                 [19, 'bust', 'wins even'],]
        for test in tests:
            player.hand.state = test[0]
            dealer.hand.state = test[1]
            with self.subTest(player=test[0], dealer=test[1]):
                self.assertEqual(test[2], score_hand(player, dealer))

    def test_aces_new_deck(self):
        count = 0
        for card in self.deck.cards:
            if card.face == faces[0]:
                count += card.value

        self.assertEqual(count, 44)

