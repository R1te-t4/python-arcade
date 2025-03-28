"""
Game engine module for the Treasure Hunter game.
Coordinates game mechanics, input handling, and game state.
"""

import sys
import time
import random
import select

# Import platform-specific modules
if sys.platform == 'win32':
    import msvcrt
else:
    import tty
    import termios

from game.dungeon import DungeonGenerator
from game.player import Player
from game.display import (render_dungeon, show_help, game_over, 
                          clear_screen, display_event_message)

class GameEngine:
    """
    Main game engine for Treasure Hunter.
    Manages game state, processes input, and controls game flow.
    """
    
    def __init__(self, dungeon_width=25, dungeon_height=12):
        """Initialize the game engine with optimized default settings."""
        # Smaller dungeon for faster generation
        self.dungeon_width = dungeon_width
        self.dungeon_height = dungeon_height
        self.score = 0
        self.turns = 0
        self.running = False
        self.won = False
        
        # Game elements
        self.dungeon = None
        self.player = None
        self.revealed_cells = set()  # Cells that have been seen by the player
        
        # Pre-load some game elements
        self.dungeon_ready = False
    
    def start_game(self):
        """Start a new game with optimized dungeon generation."""
        # Generate a new dungeon with maximum retry attempts
        max_attempts = 3
        player_start = None
        
        for attempt in range(max_attempts):
            try:
                generator = DungeonGenerator(self.dungeon_width, self.dungeon_height)
                self.dungeon, player_start = generator.generate()
                self.dungeon_ready = True
                break
            except Exception as e:
                print(f"Dungeon generation failed (attempt {attempt+1}/{max_attempts}): {e}")
                if attempt == max_attempts - 1:
                    # If all attempts failed, create a simple fallback dungeon
                    self.dungeon, player_start = self._create_fallback_dungeon()
        
        # Make sure we have a valid player start position
        if not player_start:
            player_start = (2, 2)  # Default position as last resort
            
        # Create the player at the starting position
        self.player = Player(player_start[0], player_start[1])
        
        # Reset game state
        self.score = 100
        self.turns = 0
        self.running = True
        self.won = False
        self.revealed_cells = set()
        
        # Run the game loop
        self.game_loop()
        
    def _create_fallback_dungeon(self):
        """Create a simple fallback dungeon if generation fails."""
        width, height = self.dungeon_width, self.dungeon_height
        # Create a simple dungeon with walls around the edges
        self.dungeon = [['#' for _ in range(width)] for _ in range(height)]
        
        # Fill interior with empty space
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                self.dungeon[y][x] = '.'
        
        # Add some random walls
        for _ in range(width * height // 10):
            x, y = random.randint(1, width - 2), random.randint(1, height - 2)
            self.dungeon[y][x] = '#'
        
        # Place player start, exit, and treasure
        player_start = (2, 2)
        self.dungeon[height-2][width-2] = 'E'  # Exit in bottom-right
        self.dungeon[height//2][width//2] = '$'  # Treasure in middle
        
        # Add a few traps and monsters
        for _ in range(3):
            x, y = random.randint(3, width - 3), random.randint(3, height - 3)
            if self.dungeon[y][x] == '.':
                self.dungeon[y][x] = 'T'
                
        for _ in range(2):
            x, y = random.randint(3, width - 3), random.randint(3, height - 3)
            if self.dungeon[y][x] == '.':
                self.dungeon[y][x] = 'M'
                
        self.dungeon_ready = True
        
        # Return the player start position 
        return self.dungeon, player_start
    
    def game_loop(self):
        """Main game loop with improved performance."""
        last_render_time = 0
        
        # Give the player an initial score if they don't have one
        if not hasattr(self.player, 'score') or self.player.score == 0:
            self.player.score = 100
            
        while self.running:
            # Update revealed cells based on player's vision
            self._update_revealed_cells()
            
            # Get current time to throttle rendering if needed
            current_time = time.time()
            
            # Render the current game state 
            # Using player's score directly
            render_dungeon(self.dungeon, self.player, self.revealed_cells, 
                          self.player.score, self.player.health, self.turns)
            last_render_time = current_time
            
            # Get player input
            action = self._get_input()
            
            # Only process action if it's not None
            if action:
                self._process_action(action)
                
                # Check game conditions
                if not self.player.is_alive():
                    self.running = False
                    game_over(False, self.player.score, self.turns)
                    break
                
                # Reduce score slightly each turn to encourage efficiency
                if self.running:
                    # Take score from player object now
                    self.player.score = max(0, self.player.score - 1)
                    self.turns += 1
    
    def _get_input(self):
        """
        Get keyboard input from the player in a Replit-compatible way.
        
        Returns:
            str: The key pressed by the player
        """
        # For Replit environment, use a simple input with a prompt
        # This approach works in web-based terminals
        print("\033[1mEnter move (w/a/s/d/h/q): \033[0m", end='', flush=True)
        try:
            # Set a shorter timeout for input to keep the game responsive
            import sys
            if select.select([sys.stdin], [], [], 0.5)[0]:
                key = input().lower()
                if key:  # Only process if something was entered
                    return key[0]  # Return just the first character
            
            # If no input was received, return None
            return None
        except Exception as e:
            print(f"Input error: {e}")
            # Give a small delay to prevent CPU spikes
            time.sleep(0.1)
            return None
    
    def _process_action(self, action):
        """
        Process the player's action.
        
        Args:
            action: The key pressed by the player
        """
        if action == 'q':
            # Quit the game
            self.running = False
            clear_screen()
            print("\nThanks for playing Treasure Hunter!")
            sys.exit(0)
        
        elif action == 'h':
            # Show help
            show_help()
        
        elif action in ['w', 'a', 's', 'd']:
            # Movement
            dx, dy = 0, 0
            
            if action == 'w':  # Up
                dy = -1
            elif action == 's':  # Down
                dy = 1
            elif action == 'a':  # Left
                dx = -1
            elif action == 'd':  # Right
                dx = 1
            
            # Try to move the player
            moved, cell_content, message = self.player.move(dx, dy, self.dungeon)
            
            if moved:
                # Display the message about what happened
                display_event_message(message, 'cyan')
                
                # Check for win condition
                if cell_content == 'E' and self.player.has_treasure:
                    self.won = True
                    self.running = False
                    # Bonus points for finishing with more health and fewer turns
                    health_bonus = self.player.health * 25
                    efficiency_bonus = max(0, 200 - self.turns)
                    self.player.score += health_bonus + efficiency_bonus
                    game_over(True, self.player.score, self.turns)
    
    def _update_revealed_cells(self):
        """Update the set of cells that have been revealed to the player."""
        # Add currently visible cells to the set of revealed cells
        visible = self.player.get_visible_cells(self.dungeon)
        self.revealed_cells.update(visible)
