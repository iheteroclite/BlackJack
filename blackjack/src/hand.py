class Hand:
	def __init__(self, deck, player, person_type='player'):
		self.cards = deck.draw(2)
		self.player = player  #this will be player name like 'dealer', 'player1'
		# TODO take user input for value of 'player'
		self.person = person_type
		self.state = 'playing' #records blackjack, twenty-one, bust
		self.stage = 'draw'
		self.success = 'tbd'

	def get_total(self):
		return sum([card.value for card in self.cards])

	def get_card_count(self):
		return len(self.cards)

