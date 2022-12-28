import unittest
from src.deck import Deck, Card, suits, faces
from src.hand import Hand
from blackjack import check_twenty_one
#python3 -m unittest discover test

class DeckTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        self.deck = Deck()
        self.deck_new = Deck(1, 20)

    def tearDown(self):  # this method will be run after each tests
        pass

    def test_number_of_cards(self):  # any method beginning with 'test' will be run by unittest
        number_of_cards = len(self.deck.cards)
        # check there's up to 8 decks in the deck :)
        self.assertTrue(number_of_cards in [52*n for n in range(8)])

    def test_cards_integer_value(self):
        for card in self.deck.cards:
            with self.subTest(fail_card = f"{card.suit}, {card.face}"):
                self.assertTrue((1 <= card.value <= 11) and (card.value % 1 == 0))

    def test_player_auto_names(self):
        num_players = 4
        for i in range(num_players):
            player_str = f'Player {i + 1}'
            hand = Hand(self.deck, player_str, 'player')
            with self.subTest(player=player_str):
                self.assertEqual(hand.player, player_str)

    def test_number_deck_cards_after_draws(self):
        num_players = 2
        hands = [Hand(self.deck, f'P{x}', 'player') for x in range(num_players)]
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
        # TODO: make this use subTest
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
        my_hand = Hand(self.deck, 'bob')
        old_hand_len = len(my_hand.cards)
        my_hand.hit(self.deck)
        self.assertEqual(len(my_hand.cards), (old_hand_len + 1))

    def test_score_updated_correctly_when_receive_card(self):
        '''This program calulates score after the dealer's turn
        so this tests the function of hand.get_score() to calculate score '''
        hand = Hand(self.deck, 'jim')
        initial_score = hand.get_total()

        hand.cards += [ Card(suits[2], 7)]
        first_score = hand.get_total()
        hand.cards += [Card(suits[2], 'Jack')]
        self.assertEqual(hand.get_total(), (first_score + 10) )

    def test_21_or_less_is_valid_hand(self):
        poss_scores = [i for i in range(1, 20)]
        hand = Hand(self.deck, 'alice')
        for j, score in enumerate(poss_scores):
            hand.cards = [Card(suits[0], 1), Card(suits[1], score)]
            check = check_twenty_one(hand)
            if check == 'blackjack' or check == 21:
                check = False
            with self.subTest(score=score):
                self.assertFalse(check)

    def test_22_or_more_invalid_hand_bust(self):
        poss_scores = [i for i in range(2, 19)]
        hand = Hand(self.deck, 'jane')
        for j, score in enumerate(poss_scores):
            hand.cards = [Card(suits[0], 10), Card(suits[0], 10), Card(suits[1], score)]
            check = check_twenty_one(hand)
            with self.subTest(score=score):
                self.assertIs(check, 'bust')

    def test_king_and_ace_equals_blackjack(self):
        hand = Hand(self.deck, 'bri')
        hand.cards = [Card(suits[0], 'King'), Card(suits[0], 'Ace')]
        score = check_twenty_one(hand)
        self.assertEqual(score, 'blackjack')

    def test_king_queen_ace_equals_21(self):
        hand = Hand(self.deck, 'tom')
        hand.cards = [Card(suits[0], 'King'), Card(suits[0], 'Queen'), Card(suits[0], 'Ace', 1)]
        hand.state = 'playing'
        score = check_twenty_one(hand)
        self.assertEqual(score, 21)

    def test_nine_ace_ace_equals_21(self):
        '''Assumes the program accurately sets the ace value '''
        hand = Hand(self.deck, 'zoe')
        hand.cards = [Card(suits[0], 9), Card(suits[0], 'Ace'), Card(suits[0], 'Ace', 1)]
        hand.state = 'playing'
        score = check_twenty_one(hand)
        self.assertEqual(score, 21)

    def test_correctly_set_selected_ace_vale(self):
        '''Makes a deck of aces, initialises the input  '''
        pass

if __name__ == '__main__':
    unittest.main()
