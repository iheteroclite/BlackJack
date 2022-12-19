import inquirer

from src.deck import Deck
from src.hand import Hand


def play():
    # setup number of players and decks
    chose = player_choice(False, "players", [n+1 for n in range(5)])
    num_players = chose['choice']
    print('number of players selected was:', num_players)

    # make a deck
    # min cards ensures there's at least 1 deck per 4 players
    min_decks = 2 if num_players > 4 else 1
    chose = player_choice(False, "decks", [n+min_decks for n in range(8)])
    num_decks = chose['choice']
    print('number of decks selected was:', num_decks)
    deck = Deck(num_decks)

    # start game by making everyone's hand
    dealer_hand = Hand(deck, 'Dealer', 'dealer')
    player_hands = [Hand(deck, f'Player {x + 1}', 'player')
        for x in range(num_players)]
    player_hands.append(dealer_hand)


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
                player_move = ''
                if hand.person == 'player':
                    player_move = player_choice(hand)['choice']
                elif hand.person == 'AI':
                    # TODO: add an option to have AI make choices
                    # can modify dealer draw so they only draw to specific val
                    player_move = 'temp value'
                elif hand.person == 'dealer':
                    player_move = dealer_move(hand, 17)

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

        # OR make sure there are enough decks for the players

def player_choice(hand, msg_str="", options = ['hit', 'stand', 'surrender']):
    questions = [
    inquirer.List('choice',
        message = f"{hand.player}, What do you do?" if hand else f'Select number of {msg_str}:',
        choices = options,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers

def check_twenty_one(hand, num = False, state='playing'):
    total = hand.get_total()
    if total == 21:
        if hand.state == 'draw':
            hand.state = 'blackjack'
        else:
            hand.state = 'twenty-one'
        return hand.state
    elif total > 21:
        if hand.person == 'dealer':
            # for each ace, dealer takes its value as 1, and re-checks score
            for card in hand.cards:
                if card.face=='ace':
                    card.value = 1
                    if hand.get_total() <= 21: # re-check after changing ace
                        return check_twenty_one(hand)
        hand.state = 'bust'
        return 'bust'
    return False

def dealer_move(hand, num):
    if hand.get_total() >= num:
        return 'stand'
    return 'hit'

if __name__ == '__main__':
    play()
