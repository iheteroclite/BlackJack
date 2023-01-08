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
from src.deck import Card, Deck, faces


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

            ace_card = Card('Hearts', faces[0], ace_value=ace)

            with self.subTest(player_input=player_input, ace=ace_input, deck=deck_input):
                # Test number of players
                # Test players are all players
                # Test dealer is a dealer
                for player in players:
                    with self.subTest(players):
                        self.assertTrue(isinstance(player, Player))
                        self.assertEqual(len(player.hand.cards), 2)
                self.assertEqual(len(players), player_input)
                self.assertTrue(isinstance(dealer, Dealer))

                # Test deck
                # Number of decks is correctly set
                self.assertEqual(num_decks, deck_input)
                # The number of cards in the deck is correct
                # (after 2 are drawn for each player and dealer)
                deck_add_cards = (len(deck.cards) + len(players) * 2 + 2) / 52
                self.assertEqual(deck_add_cards, deck_input)
                # The minimum deck size is either 1 or 2 52-card decks
                self.assertTrue(min_decks in [1, 2])

                # Test ace
                # Ace is equal to inputted value
                self.assertTrue(ace in [1, 11])
                # Ace choice is either True or False
                self.assertTrue(ace_choice in [True, False])
                # The card created with the ace value has value of 1 or 11
                self.assertEqual(ace_card.value, ace)

    # def test_hit_player_choice_receives_card(self, mocked_input):
    #     player_input = 1
    #     ace_input = 11
    #     deck_input = 2
    #     mocked_input.side_effect = [player_input, ace_input, deck_input, 'Heavens no!']
    #     blackjack.play()

    @mock.patch('blackjack.player_choice', create=True)
    @mock.patch('blackjack.check_twenty_one', return_value=False)
    def test_player_receives_card_when_hit(self, mock_check_21, mocked_input):
        # Create initialised values for test
        deck = Deck()
        dealer = Dealer(1, deck)
        players = [Player(deck, 'Player 1')]
        ace_choice = False
        players[0].cheater = False
        initial_num_cards = len(players[0].hand.cards)
        initial_score = players[0].hand.state

        # Set the mocked input for game_round()
        mocked_input.side_effect = ['OK', 'yes', 'hit', 'stand']
        # Play the round,
        # even if the score goes over 21, check_twenty_one is mocked to return false
        blackjack.game_round(dealer, players, deck, ace_choice)
        final_num_cards = len(players[0].hand.cards)
        final_score = players[0].hand.state

        self.assertEqual(initial_num_cards + 1, final_num_cards)
        self.assertNotEqual(initial_score, final_score)

    @mock.patch('blackjack.player_choice', create=True)
    @mock.patch('blackjack.check_twenty_one', return_value=False)
    def test_player_receives_cards_and_score_on_stand(self, mock_check_21, mocked_input):
        # Create initialised values for test
        deck = Deck()
        dealer = Dealer(1, deck)
        players = [Player(deck, 'Player 1')]
        ace_choice = False
        players[0].cheater = False
        initial_num_cards = len(players[0].hand.cards)
        initial_score = players[0].hand.state

        # Set the mocked input for game_round()
        mocked_input.side_effect = ['OK', 'yes', 'stand']
        # Play the round,
        # even if the score goes over 21, check_twenty_one is mocked to return false
        blackjack.game_round(dealer, players, deck, ace_choice)
        final_num_cards = len(players[0].hand.cards)
        final_score = players[0].hand.state

        # Calculate the total of player's hand manually
        player_total = sum([card.value for card in players[0].hand.cards])

        self.assertEqual(initial_num_cards, final_num_cards)
        self.assertEqual(players[0].hand.state, player_total)
