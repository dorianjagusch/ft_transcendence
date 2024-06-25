from .constants import *
class Ball:
	x : float = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH
	y : float = PLAYGROUND_HEIGHT // 2
	angle : float = 0