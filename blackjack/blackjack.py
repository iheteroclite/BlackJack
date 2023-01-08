"""The American Casino game blackjack / 21
In this game you will have the option to play with friends using
multiple decks, and if you want to, you can try to cheat. But watch
out: you can get caught if the dealer sees you, or even in a random
pat-down, or if the card you cheat with has already been played.
You can select your difficulty level by choosing different dealers,
but the chance of being caught will always increase as the statistical
liklihood of your success rate decreases - so try not to win every game.
"""

__version__ = 0.40
__author__ = 'iheteroclite'
__all__ = ['Dealer', 'Deck', 'Player', 'cheat_choice', 'cheat_setup',
           'check_twenty_one', 'dealer_move', 'get_screen_height',
           'play', 'player_choice', 'round', 'score_hand', 'welcome']


from src.deck import Deck
from src.people import Dealer, Player
from library.cheat import cheat_setup, cheat_choice
from library.io import welcome, player_choice
from library.io import get_screen_height, goodbye
from library.score import score_hand, check_twenty_one


def play():

    # Setup the basic game
    # Initialise: list of players, the dealer, the deck, the number of decks,
    # the ace (1 or 11), and ace_choice a bool for players choosing ace value.
    players, dealer, deck, num_decks, min_decks, ace, ace_choice = game_setup()

    # Check if player wants to cheat
    banned_players = []
    cheat_setup(players, dealer)

    # Play as many rounds as the player wants (emulating a do-while loop)
    while players:
        round(dealer, players, deck, ace_choice)

        for player in players:
            print(player)
            # Check if player has been caught cheating
            if player.cheater:
                dealer.try_catch(player, players, banned_players, deck)
        print(dealer)
        options = ['Play Another Round', 'Leave the Table']
        if player_choice(options=options) == options[0]:
            if players:
                # If deck has less than minimum cards, reshuffle
                if len(deck.cards) < (min_decks * 52):
                    deck = Deck(num_decks, ace=ace)
                for player in players + [dealer]:
                    player.reset(deck)
                    player.hand.state = 'draw'
            else:
                print('The dealer has kicked you out of the casino!')
        else:
            # Leave the table (exit game)
            break


def round(dealer, players, deck, players_choose_ace):
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
                result = check_twenty_one(player, ace_choice=players_choose_ace)

                if result:
                    print(f'{player.name} you have {result}')
                    # Go to next player if player's turn is over
                    continue

                # Get user input: hit, stand, surrender [or cheat]
                player_move = ''
                if isinstance(player, Player):
                    result = check_twenty_one(player,
                                              players_choose_ace)
                    if result:
                        print(f'{player.name} you have {result}')
                        # Go to next player if player's turn is over
                        continue
                    if player.cheater:
                        # Let player cheat multiple times, and catch finish
                        if cheat_choice(player, players_choose_ace):
                            # Go to next player if player's turn is over
                            continue
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


def game_setup():
    """Get play input and setup the game

    Returns:
    players -- a list of players of the Player class
    dealer -- a dealer of the Dealer class
    deck -- the deck to start play with
    num_decks -- the number of 52 card decks which make up the deck
    min_decks -- the minimum number of decks so that the deck will never be
                 completely depleted during a game. When the number of cards
                 is less than min_decks * 52, the deck should reset
    ace -- the initial ace vale (either 1 or 11)
    ace_choice -- a bool denoting whether players have the choice of
                  the value of the aces in their hand
    """
    # Setup number of players and ace value
    num_players = player_choice("players", 1, [n + 1 for n in range(5)])
    print('Number of players selected was:', num_players)
    player_ace = 'Player chooses'
    ace_qn = "Select the value of player's Aces"
    ace_value = player_choice(ace_qn, 3, [1, 11, player_ace])
    ace = ace_value if ace_value == 1 else 11
    ace_choice = ace_value == player_ace

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

    return players, dealer, deck, num_decks, min_decks, ace, ace_choice


def dealer_move(hand, num):
    if hand.get_total() >= num:
        return 'stand'
    return 'hit'


if __name__ == '__main__':
    welcome()
    play()
    goodbye()
