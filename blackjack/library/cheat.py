from library.io import print_cheat_info, print_chance_info, player_choice

def caught(player):
    """Check if the player has been caught (or assumed) cheating.

    """
    # TODO
    # If card has already been played
    # elif caught due to unlikely/impossible win rate
    # elif caught by random patdown
    # elif incorrectly assumed culpable for other player's cheat
    return False


def punishment(player):
    pass


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

	if players_are_cheating:
		select_dealer(dealer)


def select_dealer(dealer):
	query = f'Players, Select a Dealer (hardest first)'
	options = ['Big Brother',
			   'Casino Cat',
			   'Sharp-Eyed Stacy',
			   'Happy Harry',
			   'Grandma Gertrude',
			   'Blind Bob']
	choice = player_choice(query, 3, options)

	dealer.name = choice
	dealer.set_coeff()



