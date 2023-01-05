__version__ = 0.36
__author__ = 'iheteroclite'

from src.deck import Deck
from src.hand import Hand
from src.people import Dealer, Player
from library.cheat import caught, cheat_setup, cheat_choice
from library.io import welcome, player_choice, print_chance_info
from library.io import get_screen_height


def play():
    # Setup number of players and ace value
    num_players = player_choice("players", 1, [n + 1 for n in range(5)])
    print('Number of players selected was:', num_players)
    player_ace = 'Player chooses'
    ace_qn = "Select the value of player's Aces"
    ace_value = player_choice(ace_qn, 3, [1, 11, player_ace])
    ace = ace_value if ace_value == 1 else 11

    # Make a deck
    # min_decks ensures there's at least 1 deck per 4 players
    min_decks = 2 if num_players > 4 else 1
    num_decks = player_choice("decks", 1, [n + min_decks for n in range(8)])
    print('Number of decks selected was:', num_decks)
    deck = Deck(num_decks, ace=ace)

    # Initialise Players and Dealer
    # TODO: could add an option to load player save from file?
    dealer = Dealer(num_players, deck)
    players = [Player(deck, f'Player {x + 1}') for x in range(num_players)]

    # Check if player wants to cheat
    cheat_setup(players, dealer)

    # Play as many rounds as the player wants (emulating a do-while loop)
    while True:
        round(dealer, players, deck, ace_value, player_ace)

        for player in players:
            player.calculate_probability()
            print(player)
            # Check if player has been caught cheating
            if player.cheater:
                caught(player)
        print(dealer)
        options = ['Play Another Round', 'Leave the Table']
        if player_choice(options=options) == options[0]:
            # If deck has less than minimum cards, reshuffle
            if len(deck.cards) < (min_decks * 52):
                deck = Deck(num_decks, ace=ace)
            for player in players + [dealer]:
                player.reset(deck)
                player.hand.state = 'draw'
        else:
            # Leave the table (exit game)
            break


def round(dealer, players, deck, ace_value, player_ace):
    # Players' turns
    # TODO*: turn player into person here, for clarity
    for i, player in enumerate(players + [dealer]):
        # Clear screen of previous player
        if len(players) > 1:
            subsequent = 'first' if i == 0 else 'next'
            player_choice(f'Pass to {subsequent} player?', 3, ['OK'])
            print('\n' * get_screen_height())
        # Alert which player's turn
        print(f"{player.name.upper()}'S TURN!!")
        if isinstance(player, Player):
            # Take player input/consent before displaying cards
            player_choice('', 2, ['yes'], player)

        # Max cards a player can have is 11 (4*1 + 4*2 + 3*3 = 21)
        for j in range(11):
            if player.hand.state == 'playing' or player.hand.state == 'draw':
                # Display cards in player's hand
                print(player.hand)

                # Check blackjack, 21, or bust
                result = check_twenty_one(player.hand, player_ace == ace_value)

                if result:
                    print(f'{player.name} you have {result}')
                    # Go to next player if player's turn is over
                    continue

                # Get user input: hit, stand, surrender [or cheat]
                player_move = ''
                if isinstance(player, Player):
                    if player.cheater:
                        cheat_choice(player)
                    player_move = player_choice(player=player)
                else:
                    player_move = dealer_move(dealer.hand, 17)

                print(player_move)

                if player_move == 'hit':
                    player.hand.hit(deck)
                elif player_move == 'stand':
                    player.hand.state = player.hand.get_total()
                    break
                elif player_move == 'surrender':
                    player.hand.state = player_move
                # TODO: could add 'split'
            else:
                break

    # Final score
    print(f"The dealer's score is: {dealer.hand.state}")

    for player in players:
        # success is the win type (blackjack, even), loss, or push
        success = score_hand(player, dealer)
        print(f"{player.name} scored {player.hand.state}, {success.upper()}")
    dealer.games += 1


def score_hand(player, dealer):
    score = player.hand.state
    dealer_score = dealer.hand.state
    word = 'losses'

    if score not in ('bust', 'surrender'):
        # If player is not bust, and dealer busts, player wins
        if dealer_score == 'bust':
            word = 'blackjack_wins' if score == 'blackjack' else 'even_wins'
        # Push if there's a tie
        elif score == dealer_score:
            word = 'pushes'
        # BlackJack trumps all other hands
        # Dealer blackjack wins (unless player has blackjack)
        elif dealer_score != 'blackjack':
            if score == 'blackjack':
                word = 'blackjack_wins'
                # Update blackjack tally for probability calculations
                player.probabilities[-1]['blackjack'] = True
            # If there's no other condition, highest score wins
            elif score > dealer_score:
                word = 'even_wins'

    # Update player & dealer wins, losses and games counters
    setattr(player, word, getattr(player, word) + 1)
    setattr(dealer, word, getattr(dealer, word) + 1)
    player.games += 1

    return 'loses' if word == 'losses' else ' '.join(word.split('_')[::-1])


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
            if card.face == 'Ace' and card.value != 1:
                ordinal = ('st' if i == 1 else 'nd' if i == 2
                           else 'rd' if i == 3 else 'th')
                val_qn = f"Your {i}{ordinal} card is an Ace. Select its value"
                ace_is_1 = player_choice(val_qn, 3, [1, 11]) == 1
                if hand.dealer or (ace_choice and ace_is_1):
                    card.set_ace_value(1)
                    if hand.get_total() <= 21:   # re-check after changing ace
                        return check_twenty_one(hand)
        hand.state = 'bust'
        return 'bust'
    return False


def dealer_move(hand, num):
    if hand.get_total() >= num:
        return 'stand'
    return 'hit'


if __name__ == '__main__':
    welcome()
    play()
