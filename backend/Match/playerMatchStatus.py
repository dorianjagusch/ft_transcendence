from enum import Enum

class PlayerMatchStatus(Enum):
	NONE = 'none'
	WINS = 'wins'
	LOSSES = 'losses'

	@classmethod
	def choices(cls):
		return [(key.value, key.name.replace("_", " ").title()) for key in cls]