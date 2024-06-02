# pong/game_logic.py
from .constants import *
import math


class PongGame:
    def __init__(self):
        # Initialize game state
        self.left_player_y = PLAYGROUND_HEIGHT // 2  # Initial position for left player (midpoint)
        self.right_player_x = PLAYGROUND_WIDTH - WALL_MARGIN
        self.left_player_x = WALL_MARGIN
        self.right_player_y = PLAYGROUND_HEIGHT // 2  # Initial position for right player (midpoint)
        self.ball_x = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH   # Initial position for ball (x-coordinate)
        self.ball_y = PLAYGROUND_HEIGHT // 2     # Initial position for ball (y-coordinate)
        self.ball_angle = 0  # Initial angle of the ball's movement
        self.game_started = False  # Indicates if the game has started
        self.game_over = False  # Indicates if the game is over
        self.winner = None  # Player who won
        self.loser = None  # Player who lost
        self.left_player_score = 0
        self.right_player_score = 0

    def update_positions(self, key_press):
        self.update_player_positions(key_press)
        self.update_ball_position()

    def update_player_positions(self, key_press):
        # Update player positions based on key press
        if not self.game_started and key_press in ('o', 'l'):
            # If player 2 moves, start the game
            self.kick_start_game(key_press)
        if key_press == 'w':
            self.left_player_y -= PLAYER_MOVEMENT_UNIT 
        elif key_press == 's':
            self.left_player_y += PLAYER_MOVEMENT_UNIT
        elif key_press == 'o':
            self.right_player_y -= PLAYER_MOVEMENT_UNIT
        elif key_press == 'l':
            self.right_player_y += PLAYER_MOVEMENT_UNIT
        
        # Ensure player positions stay within the bounds of the play area
        self.left_player_y = max(min(self.left_player_y, ( PLAYGROUND_HEIGHT / 2 ) - PLAYER_HEIGHT), 0)  # Bound lfet side player between 0 and (playground height / 2  - player height)
        self.right_player_y = max(min(self.right_player_y, ( PLAYGROUND_HEIGHT / 2 )  - PLAYER_HEIGHT), 0)  # Bound right side player between 0 and (playground height / 2 - player height)
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
        if self.ball_x <= self.left_player_x + PLAYER_WIDTH and self.left_player_y <= self.ball_y <= self.left_player_y + PLAYER_HEIGHT:
            self.handle_player_collision(self.left_player_y)
        elif self.ball_x >= self.right_player_x - BALL_WIDTH and self.right_player_y <= self.ball_y <= self.right_player_y + PLAYER_HEIGHT:
            self.handle_player_collision(self.right_player_y)
        
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
        relative_intersect_y = (self.left_player_y + PLAYER_HEIGHT / 2) - self.ball_y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)
        bounce_angle = normalized_intersect_y * (MAX_BOUNCE_ANGLE - MIN_BOUNCE_ANGLE)
        self.ball_angle = 180 - bounce_angle

    def handle_wall_collision(self, wall):       
        if wall == 'left':
            self.right_player_score += 1
        elif wall == 'right':
            self.left_player_score += 1
            
        if self.left_player_score == 5:
            self.game_over = True
            self.winner = 'left_player'
            self.loser = 'right_player'
        elif self.right_player_score == 5:
            self.game_over = True
            self.winner = 'right_player'
            self.loser = 'left_player'


    def get_game_state(self):
        game_state = {
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
            'left_player_mid_y': self.left_player_y,
            'left_player_start_x': self.left_player_x,
            'right_player_mid_y': self.right_player_y,
            'right_player_start_x': self.right_player_x,
            'game-over': self.game_over,
            'winner': self.winner,
            'loser': self.loser,
            'right_player_score': self.right_player_score,
            'left_player_score': self.left_player_score
        }
        return game_state
