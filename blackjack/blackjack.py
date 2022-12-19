import inquirer

from src.deck import Deck
from src.hand import Hand


def play():
    # setup number of players and decks
    num_players = player_choice(False, "number of players", [num+1 for num in range(5)])['choice']
    print('number of players selected was:', num_players)
    # TODO: take from an input
    #num_players = 2
    num_decks = player_choice(False, "number of decks", [num+1 for num in range(8)])['choice']
    print('number of decks selected was:', num_decks)
    # make a deck
    deck = Deck(num_decks)
    #print([[card.suit, card.face] for card in deck.cards])

    #start game by making everyone's hand
    dealer_hand = Hand(deck, 'Dealer', 'dealer')
    player_hands = [Hand(deck, f'Player {x + 1}', 'player') for x in range(num_players) ]
    #print('dealer hand',[[card.suit, card.face, card.value] for card in dealer_hand.cards])
    #print('dealer_val', dealer_hand.total)
    #print('player hand',[[[card.suit, card.face, card.value] for card in hand.cards] for hand in player_hands])

    # do first player's round
    for hand in player_hands:
        # display options for player
        print (f"{hand.player.upper()}'S TURN!!")
        # display cards in your hand
        print ('Your hand contains:')
        print([[card.suit, card.face] for card in hand.cards])
        # check blackjack
        turn_res = check_twenty_one(hand)
        if turn_res:
            # print blackjack win statement to user
            print(f'{hand.player} you have {turn_res}')
            # go to next player
            continue
        # get user input for if they want to hit, stand, or surrender
        # max cards a player can have is 11

        player_move = player_choice(hand)

        print(player_move)
        print(player_move['choice'])

def player_choice(hand, msg_str="", options = ['hit', 'stand', 'surrender']):
    questions = [
    inquirer.List('choice',
                  message=f"{hand.player}, What do you do?" if hand else f'Select {msg_str}:',
                  choices=options,
                  ),
    ]
    answers = inquirer.prompt(questions)
    return answers

def check_twenty_one(hand, stage='draw'):
    if hand.get_total() == 21:
        if hand.person == 'dealer':
            #TODO: change all dealer aces into 1's are return false
            # if hand.cards contains card with card.face =='ace'
            #    return False
            print('Dealer aces always remain 11 in this game variant')
        if hand.stage == 'draw':
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
