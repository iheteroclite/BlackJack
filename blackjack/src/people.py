from src.hand import Hand
class People:
	def __init__(self, deck, name):
		self.name = name
		self.hands = [Hand(deck)]
		self.hand = self.hands[0]
		# In the case of the dealer, these counts all player's wins
		self.blackjack_wins = 0
		self.even_wins = 0
		self.losses = 0
		self.pushes = 0

class Player(People):
	def __init__(self, deck, name):
		super().__init__(deck, name)

class Dealer(People):
	def __init__(self, deck, name="Dealer"):
		super().__init__(deck, name)
		self.hand.dealer = True
		self.games = 0