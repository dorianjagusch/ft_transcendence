from .constants import *
import math
from .game_logic import PongGame


class PongStatus:
    def __init__(self):
        # Initialize game state
        self.player_left_y = PLAYGROUND_HEIGHT // 2 
        self.player_right_x = PLAYGROUND_WIDTH - WALL_MARGIN
        self.player_left_x = WALL_MARGIN
        self.player_right_y = PLAYGROUND_HEIGHT // 2
        self.ball_x = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH
        self.ball_y = PLAYGROUND_HEIGHT // 2
        self.ball_angle = 0 
        self.game_started = False
        self.game_over = False
        self.winner = None
        self.loser = None
        self.player_left_score = 0
        self.player_right_score = 0
        self.game = PongGame()

    def update_positions(self, key_press):
        self.game.update_player_positions(self, key_press)
        self.game.update_ball_position(self)

    def update_ball_position(self):
        self.game.update_ball_position(self)

    def get_game_state(self):
        game_state = {
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
            'player_left_mid_y': self.player_left_y,
            'player_left_start_x': self.player_left_x,
            'player_right_mid_y': self.player_right_y,
            'player_right_start_x': self.player_right_x,
            'game-over': self.game_over,
            'winner': self.winner,
            'loser': self.loser,
            'player_right_score': self.player_right_score,
            'player_left_score': self.player_left_score
        }
        return game_state