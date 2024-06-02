# pong/game_logic.py
from .constants import *
import math


class PongGame:
    def __init__(self):
        # Initialize game state
        self.player_left_y = PLAYGROUND_HEIGHT // 2  # Initial position for left player (midpoint)
        self.player_right_x = PLAYGROUND_WIDTH - WALL_MARGIN
        self.player_left_x = WALL_MARGIN
        self.player_right_y = PLAYGROUND_HEIGHT // 2  # Initial position for right player (midpoint)
        self.ball_x = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH   # Initial position for ball (x-coordinate)
        self.ball_y = PLAYGROUND_HEIGHT // 2     # Initial position for ball (y-coordinate)
        self.ball_angle = 0  # Initial angle of the ball's movement
        self.game_started = False  # Indicates if the game has started
        self.game_over = False  # Indicates if the game is over
        self.winner = None  # Player who won
        self.loser = None  # Player who lost
        self.player_left_score = 0
        self.player_right_score = 0

    def update_positions(self, key_press):
        self.update_player_positions(key_press)
        self.update_ball_position()

    def update_player_positions(self, key_press):
        # Update player positions based on key press
        if not self.game_started and key_press in ('o', 'l'):
            # If player 2 moves, start the game
            self.kick_start_game(key_press)
        if key_press == 'w':
            self.player_left_y -= PLAYER_MOVEMENT_UNIT 
        elif key_press == 's':
            self.player_left_y += PLAYER_MOVEMENT_UNIT
        elif key_press == 'o':
            self.player_right_y -= PLAYER_MOVEMENT_UNIT
        elif key_press == 'l':
            self.player_right_y += PLAYER_MOVEMENT_UNIT
        
        # Ensure player positions stay within the bounds of the play area
        self.player_left_y = max(min(self.player_left_y, ( PLAYGROUND_HEIGHT / 2 ) - PLAYER_HEIGHT), 0)  # Bound lfet side player between 0 and (playground height / 2  - player height)
        self.player_right_y = max(min(self.player_right_y, ( PLAYGROUND_HEIGHT / 2 )  - PLAYER_HEIGHT), 0)  # Bound right side player between 0 and (playground height / 2 - player height)
    def kick_start_game(self, key_press):
        # Kick start the game based on right side player's movement
        if key_press == 'o':
            # right side Player moves upward, set ball angle to 120 degrees
            self.ball_angle = 120
        elif key_press == 'l':
            # right side Player  moves downward, set ball angle to 240 degrees
            self.ball_angle = 240
        
        self.game_started = True
    
    # Update ball position based on angle
    def update_ball_position(self):
        if self.game_started:
            self.ball_x += BALL_SPEED * math.cos(math.radians(self.ball_angle))
            self.ball_y += BALL_SPEED * math.sin(math.radians(self.ball_angle))
            self.check_collisions()  # Check for collisions

    def check_collisions(self):
        # Check for collisions with players
        if self.ball_x <= self.player_left_x + PLAYER_WIDTH and self.player_left_y <= self.ball_y <= self.player_left_y + PLAYER_HEIGHT:
            self.handle_player_collision(self.player_left_y)
        elif self.ball_x >= self.player_right_x - BALL_WIDTH and self.player_right_y <= self.ball_y <= self.player_right_y + PLAYER_HEIGHT:
            self.handle_player_collision(self.player_right_y)
        
        # Check for collisions with top and bottom walls
        if self.ball_y <= 0 or self.ball_y >= PLAYGROUND_HEIGHT - BALL_HEIGHT:
            self.ball_angle = 360 - self.ball_angle
            
        # Check for collisions with vertical walls
        if self.ball_x <= 0:
            self.handle_wall_collision('left')
        elif self.ball_x >= PLAYGROUND_WIDTH - BALL_WIDTH:
            self.handle_wall_collision('right')


    def handle_player_collision(self, player_y):
        # Calculate new angle based on collision with player
        relative_intersect_y = (self.player_left_y + PLAYER_HEIGHT / 2) - self.ball_y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)
        bounce_angle = normalized_intersect_y * (MAX_BOUNCE_ANGLE - MIN_BOUNCE_ANGLE)
        self.ball_angle = 180 - bounce_angle

    def handle_wall_collision(self, wall):       
        if wall == 'left':
            self.player_right_score += 1
        elif wall == 'right':
            self.player_left_score += 1
            
        if self.player_left_score == 5:
            self.game_over = True
            self.winner = 'player_left'
            self.loser = 'player_right'
        elif self.player_right_score == 5:
            self.game_over = True
            self.winner = 'player_right'
            self.loser = 'player_left'


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
