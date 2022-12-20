top = ' ____________ '
pads = '|' + ' '*12 + '|'
bottom = '|____________|'

class Hand:
	def __init__(self, deck, player, person_type='player'):
		self.cards = deck.draw(2)
		self.player = player  #this will be player name like 'dealer', 'player1'
		# TODO take user input for value of 'player'
		self.person = person_type
		self.state = 'draw' #records blackjack, twenty-one, bust
		self.success = 'tbd'

	def __str__(self):
		tot = self.get_card_count()
		faces_str = ''
		suits_str = ''
		for card in self.cards:
			faces_str += '|' + card.face.center(12) + '|'
			suits_str += '|' + card.suit.center(12) + '|'
		return '\n'.join([top*tot, pads * tot, faces_str, pads * tot,pads * tot, suits_str, bottom * tot])


	def get_total(self):
		return sum([card.value for card in self.cards])

	def get_card_count(self):
		return len(self.cards)

	def hit(self, deck):
		self.state = 'playing'
		self.cards += deck.draw()

	def stand(self, condition='stand'):
		self.state = condition


