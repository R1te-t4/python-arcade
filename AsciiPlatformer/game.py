"""
Game class - Main game logic and loop
"""
import time
import curses
from player import Player
from level import Level

class Game:
    """
    Main game class handling the game loop, rendering and input
    """
    def __init__(self, stdscr):
        """
        Initialize the game state
        Args:
            stdscr: Standard screen provided by curses
        """
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.running = True
        self.frame_rate = 15  # Frames per second
        self.frame_time = 1.0 / self.frame_rate
        self.score = 0
        self.level_num = 1
        
        # Initialize player and level with safe initial position
        player_x = max(1, self.width // 4)
        player_y = max(1, self.height - 10)
        self.player = Player(player_x, player_y)
        
        # Initialize level
        self.level = Level(max(10, self.width), max(10, self.height))
        self.level.generate_level(self.level_num)
        
        # Check if level loader returned a custom player position
        if hasattr(self.level, 'player_pos') and self.level.player_pos is not None:
            player_x, player_y = self.level.player_pos
            self.player.x = player_x
            self.player.y = player_y
        
        # Set up input
        stdscr.nodelay(True)  # Make getch non-blocking
        stdscr.keypad(True)   # Enable keypad mode for arrow keys
        
        # Game state
        self.state = "playing"  # "playing", "game_over", "win"

    def handle_input(self):
        """Handle keyboard input"""
        try:
            key = self.stdscr.getch()
            
            if key == curses.KEY_LEFT or key == ord('a'):
                self.player.move_left()
            elif key == curses.KEY_RIGHT or key == ord('d'):
                self.player.move_right()
            elif key == curses.KEY_UP or key == ord('w') or key == ord(' '):
                self.player.jump()
            elif key == ord('q'):
                self.running = False
            elif key == ord('r') and (self.state == "game_over" or self.state == "win"):
                self.reset_game()
        except Exception:
            # Handle any input errors gracefully
            pass

    def update(self):
        """Update game state"""
        # Apply gravity and update player position
        self.player.update(self.level)
        
        # Check for collisions with collectibles
        for coin in self.level.coins[:]:
            if (abs(self.player.x - coin[0]) < 2 and 
                abs(self.player.y - coin[1]) < 2):
                self.level.coins.remove(coin)
                self.score += 10
        
        # Check for collisions with obstacles
        for obstacle in self.level.obstacles:
            if (abs(self.player.x - obstacle[0]) < 2 and 
                abs(self.player.y - obstacle[1]) < 2):
                self.state = "game_over"
        
        # Check if player has fallen off the bottom of the screen
        if self.player.y >= self.height - 1:
            self.state = "game_over"
        
        # Check for level completion (all coins collected)
        if not self.level.coins:
            # Get the number of available levels
            num_levels = len(self.level.level_files)
            print(f"Level complete! Current level: {self.level_num}, Total levels: {num_levels}")
            
            if self.level_num < num_levels:
                self.level_num += 1
                print(f"Loading next level: {self.level_num}")
                self.level.generate_level(self.level_num)
            else:
                print("All levels complete! Player wins!")
                self.state = "win"
        
        # Check for screen resize
        new_height, new_width = self.stdscr.getmaxyx()
        if new_height != self.height or new_width != self.width:
            # Update dimensions regardless of size
            self.height, self.width = new_height, new_width
            # Always regenerate level on resize to ensure it fits
            self.level.regenerate(self.width, self.height, self.level_num)

    def render(self):
        """Render the game state to the terminal"""
        try:
            self.stdscr.clear()
            
            # Always render, even for small terminals - we'll just make our best effort
            # If the terminal is very small, we'll just show as much as we can
            
            # Draw platforms
            for platform in self.level.platforms:
                x, y, width = platform
                for i in range(width):
                    if 0 <= x + i < self.width - 1 and 0 <= y < self.height - 1:
                        try:
                            self.stdscr.addch(int(y), int(x + i), '=', curses.color_pair(2))
                        except:
                            # Silently ignore any errors when drawing
                            pass
            
            # Draw obstacles
            for obstacle in self.level.obstacles:
                x, y = obstacle
                if 0 <= x < self.width - 1 and 0 <= y < self.height - 1:
                    try:
                        self.stdscr.addch(int(y), int(x), 'X', curses.color_pair(3))
                    except:
                        pass
            
            # Draw coins
            for coin in self.level.coins:
                x, y = coin
                if 0 <= x < self.width - 1 and 0 <= y < self.height - 1:
                    try:
                        self.stdscr.addch(int(y), int(x), 'o', curses.color_pair(4))
                    except:
                        pass
            
            # Draw player
            if 0 <= self.player.x < self.width - 1 and 0 <= self.player.y < self.height - 1:
                try:
                    self.stdscr.addch(int(self.player.y), int(self.player.x), '@', curses.color_pair(1))
                except:
                    pass
            
            # Draw score and level info
            score_text = f"Score: {self.score}"
            if len(score_text) < self.width:
                try:
                    self.stdscr.addstr(0, 0, score_text)
                except:
                    pass
                    
            # Show current level information
            level_text = f"Level: {self.level_num}/{len(self.level.level_files)}"
            if len(level_text) < self.width:
                try:
                    self.stdscr.addstr(0, len(score_text) + 2, level_text)
                except:
                    pass
            
            # Draw controls if playing
            if self.state == "playing":
                controls = "Controls: ←/a ↓/s →/d, ↑/w/SPACE=jump, q=quit"
                if len(controls) < self.width:
                    try:
                        self.stdscr.addstr(self.height - 1, 0, controls)
                    except:
                        pass
            
            # Draw game over or win screen
            if self.state == "game_over":
                game_over_text = "GAME OVER! Press 'r' to restart or 'q' to quit"
                if len(game_over_text) < self.width and self.height > 5:
                    try:
                        self.stdscr.addstr(self.height // 2, max(0, (self.width - len(game_over_text)) // 2), 
                                          game_over_text, curses.A_BOLD)
                    except:
                        pass
            
            if self.state == "win":
                win_text = f"YOU WIN! Final Score: {self.score} - Press 'r' to restart or 'q' to quit"
                if len(win_text) < self.width and self.height > 5:
                    try:
                        self.stdscr.addstr(self.height // 2, max(0, (self.width - len(win_text)) // 2), 
                                          win_text, curses.A_BOLD)
                    except:
                        pass
            
            self.stdscr.refresh()
        except Exception as e:
            # Catch any rendering errors and try to recover
            try:
                self.stdscr.clear()
                if self.width > 20 and self.height > 3:
                    self.stdscr.addstr(0, 0, "Rendering error")
                self.stdscr.refresh()
            except:
                pass

    def reset_game(self):
        """Reset the game state for a new game"""
        self.score = 0
        self.level_num = 1
        
        # Initialize player with safe initial position
        player_x = max(1, self.width // 4)
        player_y = max(1, self.height - 10)
        self.player = Player(player_x, player_y)
        
        # Regenerate level
        self.level.generate_level(self.level_num)
        
        # Check if level loader returned a custom player position
        if hasattr(self.level, 'player_pos') and self.level.player_pos is not None:
            player_x, player_y = self.level.player_pos
            self.player.x = player_x
            self.player.y = player_y
            
        self.state = "playing"

    def run(self):
        """Main game loop"""
        last_frame_time = time.time()
        
        while self.running:
            # Calculate elapsed time
            current_time = time.time()
            delta_time = current_time - last_frame_time
            
            # Handle input
            self.handle_input()
            
            # Update game state if it's time for a new frame
            if delta_time >= self.frame_time:
                if self.state == "playing":
                    self.update()
                self.render()
                last_frame_time = current_time
            
            # Sleep to reduce CPU usage
            time.sleep(0.01)