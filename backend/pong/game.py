from .constants import *
import math
from .game_logic import PongGame
from .pongPlayer import PongPlayer
from .ball import Ball
from .game_stats import GameStats
import asyncio

class PongStatus:
    def __init__(self, ball, player_left, player_right):
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

    async def ai_move_paddle(self, target_y):
        error = target_y - self.player_right.y
        if abs(error) > AI_PADDLE_TOLERANCE:
            movement = math.copysign(min(abs(error), PLAYER_MOVEMENT_UNIT), error)
            self.player_right.y = self.game.move_player(self.player_right.y, movement)
            self.player_right.y = self.game.check_boundary(self.player_right.y)

    def update_ball_position(self):
        self.game.update_ball_position(self)

    def calculate_ai_steps(self):
        angle = self.ball.angle % (2 * math.pi)
        if math.pi / 2 <= angle <= 3 * math.pi / 2:
            return PLAYGROUND_HEIGHT // 2

        speed_x = math.cos(self.ball.angle) * self.ball.speed
        speed_y = math.sin(self.ball.angle) * self.ball.speed

        ball_x = self.ball.x
        ball_y = self.ball.y
        while ball_x < self.player_right.x:
            # Calculate the time until the next vertical wall collision
            if speed_x != 0:
                time_to_vertical_wall = (PLAYGROUND_WIDTH - ball_x) / speed_x if speed_x > 0 else ball_x / -speed_x
            else:
                time_to_vertical_wall = float('inf')

            # Calculate the time until the next horizontal wall collision
            if speed_y != 0:
                time_to_horizontal_wall = (PLAYGROUND_HEIGHT - ball_y) / speed_y if speed_y > 0 else ball_y / -speed_y
            else:
                time_to_horizontal_wall = float('inf')

            # Find the minimum time to the next collision
            time_to_collision = min(time_to_vertical_wall, time_to_horizontal_wall)

            ball_x += speed_x * time_to_collision
            ball_y += speed_y * time_to_collision

            # Check for collisions with walls and update the speed components
            if ball_x >= PLAYGROUND_WIDTH or ball_x <= 0:
                speed_x = -speed_x
                ball_x = max(min(ball_x, PLAYGROUND_WIDTH), 0)

            if ball_y >= PLAYGROUND_HEIGHT or ball_y <= 0:
                speed_y = -speed_y
                ball_y = max(min(ball_y, PLAYGROUND_HEIGHT), 0)

            # If the ball has reached or passed the paddle, stop the loop
            if ball_x >= self.player_right.x:
                break

        return ball_y

    def get_consts(self, left_name: str, right_name: str) -> dict[str, any]:
        game_consts = {
            'players': {
                'width': 2 * HALF_PLAYER_WIDTH,
                'height': 2 * HALF_PLAYER_HEIGHT,
                'left_name': left_name,
                'right_name': right_name
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
