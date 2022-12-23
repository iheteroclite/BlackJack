import inquirer

from src.deck import Deck
from src.hand import Hand

def play():
    # Setup number of players and ace value
    num_players = player_choice("players", 1, [n+1 for n in range(5)])
    print('number of players selected was:', num_players)
    player_ace = 'Player chooses'
    ace_qn = "Select the value of player's Aces"
    ace_value = player_choice(ace_qn, 3, [1, 11, player_ace])

    # Make a deck
    # min cards ensures there's at least 1 deck per 4 players
    min_decks = 2 if num_players > 4 else 1
    num_decks = player_choice("decks", 1, [n+min_decks for n in range(8)])
    print('number of decks selected was:', num_decks)
    deck = Deck(num_decks, ace_value)

    # Start game by making everyone's hand
    dealer_hand = Hand(deck, 'Dealer', 'dealer')
    player_hands = [Hand(deck, f'Player {x + 1}', 'player')
        for x in range(num_players)]
    player_hands.append(dealer_hand)

    # Players' turns
    for hand in player_hands:
        # alert which player's turn
        print (f"{hand.player.upper()}'S TURN!!")
        if hand.person == 'player':
            # take player input/consent before displaying cards
            player_choice('', 2, ['yes'], hand)

        # max cards a player/dealer can have is 11 (1*4 + 2*4 +3*4 = 7*3 = 21)
        for j in range(11):
            if hand.state == 'playing' or hand.state == 'draw':
                # display cards in your hand
                print ('Your hand contains:')
                print(hand)

                # check blackjack
                turn_res = check_twenty_one(hand, player_ace==ace_value)
                if turn_res:
                    # print blackjack, twenty-one or bust statement to user
                    print(f'{hand.player} you have {turn_res}')
                    # go to next player
                    continue

                # get user input for if they want to hit, stand, or surrender
                player_move = ''
                if hand.person == 'player':
                    player_move = player_choice(hand=hand)
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
        success = 'win' if hand.success == 1 else \
            'lose' if hand.success == -1 else '(push) tie'
        print(f"{hand.player} scored {hand.state}, {success.upper()}S")


    # TODO: make a player class, and have a player who can play again
    # player gets a new hand, but their wins/lossess are tallied

# TODO: 'Select value of ' or {} format strings
def player_choice(msg="", i=0, options = ['hit', 'stand', 'surrender'], hand=False,):
    parts = [", What do you do?", "Select number of ", " are you ready?", " "]
    questions = [
    inquirer.List('choice',
        message = f'{hand.player}{parts[i]}' if hand else f'{parts[i]}{msg}',
        choices = options,
        ),
    ]
    return inquirer.prompt(questions)['choice']

# TODO: remove num and state args if not used
def check_twenty_one(hand, ace_choice=False, num=False, state='playing'):
    total = hand.get_total()
    if total == 21:
        if hand.state == 'draw':
            hand.state = 'blackjack'
        else:
            hand.state = 21
        return hand.state
    elif total > 21:
        # for each ace, dealer takes its value as 1, and re-checks score
        for i, card in enumerate(hand.cards, 1):
            if card.face=='Ace' and card.value != 1:
                ordinal = 'st' if i==1 else 'nd' if i==2 else 'rd' if i==3 else 'th'
                val_qn = f"Your {i}{ordinal} card is an Ace. Select its value"

                if hand.person == 'dealer' or (ace_choice and \
                    player_choice(val_qn, 3, [1, 11])==1):
                    card.set_ace_value(1)
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
