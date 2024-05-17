# pong/game_logic.py
from .constants import *
import math


class PongGame:
    def __init__(self):
        # Initialize game state
        self.player1_y = PLAYGROUND_HEIGHT // 2  # Initial position for player 1 (midpoint)
        self.player2_x = PLAYGROUND_WIDTH - WALL_MARGIN
        self.player1_x = WALL_MARGIN
        self.player2_y = PLAYGROUND_HEIGHT // 2  # Initial position for player 2 (midpoint)
        self.ball_x = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH   # Initial position for ball (x-coordinate)
        self.ball_y = PLAYGROUND_HEIGHT // 2     # Initial position for ball (y-coordinate)
        self.ball_angle = 0  # Initial angle of the ball's movement
        self.game_started = False  # Indicates if the game has started
        self.game_over = False  # Indicates if the game is over
        self.winner = None  # Player who won
        self.loser = None  # Player who lost

    def update_positions(self, key_press):
        self.update_player_positions(key_press)
        self.update_ball_position()

    def update_player_positions(self, key_press):
        # Update player positions based on key press
        if not self.game_started and key_press in ('o', 'l'):
            # If player 2 moves, start the game
            self.kick_start_game(key_press)
        elif key_press == 'w':
            self.player1_y -= PLAYER_MOVEMENT_UNIT  # Move player 1 up
        elif key_press == 's':
            self.player1_y += PLAYER_MOVEMENT_UNIT  # Move player 1 down
        elif key_press == 'o':
            self.player2_y -= PLAYER_MOVEMENT_UNIT  # Move player 2 up
        elif key_press == 'l':
            self.player2_y += PLAYER_MOVEMENT_UNIT  # Move player 2 down
        
        # Ensure player positions stay within the bounds of the play area
        self.player1_y = max(min(self.player1_y, PLAYGROUND_HEIGHT - PLAYER_HEIGHT), 0)  # Bound player 1 between 0 and (playground height - player height)
        self.player2_y = max(min(self.player2_y, PLAYGROUND_HEIGHT - PLAYER_HEIGHT), 0)  # Bound player 2 between 0 and (playground height - player height)
    def kick_start_game(self, key_press):
        # Kick start the game based on player 2's movement
        if key_press == 'o':
            # Player 2 moves upward, set ball angle to 120 degrees
            self.ball_angle = 120
        elif key_press == 'l':
            # Player 2 moves downward, set ball angle to 240 degrees
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
        if self.ball_x <= self.player1_x + PLAYER_WIDTH and self.player1_y <= self.ball_y <= self.player1_y + PLAYER_HEIGHT:
            self.handle_player_collision(self.player1_y)
        elif self.ball_x >= self.player2_x - BALL_WIDTH and self.player2_y <= self.ball_y <= self.player2_y + PLAYER_HEIGHT:
            self.handle_player_collision(self.player2_y)
        
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
        relative_intersect_y = (self.player1_y + PLAYER_HEIGHT / 2) - self.ball_y
        normalized_intersect_y = relative_intersect_y / (PLAYER_HEIGHT / 2)
        bounce_angle = normalized_intersect_y * (MAX_BOUNCE_ANGLE - MIN_BOUNCE_ANGLE)
        self.ball_angle = 180 - bounce_angle

    def handle_wall_collision(self, wall):
        # Game over, set winner and loser
        self.game_over = True
        if wall == 'left':
            self.winner = 'player2'
            self.loser = 'player1'
        elif wall == 'right':
            self.winner = 'player1'
            self.loser = 'player2'

    def get_game_state(self):
        # Construct JSON message with player and ball positions
        game_state = {
            'player-width' : PLAYER_WIDTH,
            'player-height' : PLAYER_HEIGHT,
            'player1_mid_y': self.player1_y,
            'player1_start_x': self.player1_x,
            'player2_mid_y': self.player2_y,
            'player2_start_x': self.player2_x,
            'ball-width' : BALL_WIDTH,
            'ball-height' : BALL_HEIGHT,
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
            'wall-margin' : WALL_MARGIN,
            'game-over': self.game_over,
            'winner': self.winner,
            'loser': self.loser
        }
        return game_state
