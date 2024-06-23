from .constants import *
class Player:
	def __init__(self, x):
		self.x : float = x
		self.y : float = PLAYGROUND_HEIGHT // 2
		self.score : int = 0
