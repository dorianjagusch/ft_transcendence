# pong/game_logic.py
from .constants import *

class PongGame:
    def __init__(self):
        # Initialize game state
        self.player1_y = PLAYGROUND_HEIGHT // 2  # Initial position for player 1 (midpoint)
        self.player2_x = PLAYGROUND_WIDTH - WALL_MARGIN
        self.player1_x = WALL_MARGIN
        self.player2_y = PLAYGROUND_HEIGHT // 2  # Initial position for player 2
        self.ball_x = PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH   # Initial position for ball (x-coordinate)
        self.ball_y = PLAYGROUND_HEIGHT // 2     # Initial position for ball (y-coordinate)

    def update_player_positions(self, key_press):
        # Update player positions based on key press
        if key_press == 'w':
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
        }
        return game_state
