from .constants import *
class Ball:
	x : float = PLAYGROUND_WIDTH // 2
	y : float = PLAYGROUND_HEIGHT // 2
	angle : float = 0
	speed : float = BALL_SPEED