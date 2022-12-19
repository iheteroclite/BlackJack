import inquirer

from src.deck import Deck
from src.hand import Hand


def play():
    # setup number of players and decks
    chose = player_choice(False, "players", [n+1 for n in range(5)])
    num_players = chose['choice']
    print('number of players selected was:', num_players)

    # make a deck
    min_decks = 2 if num_players > 4 else 1
    chose = player_choice(False, "decks", [n+min_decks for n in range(8)])
    num_decks = chose['choice']
    print('number of decks selected was:', num_decks)
    deck = Deck(num_decks)

    # start game by making everyone's hand
    dealer_hand = Hand(deck, 'Dealer', 'dealer')
    player_hands = [Hand(deck, f'Player {x + 1}', 'player')
        for x in range(num_players)]

    # players' turns
    for hand in player_hands:
        # alert which player's turn
        # TODO: take player input/consent before displaying cards
        print (f"{hand.player.upper()}'S TURN!!")

        # max cards a player/dealer can have is 11 (1*4 + 2*4 +3*4 = 7*3 = 21)
        for j in range(11):
            if hand.state == 'playing' or hand.state == 'draw':
                # display cards in your hand
                print ('Your hand contains:')
                print([[card.suit, card.face] for card in hand.cards])
                # check blackjack
                turn_res = check_twenty_one(hand)
                if turn_res:
                    # print blackjack, twenty-one or bust statement to user
                    print(f'{hand.player} you have {turn_res}')
                    # go to next player
                    continue

                # get user input for if they want to hit, stand, or surrender
                player_move = player_choice(hand)['choice']

                print(player_move)

                if player_move == 'hit':
                    hand.hit(deck)
                elif player_move == 'stand': #'stand'
                    hand.state = hand.get_total() #total of player's cards
                    break
                elif player_move == 'surrender':
                    hand.state = player_move
            else:
                break

        # TODO: check deck doesn't get down to 0 cards
        # OR make sure there are enough decks for the players

        # Dealer's turn

def hit(hand, deck):
    # not yet used
    print('hit me with your rhythm stick')
    hand.hit(deck)

def player_choice(hand, msg_str="", options = ['hit', 'stand', 'surrender']):
    question = f"{hand.player}, What do you do?"
    questions = [
    inquirer.List('choice',
        message = question if hand else f'Select number of {msg_str}:',
        choices = options,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers

def check_twenty_one(hand, state='playing'):
    if hand.get_total() == 21:
        if hand.person == 'dealer':
            #TODO: change all dealer aces into 1's are return false
            # if hand.cards contains card with card.face =='ace'
            #    return False
            print('Dealer aces always remain 11 in this game variant')
        if hand.state == 'draw':
            hand.state = 'blackjack'
        else:
            hand.state = 'twenty-one'
        return hand.state
    elif hand.get_total() > 21:
        hand.state = 'bust'
        return 'bust'
    return False


if __name__ == '__main__':
    play()
