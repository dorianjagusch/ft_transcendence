from .constants import *
import math


class PongStatus:
    def __init__(self):
        # Initialize game state
        self.left_player_y = PLAYGROUND_HEIGHT // 2  # Initial position for left player (midpoint)
        self.right_player_x = PLAYGROUND_WIDTH - WALL_MARGIN
        self.left_player_x = WALL_MARGIN
        self.right_player_y = PLAYGROUND_HEIGHT // 2  # Initial position for right player (midpoint)
        self.ball_x = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH   # Initial position for ball (x-coordinate)
        self.ball_y = PLAYGROUND_HEIGHT // 2     # Initial position for ball (y-coordinate)
        self.ball_angle = 0  # Initial angle of the ball's movement
        self.game_started = False  # Indicates if the game has started
        self.game_over = False  # Indicates if the game is over
        self.winner = None  # Player who won
        self.loser = None  # Player who lost
        self.left_player_score = 0
        self.right_player_score = 0