# pong/game_logic.py
from .constants import *
import math


class PongGame:
    def move_player(self, player_y , move_units):
        player_y += move_units
        return player_y

    def check_boundery(self, player_y):
        player_y = max(min(player_y, PLAYGROUND_HEIGHT - (PLAYER_HEIGHT / 2 )), 0)
        return player_y
    
    def kick_start_game(self, pong_stat, move):
        # Kick start the game based on right side player's movement
        if move == PLAYER_RIGHT_UP:
            # right side Player moves upward, set ball angle to 120 degrees
            pong_stat.ball.angle = 120
        elif move == PLAYER_RIGHT_DOWN:
            # right side Player  moves downward, set ball angle to 240 degrees
            pong_stat.ball.angle = 240
        pong_stat.game_stats.game_started = True

    def update_ball_position(self, pong_stat):
        if pong_stat.game_stats.game_started:
            pong_stat.ball.x += BALL_SPEED * math.cos(math.radians(pong_stat.ball.angle))
            pong_stat.ball.y += BALL_SPEED * math.sin(math.radians(pong_stat.ball.angle))
            self.check_collisions(pong_stat)

    def check_collisions(self, pong_stat):
        # Check for collisions with players
        if pong_stat.ball.x <= pong_stat.player_left.x + PLAYER_WIDTH and pong_stat.player_left.y <= pong_stat.ball.y <= pong_stat.player_left.y + PLAYER_HEIGHT:
            self.handle_player_collision(pong_stat, pong_stat.player_left.y)
        elif pong_stat.ball.x >= pong_stat.player_right.x - BALL_WIDTH and pong_stat.player_right.y <= pong_stat.ball.y <= pong_stat.player_right.y + PLAYER_HEIGHT:
            self.handle_player_collision(pong_stat, pong_stat.player_right.y)

        # Check for collisions with top and bottom walls
        if pong_stat.ball.y <= 0 or pong_stat.ball.y >= PLAYGROUND_HEIGHT - BALL_HEIGHT:
            pong_stat.ball.angle = 360 - pong_stat.ball.angle

        # Check for collisions with vertical walls
        if pong_stat.ball.x <= 0:
            self.handle_wall_collision(pong_stat, 'left')
        elif pong_stat.ball.x >= PLAYGROUND_WIDTH - BALL_WIDTH:
            self.handle_wall_collision(pong_stat, 'right')

    def handle_player_collision(self, pong_stat, player_y):
        # Calculate new angle based on collision with player
        relative_intersect_y = (pong_stat.player_left.y + PLAYER_HEIGHT / 2) - pong_stat.ball.y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)
        bounce_angle = normalized_intersect_y * (MAX_BOUNCE_ANGLE - MIN_BOUNCE_ANGLE)
        pong_stat.ball.angle = 180 - bounce_angle

    def handle_wall_collision(self, pong_stat, wall):
        if wall == 'left':
            pong_stat.player_right.score += 1
        elif wall == 'right':
            pong_stat.player_left.score += 1

        if pong_stat.player_left.score == 5:
            pong_stat.game_stats.game_over = True
            pong_stat.game_stats.winner = 'player_left'
            pong_stat.game_stats.loser = 'player_right'
        elif pong_stat.player_right.score == 5:
            pong_stat.game_stats.game_over = True
            pong_stat.game_stats.winner = 'player_right'
            pong_stat.game_stats.loser = 'player_left'

