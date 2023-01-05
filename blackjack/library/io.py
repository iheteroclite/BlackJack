"""This library provides various input and output functions for blackjack."""

import inquirer
from os import get_terminal_size

top = ' ____________ '
pads_top = '/' + ' ' * 12 + '\\'
pads = '|' + ' ' * 12 + '|'
bottom = '\\____________/'

def card_string(cards):
    tot = len(cards)
    faces_str = ''
    suits_str = ''
    suits_two = ''
    for card in cards:
        faces_str += '|' + card.face.center(12) + '|'
        suits_two += f'|  {card.suit}     {card.suit}   |'
        suits_str += f'|     {card.suit}      |'
    return '\n'.join([top * tot, pads_top * tot, faces_str, pads * tot,
                      suits_two, pads * tot, suits_str, bottom * tot])


def player_choice(
        msg="", i=0, options=['hit', 'stand', 'surrender'], player=False,):
    # TODO: tidy this
    bits = [', What do you do?', 'Select number of ', ' are you ready?', ' ']
    questions = [inquirer.List('choice',
                 message=f'{player.name}{bits[i]}{msg}' if player
                               else f'{bits[i]}{msg}',
                 choices=options)]
    return inquirer.prompt(questions)['choice']

def get_screen_height():
    size = get_terminal_size()
    return size.columns - 15


def welcome():
    print('Welcome to BlackJack (with a twist)! \n'
          + 'In this game you will have the option to play with friends '
          + 'using multiple decks, and if you want to, you can try to cheat. '
          + 'But watch out: you can get caught if the dealer sees you, or '
          + 'even in a random pat-down, or if the card you cheat with has '
          + 'already been played. \n'
          + 'You can select your difficulty level by choosing different '
          + 'dealers, but the chance of being caught will always increase '
          + 'as the statistical liklihood of your success rate decreases - '
          + 'so try not to win every game. \n'
          + 'Have fun, rascals!')


def print_cheat_info():
    print('Choose up to 4 cards to hide on your person. '
        + 'Also select a dealer, with varying difficulty levels (chance of '
        + 'being caught cheating). The chance of being caught varies'
        + 'with the liklihood of winning at the rate you are winning. This '
        + 'is especially true if you win many blackjacks!'
        + 'Even if you do not cheat, there is a small possibility of being '
        + 'suspected of cheating if you do very well, or if another player '
        + 'cheats with a card you have been dealt.'
        + 'If you\'re holding cards during a random '
        + 'patdown (more likely with good dealers), chances of being caught '
        + 'are very high!')

def print_chance_info():
    print('The probability of your hand and of you gettting the '
        + 'wins you have without cheating is shown after every round.\n'
        + '% chance on a hand is the percentage chance you had of getting '
        + 'that hand this round.\n'
        + '% chance on a win is the percentage chance that a player would '
        + 'get at least as many wins as you have over that many games.\n'
        + '\u03C3 means Standard Deviation, a measure of how far away from '
        + 'the mean your results are. Within 1\u03C3 is completely normal, '
        + "and won't arouse suspicion, whereas 3\u03C3 from the mean is "
        + 'very abnormal.' )