from src.deck import Deck


def play():
    print('Hello, potential future BBC developer!')  # execution starts here! delete this line and add your game code.
    # setup number of players and decks
    # TODO: take from an input
    num_players = 1
    num_decks = 1
    # make a deck
    deck = Deck(num_decks)
    print([[card.suit, card.face] for card in deck.cards])

    #start game by making everyone's hand

    drawn = deck.draw(2)
    print([[card.suit, card.face] for card in drawn])
    # put those in cards in players hand




if __name__ == '__main__':
    play()
