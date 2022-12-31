top = ' ____________ '
pads_top = '/' + ' '*12 + '\\'
pads = '|' + ' '*12 + '|'
bottom = '\\____________/'

class Hand:
	def __init__(self, deck, dealer=False):
		self.cards = deck.draw(2)
		# TODO take user input for value of 'player'
		self.dealer = dealer
		self.state = 'draw' #records blackjack, twenty-one, bust
		self.success = 'tbd'

	def __str__(self):
		tot = self.get_card_count()
		faces_str = ''
		suits_str = ''
		suits_two = ''
		for card in self.cards:
			faces_str += '|' + card.face.center(12) + '|'
			suits_two += f'|  {card.suit}     {card.suit}   |'
			suits_str += f'|     {card.suit}      |'
		return '\n'.join([top*tot, pads_top * tot, faces_str, pads * tot, \
			suits_two, pads * tot, suits_str, bottom * tot])


	def get_total(self):
#		print([card.value for card in self.cards])
		return sum([card.value for card in self.cards])

	def get_card_count(self):
		return len(self.cards)

	# Keeping hit as a hand method, so game can be extended for multiple hands
	def hit(self, deck):
		self.state = 'playing'
		self.cards += deck.draw()

	def stand(self, condition='stand'):
		self.state = condition


