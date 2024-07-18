from .constants import *
import math
from .game_logic import PongGame
from .player import Player
from .ball import Ball
from .game_stats import GameStats
import sys

class PongStatus:
    def __init__(self):
        # Initialize game state
        self.player_left = Player(WALL_MARGIN)
        self.player_right = Player(PLAYGROUND_WIDTH - WALL_MARGIN)
        self.ball = Ball()
        self.game_stats = GameStats()
        self.ai_opponent = False
        self.game = PongGame()

    def use_ai_opponent(self):
        self.ai_opponent = True

    def update_positions(self, move):
        if not self.game_stats.game_started and move == START_PAUSE_GAME:
            self.game.kick_start_game(self)
        if move == PLAYER_LEFT_UP:
            self.player_left.y = self.game.move_player(self.player_left.y, PLAYER_MOVEMENT_UNIT)
        elif move == PLAYER_LEFT_DOWN:
            self.player_left.y = self.game.move_player(self.player_left.y, -PLAYER_MOVEMENT_UNIT)

        if self.ai_opponent is False:
            if move == PLAYER_RIGHT_UP:
                self.player_right.y = self.game.move_player(self.player_right.y, PLAYER_MOVEMENT_UNIT)
            elif move == PLAYER_RIGHT_DOWN:
                self.player_right.y = self.game.move_player(self.player_right.y, -PLAYER_MOVEMENT_UNIT)
        self.player_right.y = self.game.check_boundary(self.player_right.y)
        self.player_left.y = self.game.check_boundary(self.player_left.y)
        self.game.update_ball_position(self)

    def ai_move_paddle(self):
        move = self.calculate_ai_position()
        if move == PLAYER_AI_UP:
            self.player_right.y = self.game.move_player(self.player_right.y, PLAYER_MOVEMENT_UNIT)
        elif move == PLAYER_AI_DOWN:
            self.player_right.y = self.game.move_player(self.player_right.y, -PLAYER_MOVEMENT_UNIT)
        self.player_right.y = self.game.check_boundary(self.player_right.y)
        self.player_left.y = self.game.check_boundary(self.player_left.y)
        self.game.update_ball_position(self)

    def update_ball_position(self):
        self.game.update_ball_position(self)

    def calculate_ai_position(self):
        return 'up'

    def get_consts(self):
        game_consts = {
            'players': {
                'width': 2 * HALF_PLAYER_WIDTH,
                'height': 2 * HALF_PLAYER_HEIGHT,
            },
            'ball': {
                'size': 2 * HALF_BALL_SIZE
            },
            'game': {
                'margin': WALL_MARGIN,
                'width': PLAYGROUND_WIDTH,
                'height': PLAYGROUND_HEIGHT
            }
        }
        return game_consts

    def get_game_state(self):
        game_state = {
            'ball': {
                'position': {
                'x': self.ball.x,
                'y': self.ball.y
                },
            },
            'players': {
                'left': {
                    'position': {
                        'x': self.player_left.x,
                        'y': self.player_left.y
                    },
                    'score': self.player_left.score
                },
                'right': {
                    'position': {
                        'x': self.player_right.x,
                        'y': self.player_right.y
                    },
                    'score': self.player_right.score
                }
            },
            'game': {
                'over': self.game_stats.game_over,
                'winner': self.game_stats.winner,
                'loser': self.game_stats.loser
            }
        }
        return game_state
