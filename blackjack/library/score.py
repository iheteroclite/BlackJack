"""Library of functions for scoring a hand in the game of Blackjack.


See the README.md file for the rules and scoring assumptions."""

__version__ = 0.40
__author__ = 'iheteroclite'
__all__ = ['Dealer', 'Deck', 'Player', 'cheat_choice', 'cheat_setup',
           'check_twenty_one', 'dealer_move', 'get_screen_height',
           'play', 'player_choice', 'round', 'score_hand', 'welcome']

# Prevent circular import by importing the module here
import src.people as people
from library.io import player_choice

def score_hand(player, dealer):
    """Compares the dealer and player scores to see the success state"""
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
            # If there's no other condition, highest score wins
            elif score > dealer_score:
                word = 'even_wins'

    # Update player & dealer wins, losses and games counters
    setattr(player, word, getattr(player, word) + 1)
    setattr(dealer, word, getattr(dealer, word) + 1)
    player.games += 1

    return 'loses' if word == 'losses' else ' '.join(word.split('_')[::-1])


def check_twenty_one(player, ace_choice=False):
    """Checks whethr the player/dealer has 21, blackjack, or is bust"""
    hand = player.hand
    total = hand.get_total()
    if total == 21:
        if hand.state == 'draw':
            hand.state = 'blackjack'
            # Update blackjack tally for probability calculations
            if isinstance(player, people.Player):
                player.probabilities[-1]['blackjack'] = True
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

                if isinstance(player, people.Player) and ace_choice:
                    ace_to_1 = player_choice(val_qn, 3, [1, 11]) == 1
                    if ace_to_1:
                        card.set_ace_value(1)
                        if hand.get_total() <= 21:
                            # re-check after changing ace
                            return check_twenty_one(player)
        hand.state = 'bust'
        return 'bust'
    return False

