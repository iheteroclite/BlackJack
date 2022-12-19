import random

suits = ['diamonds', 'clubs', 'hearts', 'spades']
faces = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

class Deck:
    def __init__(self, num_decks=1):
        if num_decks > 8:
            num_decks = 8
        self.cards = [Card(s, f) for s in suits for f in faces]*num_decks
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw(self, num_cards=1):
        return [self.cards.pop(0) for c in range(num_cards)]



