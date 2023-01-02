from src.hand import Hand
class People:
	"""SuperClass the Player and Dealer SubClasses."""

	def __init__(self, deck, name):
		self.name = name
		self.hands = [Hand(deck)]	# List of player hands
		self.hand = self.hands[0]	# Current hand in play
		# In the case of the dealer, these count all player's wins
		self.blackjack_wins = 0
		self.even_wins = 0
		self.losses = 0 			# Includes bust, surrender, and loss
		self.pushes = 0
		self.games = 0 				# Number of rounds played

	def reset(self, deck):
		self.hands = [Hand(deck)]
		self.hand = self.hands[0]

	def print_str(self, name_str, person, multiple):
		wins = self.blackjack_wins + self.even_wins
		return '_'*52 +f'\n{name_str}, over {self.games} rounds {person}:\n' \
		f'Wins: {wins} ({round(100*wins/(self.games*multiple), 1)}%) with ' \
		f'{self.blackjack_wins} blackjack and ' \
		f'{self.even_wins} even payouts \n' \
		f'Losses: {self.losses}		Pushes: {self.pushes}'


class Player(People):
	"""Players are users.

	Player extends the People superclass.
	"""

	def __init__(self, deck, name):
		super().__init__(deck, name)

	def __str__(self):
		return self.print_str(self.name, 'you have scored', 1)


class Dealer(People):
	r"""Dealer is an automated Dealer

	Dealer extends the People superclass.
	An instance of Dealer counts all even or blackjack wins, \
	pushes and losses of every player at the table as a tally.
	"""

	def __init__(self, num_players, deck, name="Dealer"):
		super().__init__(deck, name)
		self.hand.dealer = True
		self.num_players = num_players

	def __str__(self):
		return self.print_str('All players','scored a total of', self.num_players)
