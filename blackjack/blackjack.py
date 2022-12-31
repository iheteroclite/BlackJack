import inquirer

from src.deck import Deck
from src.hand import Hand
from src.people import Dealer, Player

def play():
    # Setup number of players and ace value
    num_players = player_choice("players", 1, [n+1 for n in range(5)])
    print('Number of players selected was:', num_players)
    player_ace = 'Player chooses'
    ace_qn = "Select the value of player's Aces"
    ace_value = player_choice(ace_qn, 3, [1, 11, player_ace])

    # Make a deck
    # min_decks ensures there's at least 1 deck per 4 players
    min_decks = 2 if num_players > 4 else 1
    num_decks = player_choice("decks", 1, [n+min_decks for n in range(8)])
    print('Number of decks selected was:', num_decks)
    deck = Deck(num_decks, ace=ace_value if ace_value==1 else 11)

    # Initialise Players and Dealer
    dealer = Dealer(deck)
    players = [Player(deck, f'Player {x + 1}') for x in range(num_players)]
    players.append(dealer)

    # Play as many rounds as the player wants
    while True: # Emulating a do-while loop
        round(dealer, players, deck, ace_value, player_ace)
        options = ['Play Another Round', 'Leave the Table']
        if player_choice(options=options) == options[0]:
            # TODO*: reset the deck, reset player hands, and player state
            continue
        else:
            # TODO*: Print user score tallies
            # Make a lambda function in class People, and pass the different
            # strings for Dealer and Player to the printout
            break


def round(dealer, players, deck, ace_value, player_ace):
        # Players' turns
    for player in players:
        # alert which player's turn
        print (f"{player.name.upper()}'S TURN!!")
        if isinstance(player, Player):
            # take player input/consent before displaying cards
            player_choice('', 2, ['yes'], player)

        # max cards a player/dealer can have is 11 (1*4 + 2*4 +3*4 = 7*3 = 21)
        for j in range(11):
            if player.hand.state == 'playing' or player.hand.state == 'draw':
                # display cards in your hand
                print ('Your hand contains:')
                print(player.hand)

                # check blackjack
                result = check_twenty_one(player.hand, player_ace==ace_value)
                if result:
                    print(f'{player.name} you have {result}')
                    # go to next player
                    continue

                # get user input for if they want to hit, stand, or surrender
                player_move = ''
                if isinstance(player, Player):
                    player_move = player_choice(player=player)
                #elif hand.person == 'AI':
                    # TODO: add an option to have AI make choices
                    # can modify dealer draw so they only draw to specific val
                #    player_move = 'temp value'
                else:
                    player_move = dealer_move(dealer.hand, 17)

                print(player_move)

                if player_move == 'hit':
                    player.hand.hit(deck)
                elif player_move == 'stand': #'stand'
                    player.hand.state = player.hand.get_total()
                    break
                elif player_move == 'surrender':
                    player.hand.state = player_move
                # TODO: could add 'split', I'll need a player class
            else:
                break

    # Final score
    print(f"The dealer's score is: {dealer.hand.state}")

    for player in players[:-1]:  #bust, a total, blackjack, or surrender
        success = score_hand(player.hand, dealer.hand)
        print(f"{player.name} scored {player.hand.state}, {success.upper()}S")
    # TODO*: player wins/lossess are tallied


def score_hand(hand, dealer_hand):
    # Player always loses if they bust or surrender
    if hand.state in ('bust', 'surrender'):
        hand.success = -1
    # If player is not bust, and dealer busts, player wins
    elif dealer_hand.state == 'bust':
        hand.success = 1
    # Push if there's a tie
    elif hand.state == dealer_hand.state:
        hand.success = 0
    # BlackJack trumps all other hands
    # Dealer blackjack wins (unless player has blackjack, push)
    elif dealer_hand.state == 'blackjack':
        hand.success = -1
    elif hand.state == 'blackjack':
        hand.success = 1
    # If there's no other condition, highest score wins
    elif hand.state > dealer_hand.state:
        hand.success = 1
    else:
        hand.success = -1
    return 'win' if hand.success == 1 else \
        'lose' if hand.success == -1 else '(push) tie'


# TODO: 'Select value of ' or {} format strings
def player_choice(msg="", i=0, options = ['hit', 'stand', 'surrender'], player=False,):
    parts = [", What do you do?", "Select number of ", " are you ready?", " "]
    questions = [
    inquirer.List('choice',
        message = f'{player.name}{parts[i]}' if player else f'{parts[i]}{msg}',
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
        # For each ace, dealer takes its value as 1, and re-checks score
        for i, card in enumerate(hand.cards, 1):
            if card.face=='Ace' and card.value != 1:
                ordinal = 'st' if i==1 else 'nd' if i==2 else 'rd' if i==3 else 'th'
                val_qn = f"Your {i}{ordinal} card is an Ace. Select its value"

                if hand.dealer or (ace_choice and \
                    player_choice(val_qn, 3, [1, 11])==1):
                    card.set_ace_value(1)
                    if hand.get_total() <= 21: # re-check after changing ace
                        return check_twenty_one(hand)
        hand.state = 'bust'
        return 'bust'
    return False


def dealer_move(hand, num):
    if hand.get_total() >= num:
        return 'stand'
    return 'hit'

def welcome():
    print('Welcome to BlackJack (with a twist)! \n' \
    'In this game you will have the option to play with friends using \n' \
    'multiple decks, and if you want to, you can try to cheat. ' \
    'But watch out: you can get caught if the dealer sees you, or even in ' \
    'a random pat-down, or if the card you cheat with has already been ' \
    'played. \n' \
    'You can select your difficulty level by choosing different ' \
    'dealers, but the chance of being caught will always increase as the ' \
    'statistical liklihood of your success rate decreases - so try not to ' \
    'win every game. \n' \
    'Have fun, rascals!')

if __name__ == '__main__':
    welcome()
    play()
