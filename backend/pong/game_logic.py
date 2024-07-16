# pong/game_logic.py
from .constants import *
import math
import random


class PongGame:

    def __init__(self):
        self.vertical_distance = HALF_PLAYER_HEIGHT + HALF_BALL_SIZE
        self.horizontal_distance = HALF_PLAYER_WIDTH + HALF_BALL_SIZE
        self.collision_tolerance = COLLISION_TOLERANCE
        self.half_pi = math.pi / 2

    def generate_random_angle(self):
        while True:
            angle = random.uniform(0, 2 * math.pi)
            if MAX_BOUNCE_ANGLE_RAD <= angle <= self.half_pi - MAX_BOUNCE_ANGLE_RAD or \
                self.half_pi+ MAX_BOUNCE_ANGLE_RAD <= angle <= 3 * self.half_pi - MAX_BOUNCE_ANGLE_RAD:
                return angle

    def move_player(self, player_y, move_units):
        player_y += move_units
        return player_y

    def check_boundary(self, player_y):
        player_y = max(min(player_y, PLAYGROUND_HEIGHT - HALF_PLAYER_HEIGHT), HALF_PLAYER_HEIGHT)
        return player_y

    def kick_start_game(self, pong_stat):
        pong_stat.ball.angle = self.generate_random_angle()
        pong_stat.game_stats.game_started = True

    def update_ball_position(self, pong_stat):
        if pong_stat.game_stats.game_started:
            pong_stat.ball.x += pong_stat.ball.speed * math.cos(pong_stat.ball.angle)
            pong_stat.ball.y += pong_stat.ball.speed* math.sin(pong_stat.ball.angle)
            self.check_collisions(pong_stat)

    def check_ball_close_to_player(self, pong_stat, player):
        if abs(pong_stat.ball.x - player.x) < self.horizontal_distance + self.collision_tolerance:
            player_min = player.y - self.vertical_distance
            player_max = player.y + self.vertical_distance
            if player_min <= pong_stat.ball.y <= player_max:
                self.handle_player_collision(pong_stat, player.y)

    def check_player_ball_collision(self, pong_stat):
        self.check_ball_close_to_player(pong_stat, pong_stat.player_left)
        self.check_ball_close_to_player(pong_stat, pong_stat.player_right)

    def check_ball_wall_collision(self, pong_stat):
        if pong_stat.ball.y <= HALF_BALL_SIZE or pong_stat.ball.y >= PLAYGROUND_HEIGHT - HALF_BALL_SIZE:
            pong_stat.ball.angle = math.pi * 2 - pong_stat.ball.angle

    def check_scoring(self, pong_stat):
        if pong_stat.ball.x <= 0:
            self.handle_wall_collision(pong_stat, 'left')
        elif pong_stat.ball.x >= PLAYGROUND_WIDTH:
            self.handle_wall_collision(pong_stat, 'right')

    def check_collisions(self, pong_stat):
        self.check_player_ball_collision(pong_stat)
        self.check_ball_wall_collision(pong_stat)
        self.check_scoring(pong_stat)

    def handle_player_collision(self, pong_stat, player_y):
        ball_y = pong_stat.ball.y
        impact_point = ball_y - player_y
        normalized_impact_point = impact_point / HALF_PLAYER_HEIGHT
        new_angle = normalized_impact_point * MAX_BOUNCE_ANGLE_RAD * 2

        if self.half_pi <= pong_stat.ball.angle < 3 * self.half_pi:
            pong_stat.ball.angle = (new_angle)
        else:
            pong_stat.ball.angle = (math.pi - new_angle)
        pong_stat.ball.speed *= SPEED_UP_FACTOR
        self.collision_tolerance *= SPEED_UP_FACTOR

    def handle_wall_collision(self, pong_stat, wall):
        if wall == 'left':
            pong_stat.player_right.score += 1
        elif wall == 'right':
            pong_stat.player_left.score += 1

        if pong_stat.player_left.score == WINNING_SCORE:
            pong_stat.game_stats.game_over = True
            pong_stat.game_stats.winner = 'player_left'
            pong_stat.game_stats.loser = 'player_right'
        elif pong_stat.player_right.score == WINNING_SCORE:
            pong_stat.game_stats.game_over = True
            pong_stat.game_stats.winner = 'player_right'
            pong_stat.game_stats.loser = 'player_left'
        pong_stat.ball.x = PLAYGROUND_WIDTH / 2
        pong_stat.ball.y = PLAYGROUND_HEIGHT / 2
        pong_stat.ball.angle = self.generate_random_angle()
        pong_stat.ball.speed *= SLOW_DOWN_FACTOR
        self.collision_tolerance *= SLOW_DOWN_FACTOR

