def cheat_setup(players):
	for player in players:
		query = f'{player.name}, Would you like to cheat?'
		options = ['Yes, sneak cards up my sleeve!',
				   'Heavens no!',
				   'Help info']
		while True:
			choice = player_choice(query, 3, options)
			if choice == options[0]:
				player.hide_cards()
				break
			elif choice == options[2]:
				print_cheat_info()
				continue
			else:
				break

def print_cheat_info():
	print('Choose up to 4 cards to hide on your person. '
		+ 'Also select a dealer, with varying difficulty levels (chance of '
		+ 'being caught cheating). The chance of being caught varies'
		+ 'with the liklihood of winning at the rate you are winning. This '
		+ 'is especially true if you win many blackjacks!'
		+ 'Even if you do not cheat, there is a small possibility of being '
		+ 'suspected of cheating if you do very well, or if another player '
		+ 'cheats with a card you have been dealt.'
		+ 'The probability of your hand and of you gettting the running '
		+ 'of wins you have without cheating is shown after every round.'
		+ 'If you\'re holding cards during a random '
		+ 'patdown (more likely with good dealers), chances of being caught '
		+ 'are very high!')
