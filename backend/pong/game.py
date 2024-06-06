from .constants import *
import math
from .game_logic import PongGame
from .player import Player
from .ball import Ball
from .game_stats import GameStats

class PongStatus:
    def __init__(self):
        # Initialize game state
        self.player_left = Player(WALL_MARGIN)
        self.player_right = Player(PLAYGROUND_WIDTH - WALL_MARGIN)
        self.ball = Ball()
        self.game_stats = GameStats()
        self.game = PongGame()
        

    def update_positions(self, key_press):
        if not self.game_started and key_press in ('o', 'l'):
            self.game.kick_start_game(self, key_press)
        if key_press == 'w':
            self.player_left.y = self.game.move_player(self.player_left.y, PLAYER_MOVEMENT_UNIT)
        elif key_press == 's':
            self.player_left.y = self.game.move_player(self.player_left.y, -PLAYER_MOVEMENT_UNIT)
        elif key_press == 'o':
            self.player_right.y = self.game.move_player(self.player_right.y, PLAYER_MOVEMENT_UNIT)
        elif key_press == 'l':
            self.player_right.y = self.game.move_player(self.player_right.y, -PLAYER_MOVEMENT_UNIT)
        self.player_right.y = self.game.check_boundery(self.player_right.y)
        self.player_left.y = self.game.check_boundery(self.player_left.y)
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