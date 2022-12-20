import inquirer

from src.deck import Deck
from src.hand import Hand


def play():
    # Setup number of players and decks
    chose = player_choice(False, "players", [n+1 for n in range(5)])
    num_players = chose['choice']
    print('number of players selected was:', num_players)

    # Make a deck
    # min cards ensures there's at least 1 deck per 4 players
    min_decks = 2 if num_players > 4 else 1
    chose = player_choice(False, "decks", [n+min_decks for n in range(8)])
    num_decks = chose['choice']
    print('number of decks selected was:', num_decks)
    deck = Deck(num_decks)

    # Start game by making everyone's hand
    dealer_hand = Hand(deck, 'Dealer', 'dealer')
    player_hands = [Hand(deck, f'Player {x + 1}', 'player')
        for x in range(num_players)]
    player_hands.append(dealer_hand)

    # Players' turns
    for hand in player_hands:
        # alert which player's turn
        # TODO: take player input/consent before displaying cards
        print (f"{hand.player.upper()}'S TURN!!")

        # max cards a player/dealer can have is 11 (1*4 + 2*4 +3*4 = 7*3 = 21)
        for j in range(11):
            if hand.state == 'playing' or hand.state == 'draw':
                # display cards in your hand
                print ('Your hand contains:')
                print(hand)

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
                # TODO: could add 'split', I'll need a player class
            else:
                break

    dealers_score = dealer_hand.state
    print(f"The dealer's score is: {dealers_score}")

    # Final score
    for hand in player_hands[:-1]:  #bust, a total, blackjack, surrender
        # hand_val = 0
        # if hand.state in ('bust', 'surrender', 'blackjack'):
        #     hand_val = 23 if hand.state == 'blackjack' else 0

        if hand.state in ('bust', 'surrender'):
            hand.success = -1
        elif dealer_hand.state == 'bust':
            hand.success = 1
        elif hand.state == dealer_hand.state:
            hand.success = 0
        elif dealer_hand.state == 'blackjack':
            hand.success = -1
        elif hand.state == 'blackjack':
            hand.success = 1
        elif hand.state > dealer_hand.state:
            hand.success = 1
        elif dealer_hand.state > hand.state:
            hand.success = -1
        success = 'win' if hand.success == 1 else 'lose' if hand.success == -1 else '(push) tie'
        print(f"{hand.player} scored {hand.state}, {success.upper()}S")


    # TODO: make a player class, and have a player who can play again
    # player gets a new hand, but their wins/lossess are tallied


def player_choice(hand, msg_str="", options = ['hit', 'stand', 'surrender']):
    parts = [", What do you do?", "Select number of "]
    questions = [
    inquirer.List('choice',
        message = f'{hand.player}{parts[0]}' if hand else f'{parts[1]}{msg_str}:',
        choices = options,
        ),
    ]
    return inquirer.prompt(questions)

def check_twenty_one(hand, num = False, state='playing'):
    total = hand.get_total()
    if total == 21:
        if hand.state == 'draw':
            hand.state = 'blackjack'
        else:
            hand.state = 21
        return hand.state
    elif total > 21:
        if hand.person == 'dealer':
            # for each ace, dealer takes its value as 1, and re-checks score
            for card in hand.cards:
                if card.face=='Ace':
                    card.value = 1
                    if hand.get_total() <= 21: # re-check after changing ace
                        return check_twenty_one(hand)
        hand.state = 'bust'
        hand.success = -1
        return 'bust'
    return False

def dealer_move(hand, num):
    if hand.get_total() >= num:
        return 'stand'
    return 'hit'

if __name__ == '__main__':
    play()
