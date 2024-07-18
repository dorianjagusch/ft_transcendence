from .constants import *
import math
from .game_logic import PongGame
from .pongPlayer import PongPlayer
from .ball import Ball
from .game_stats import GameStats
import asyncio
import sys

class PongStatus:
    def __init__(self, ball, player_left, player_right):
        # Initialize game state
        self.player_left = player_left
        self.player_right = player_right
        self.ball = ball
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

    async def ai_move_paddle(self):
        steps = self.calculate_ai_steps()
        move = self.calculate_ai_move()
        if move != PLAYER_AI_STAY:
            for i in range(steps):
                if move == PLAYER_AI_UP:
                    self.player_right.y = self.game.move_player(self.player_right.y, PLAYER_MOVEMENT_UNIT)
                elif move == PLAYER_AI_DOWN:
                    self.player_right.y = self.game.move_player(self.player_right.y, -PLAYER_MOVEMENT_UNIT)

                self.player_right.y = self.game.check_boundary(self.player_right.y)
                if steps > 1:
                    await asyncio.sleep(0.0001)
        self.player_left.y = self.game.check_boundary(self.player_left.y)
        self.game.update_ball_position(self)

    def update_ball_position(self):
        self.game.update_ball_position(self)

    def length(self, x, y):
        sum = x * x + y * y
        return math.sqrt(sum)

    def calculate_ai_move(self):
        if self.ball.y < self.player_right.y:
            return 'down'
        elif self.ball.y > self.player_right.y:
            return 'up'
        return 'stay'

    def calculate_ai_steps(self):
        dist_from_ball_x = self.ball.x - self.player_right.x
        dist_from_ball_y = self.ball.y - self.player_right.y
        dist_length = self.length(dist_from_ball_x, dist_from_ball_y)
        print(f"ball.x: {self.ball.y}", file=sys.stderr)
        print(f"distance from ball: {dist_length}", file=sys.stderr)

        # Look ahead factor depends on the speed and distance of the ball
        look_ahead_factor = dist_length / (PLAYER_MOVEMENT_UNIT + self.ball.speed)
        print(f"look ahead: {look_ahead_factor}", file=sys.stderr)
        if look_ahead_factor > 10:
            return 1
        elif look_ahead_factor > 5:
            return 2
        elif look_ahead_factor > 1:
            return 3
        else:
            return 0

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
