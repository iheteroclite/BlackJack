class Hand:
	def __init__(self, deck, player, person_type='player'):
		self.cards = deck.draw(2)
		self.player = player  #this will be player name like 'dealer', 'player1'
		# TODO take user input for value of 'player'
		self.person = person_type
		self.card_count = len(self.cards)
		self.total = 0; # function here


