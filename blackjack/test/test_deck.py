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
       self.assertEqual(suit_list, [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]*4 )

    def test_card_ace_value_one_or_eleven(self):
        aces = [Card(suits[1], faces[0])]
        aces.append(Card(suits[1], faces[0], 1))
        aces.append(Card(suits[1], faces[0], 11))
        values = [ace.value for ace in aces]
        aces[1].set_ace_value(11)
        aces[0].set_ace_value(1)
        aces[2].set_ace_value(1)
        values.append([ace.value for ace in aces])
        self.assertEqual(values, [11, 1, 11, [1, 11, 1]])

    def test_deck_ace_value_one_or_eleven(self):
        # make a deck with ace_value=1, and a deck for ace_val=11
        # test they have correct ace values
        truth = [0]*3
        values = [11, 1, 11]
        decks = [Deck(), Deck(1, values[1]), Deck(1, values[2])]
        for i, deck in enumerate(decks):
            for card in deck.cards:
                truth[i] += 1 if (card.face == 'Ace' and card.value == values[i]) else 0
        self.assertEqual(truth, [4]*3)

    def test_receive_1_card_when_hit(self):
        pass

    def test_score_updated_when_receive_card(self):
        pass

    def test_21_or_less_is_valid)hand(self):
        pass

    def test_22_or_more_invalid_hand_bust(self):
        pass


    def test_king_and_ace_equals_blackjack(self):
        pass

    def test_king_queen_ace_equals_21(self):
        pass

    def test_nine_ace_ace_equals_21(self):
        pass


    # once all these tests are written, and comments cleared up,
    # issues raised on github, create Version 1

if __name__ == '__main__':
    unittest.main()
