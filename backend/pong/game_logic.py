# pong/game_logic.py
from .constants import *
import math

class PongGame:
    def update_player_positions(self, pong_stat, key_press):
        # Update player positions based on key press
        if not pong_stat.game_started and key_press in ('o', 'l'):
            # If player 2 moves, start the game
            self.kick_start_game(pong_stat, key_press)
        if key_press == 'w':
            pong_stat.player_left_y -= PLAYER_MOVEMENT_UNIT 
        elif key_press == 's':
            pong_stat.player_left_y += PLAYER_MOVEMENT_UNIT
        elif key_press == 'o':
            pong_stat.player_right_y -= PLAYER_MOVEMENT_UNIT
        elif key_press == 'l':
            pong_stat.player_right_y += PLAYER_MOVEMENT_UNIT
        
        # Ensure player positions stay within the bounds of the play area
        pong_stat.player_left_y = max(min(pong_stat.player_left_y, PLAYGROUND_HEIGHT - (PLAYER_HEIGHT / 2 )), 0)  # Bound lfet side player between 0 and (playground height / 2  - player height)
        pong_stat.player_right_y = max(min(pong_stat.player_right_y, PLAYGROUND_HEIGHT - (PLAYER_HEIGHT / 2 )), 0)  # Bound right side player between 0 and (playground height / 2 - player height)
    
    def kick_start_game(self, pong_stat, key_press):
        # Kick start the game based on right side player's movement
        if key_press == 'o':
            # right side Player moves upward, set ball angle to 120 degrees
            pong_stat.ball_angle = 120
        elif key_press == 'l':
            # right side Player  moves downward, set ball angle to 240 degrees
            pong_stat.ball_angle = 240
        pong_stat.game_started = True



   # Update ball position based on angle
    def update_ball_position(self, pong_stat):
        if pong_stat.game_started:
            pong_stat.ball_x += BALL_SPEED * math.cos(math.radians(pong_stat.ball_angle))
            pong_stat.ball_y += BALL_SPEED * math.sin(math.radians(pong_stat.ball_angle))
            self.check_collisions(pong_stat)  # Check for collisions

    def check_collisions(self, pong_stat):
        # Check for collisions with players
        if pong_stat.ball_x <= pong_stat.player_left_x + PLAYER_WIDTH and pong_stat.player_left_y <= pong_stat.ball_y <= pong_stat.player_left_y + PLAYER_HEIGHT:
            self.handle_player_collision(pong_stat, pong_stat.player_left_y)
        elif pong_stat.ball_x >= pong_stat.player_right_x - BALL_WIDTH and pong_stat.player_right_y <= pong_stat.ball_y <= pong_stat.player_right_y + PLAYER_HEIGHT:
            self.handle_player_collision(pong_stat, pong_stat.player_right_y)
        
        # Check for collisions with top and bottom walls
        if pong_stat.ball_y <= 0 or pong_stat.ball_y >= PLAYGROUND_HEIGHT - BALL_HEIGHT:
            pong_stat.ball_angle = 360 - pong_stat.ball_angle
            
        # Check for collisions with vertical walls
        if pong_stat.ball_x <= 0:
            self.handle_wall_collision(pong_stat, 'left')
        elif pong_stat.ball_x >= PLAYGROUND_WIDTH - BALL_WIDTH:
            self.handle_wall_collision(pong_stat, 'right')


    def handle_player_collision(self, pong_stat, player_y):
        # Calculate new angle based on collision with player
        relative_intersect_y = (pong_stat.player_left_y + PLAYER_HEIGHT / 2) - pong_stat.ball_y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)
        bounce_angle = normalized_intersect_y * (MAX_BOUNCE_ANGLE - MIN_BOUNCE_ANGLE)
        pong_stat.ball_angle = 180 - bounce_angle

    def handle_wall_collision(self, pong_stat, wall):       
        if wall == 'left':
            pong_stat.player_right_score += 1
        elif wall == 'right':
            pong_stat.player_left_score += 1
            
        if pong_stat.player_left_score == 5:
            pong_stat.game_over = True
            pong_stat.winner = 'player_left'
            pong_stat.loser = 'player_right'
        elif pong_stat.player_right_score == 5:
            pong_stat.game_over = True
            pong_stat.winner = 'player_right'
            pong_stat.loser = 'player_left'

