top = ' ____________ '
pads_top = '/' + ' '*12 + '\\'
pads = '|' + ' '*12 + '|'
bottom = '\\____________/'

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
		suits_two = ''
		for card in self.cards:
			faces_str += '|' + card.face.center(12) + '|'
			suits_two += f'|  {card.suit}     {card.suit}   |'
			suits_str += f'|     {card.suit}      |'
		return '\n'.join([top*tot, pads_top * tot, faces_str, pads * tot, \
			suits_two, pads * tot, suits_str, bottom * tot])


	def get_total(self):
		return sum([card.value for card in self.cards])

	def get_card_count(self):
		return len(self.cards)

	# TODO: dealer hits, not hand
	def hit(self, deck):
		self.state = 'playing'
		self.cards += deck.draw()

	def stand(self, condition='stand'):
		self.state = condition


