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

    def get_consts(self):
        game_consts = {
            'players': {
                'player-width': PLAYER_WIDTH,
                'player-height': PLAYER_HEIGHT,
            },
            'ball': {
                'ball-width': BALL_WIDTH,
                'ball-height': BALL_HEIGHT,
                'ball-speed': BALL_SPEED
            },
            'game': {
                'wall-margin': WALL_MARGIN,
                'playground-width': PLAYGROUND_WIDTH,
                'playground-hight': PLAYGROUND_HEIGHT
            }
        }
        return game_consts

    def get_game_state(self):
        game_state = {
            'ball': {
                'position': {
                'x': self.ball_x,
                'y': self.ball_y
                },
            },
            'players': {
                'left': {
                    'position': {
                        'x': self.player_left_x,
                        'y': self.player_left_y
                    },
                    'score': self.player_left_score
                },
                'right': {
                    'position': {
                        'x': self.player_right_x,
                        'y': self.player_right_y
                    },
                    'score': self.player_right_score
                }
            },
            'game': {
                'over': self.game_over,
                'winner': self.winner,
                'loser': self.loser
            }
        }
        return game_state