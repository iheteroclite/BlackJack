import random

suits = ['\033[91m♦\033[00m', '♣', '\033[91m♥\033[00m', '♠']
faces = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face
        self.value = 0
        self.lines = []
        try:
            self.value = int(self.face)
        except:
            if self.face == faces[0]:
                # for a player, value is always 11
                self.value = 11
                # TODO: (most variants) for a dealer, value changes to 1 if dealer total > 21
                # ^ put this as a function of hand?
            elif self.face in faces[10:]:
                self.value = 10

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



