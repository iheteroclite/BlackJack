import unittest
from src.deck import Deck
from src.hand import Hand


class DeckTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        self.deck = Deck()

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_number_of_cards(self):  # any method beginning with 'test' will be run by unittest
        number_of_cards = len(self.deck.cards)
        # check there's up to 8 decks in the deck :)
        self.assertTrue(number_of_cards in [52*n for n in range(8)])

    def test_cards_integer_value(self):
        card_int_val_truth = True
        for card in self.deck.cards:
            if not 1 <= card.value <= 11:
                card_int_val_truth *= False
            elif card.value % 1 != 0: #test for integer
                card_int_val_truth *= False
        self.assertTrue(card_int_val_truth)

    def test_player_auto_names(self):
        num_players = 2
        player_list = ''
        player_hands = [Hand(self.deck, f'Player {x + 1}', 'player') for x in range(num_players) ]
        for i in range(num_players):
            player_list += player_hands[i].player
        self.assertEqual(player_list, 'Player 1Player 2')

    def test_number_deck_cards_after_draws(self):
        num_players = 2
        player_list = ''
        player_hands = [Hand(self.deck, f'Player {x + 1}', 'player') for x in range(num_players) ]
        self.deck.draw()
        self.assertEqual(len(self.deck.cards), 47)



if __name__ == '__main__':
    unittest.main()
