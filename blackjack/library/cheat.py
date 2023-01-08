from library.io import print_cheat_info, print_chance_info, player_choice
from library.io import get_screen_height


def cheat_setup(players, dealer):
    players_are_cheating = False

    for player in players:
        query = f'{player.name}, Would you like to cheat?'
        options = ['Yes, sneak cards up my sleeve!',
                   'Heavens no!',
                   'Help me with Cheating',
                   'Help me with Probability']
        while True:
            choice = player_choice(query, 3, options)
            if choice == options[0]:
                player.cheater = True
                players_are_cheating = True
                player.hide_cards()
                break
            elif choice == options[2]:
                print_cheat_info()
                continue
            elif choice == options[3]:
                print_chance_info()
                continue
            else:
                break

        # TODO: Pass to next player
        player_choice('Pass to next player?', 3, ['OK'])
        print('\n' * get_screen_height())

    if players_are_cheating:
        select_dealer(dealer)


def select_dealer(dealer):
    query = 'Players, Select a Dealer (hardest first)'
    options = ['Big Brother',
               'Casino Cat',
               'Sharp-Eyed Stacy',
               'Happy Harry',
               'Grandma Gertrude',
               'Blind Bob']
    choice = player_choice(query, 3, options)

    dealer.name = choice
    dealer.set_coeff()


def cheat_choice(player, now='now'):
    # Check player wants to cheat
    cheat = player_choice(f'Do you want to cheat {now}?', 3,
                          ['Yes', 'No'],
                          player)
    if cheat == 'Yes':
        print(player.sleeve)

        # Ask player which card in their hand to swap
        hand_choices = [card.__str__() for card in player.hand.cards]
        hand_card = player_choice('Which hand card do you swap?', 3,
                                  hand_choices,
                                  player)
        hand_index = hand_choices.index(hand_card)

        # Ask player which card in their sleeve to swap
        sleeve_choices = [card.__str__() for card in player.sleeve.cards]
        sleeve_card = player_choice('Which sleeved card do you swap?', 3,
                                    sleeve_choices, player)
        sleeve_index = sleeve_choices.index(sleeve_card)

        player.hand.cards[hand_index], player.sleeve.cards[sleeve_index] = (
            player.sleeve.cards[sleeve_index], player.hand.cards[hand_index])
        # TODO: test card marking
        player.sleeve.mark_cheat_cards()
        print(player.hand)

        if now == 'now':
            cheat_choice(player, now='again')


def card_in_deck(search_card, deck):
    copies_in_deck = 0
    for card in deck.cards:
        if card.face == search_card.face and card.suit == search_card.suit:
            copies_in_deck += 1
    return copies_in_deck
