class Hand:
	def __init__(self, deck, person_type='player'):
		self.cards = deck.draw(2)
		self.person = person_type
