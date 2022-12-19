import unittest
from src.deck import Deck


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



if __name__ == '__main__':
    unittest.main()
