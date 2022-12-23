import unittest
from src.deck import Deck, Card, suits, faces
from src.hand import Hand

#python3 -m unittest discover test

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

    def test_number_card_worth_its_value(self):
        card_values = [Card(suits[0], face=x).value for x in range(2,10)]
        self.assertEqual(card_values, [2, 3, 4, 5, 6, 7, 8, 9])

    def test_king_queen_jack_worth_ten(self):
        card_values = [Card(suits[1], face).value for face in faces[10:]]
        self.assertEqual(card_values, [10]*3)

    def test_suit_inconsequential_to_face(self):
        suit_list = [Card(suits[0], face).face for suit in suits for face in faces]
        self.assertEqual(suit_list, faces*4)


    def test_suit_inconsequential_to_value(self):
        suit_list = [Card(suits[0], face).value for suit in suits for face in faces]
        #self.assertEqual(suit_list, [11,
        # ^ this needs to be a list of all the values

if __name__ == '__main__':
    unittest.main()
