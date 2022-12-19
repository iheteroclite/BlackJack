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


if __name__ == '__main__':
    unittest.main()
