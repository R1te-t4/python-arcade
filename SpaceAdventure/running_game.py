#!/usr/bin/env python3
# Heavily commented for you all to add to

import curses
import time
import random
import os
import sys

class SpaceAdventureGame:
    """
    A console-based space-flying game with ASCII graphics, obstacle avoidance, and score tracking.
    """
    
    def __init__(self, difficulty="easy"):
        # Game settings based on difficulty
        if difficulty == "easy":
            self.game_speed = 0.1  # Initial speed - lower is faster
            self.speed_increase = 0.001  # Speed increase after each obstacle
            self.min_speed = 0.05  # Minimum speed (maximum difficulty)
            self.obstacle_frequency = 0.3  # Chance to spawn obstacles
        elif difficulty == "medium":
            self.game_speed = 0.08  # Start faster
            self.speed_increase = 0.0015  # Increases faster
            self.min_speed = 0.04  # Higher maximum speed
            self.obstacle_frequency = 0.5  # More obstacles
        elif difficulty == "hard":
            self.game_speed = 0.06  # Start even faster
            self.speed_increase = 0.002  # Increases even faster
            self.min_speed = 0.03  # Highest maximum speed
            self.obstacle_frequency = 0.7  # Many more obstacles
        else:  # Default to easy
            self.game_speed = 0.1
            self.speed_increase = 0.001
            self.min_speed = 0.05
            self.obstacle_frequency = 0.3
            
        self.difficulty = difficulty
        self.player_x = 5  # Fixed player horizontal position
        self.player_y = 10  # Initial player vertical position in the middle
        self.score = 0
        self.obstacles = []  # List to hold obstacle positions
        self.width = 80  # Game width
        self.height = 20  # Game height
        self.running = True
        self.level = 1
        self.obstacles_passed = 0

        # Player and obstacle characters 
        self.player_char = "D"  # Player character (D stands for Da Character)
        self.obstacle_chars = ["#", "^", "%", "@"]  # Obstacle characters
        self.sky_chars = ["*", ".", "+"]  # Space decorations
        self.collectible_chars = ["$", "&", "O"]  # Collectible items
        self.collectibles = []  # List to hold collectible positions
        self.collected_items = 0  # Counter for collected items
        
        # Initialize the obstacles with some empty space at the beginning
        self.init_obstacles()
    
    def init_obstacles(self):
        """Initialize the obstacles with some spacing."""
        self.obstacles = []
        self.collectibles = []  # Reset collectibles
        # Start with empty space to give the player time to prepare
        starting_distance = 30
        obstacle_pos = self.width + starting_distance
        
        # Generate initial set of obstacles
        for _ in range(10):
            obstacle_height = random.randint(1, self.height - 5)
            obstacle_char = random.choice(self.obstacle_chars)
            self.obstacles.append({
                "x": obstacle_pos,
                "y": obstacle_height,
                "char": obstacle_char,
                "passed": False
            })
            
            # Randomly add collectibles between obstacles
            if random.random() < 0.4:  # 40% chance to spawn a collectible
                self.add_collectible(obstacle_pos - random.randint(5, 10))
                
            # Random distance between obstacles, increasing with level
            obstacle_pos += random.randint(15, 30 - min(10, self.level))
    
    def add_obstacle(self):
        """Add a new obstacle at the right edge of the screen."""
        if not self.obstacles or self.obstacles[-1]["x"] < self.width - 15:
            # Only add an obstacle based on difficulty-based frequency
            if random.random() < self.obstacle_frequency:
                obstacle_height = random.randint(1, self.height - 5)
                obstacle_char = random.choice(self.obstacle_chars)
                self.obstacles.append({
                    "x": self.width + 10,
                    "y": obstacle_height,
                    "char": obstacle_char,
                    "passed": False
                })
                
                # Chance to add a collectible near the new obstacle
                if random.random() < 0.3:  # 30% chance
                    self.add_collectible(self.width + random.randint(5, 15))
    
    def add_collectible(self, x_pos):
        """Add a collectible item at a specific x position with random y."""
        collectible_y = random.randint(4, self.height - 6)  # Positioned in the playable area
        collectible_char = random.choice(self.collectible_chars)
        value = 0
        
        # Assign different values based on rarity
        if collectible_char == "$":  # Coin 
            value = 5
        elif collectible_char == "&":  # Star
            value = 15
        elif collectible_char == "O":  # Diamond
            value = 30
            
        self.collectibles.append({
            "x": x_pos,
            "y": collectible_y,
            "char": collectible_char,
            "collected": False,
            "value": value
        })
    
    def update_obstacles(self):
        """Move obstacles to the left and remove those that are off-screen."""
        for obstacle in self.obstacles:
            obstacle["x"] -= 1
            
            # Check if player has passed this obstacle
            if not obstacle["passed"] and obstacle["x"] < self.player_x:
                obstacle["passed"] = True
                self.score += 10
                self.obstacles_passed += 1
                
                # Level up after every 5 obstacles
                if self.obstacles_passed % 5 == 0:
                    self.level += 1
                    # Increase speed with each level
                    self.game_speed = max(self.min_speed, self.game_speed - self.speed_increase * 5)
        
        # Remove obstacles that have moved off the screen
        self.obstacles = [obs for obs in self.obstacles if obs["x"] > -2]
        
        # Update collectibles
        self.update_collectibles()
        
        # Add new obstacles as needed
        self.add_obstacle()
        
    def update_collectibles(self):
        """Move collectibles to the left and check for collection."""
        for collectible in self.collectibles:
            collectible["x"] -= 1
            
            # Check if player has collected this item
            if not collectible["collected"] and self.check_collectible_collision(collectible):
                collectible["collected"] = True
                self.score += collectible["value"]
                self.collected_items += 1
        
        # Remove collectibles that are collected or off-screen
        self.collectibles = [col for col in self.collectibles if not col["collected"] and col["x"] > -2]
    
    def check_collectible_collision(self, collectible):
        """Check if player has collided with a collectible."""
        player_rect = {
            "x1": self.player_x, 
            "y1": self.player_y, 
            "x2": self.player_x + len(self.player_char), 
            "y2": self.player_y + 1
        }
        
        collectible_rect = {
            "x1": collectible["x"], 
            "y1": collectible["y"], 
            "x2": collectible["x"] + len(collectible["char"]), 
            "y2": collectible["y"] + 1
        }
        
        # Check for collision (simplified rectangle collision)
        if (player_rect["x1"] < collectible_rect["x2"] and
            player_rect["x2"] > collectible_rect["x1"] and
            player_rect["y1"] < collectible_rect["y2"] and
            player_rect["y2"] > collectible_rect["y1"]):
            return True
        
        return False
    
    def check_collision(self):
        """Check if player has collided with any obstacles."""
        player_rect = {
            "x1": self.player_x, 
            "y1": self.player_y, 
            "x2": self.player_x + len(self.player_char), 
            "y2": self.player_y + 1
        }
        
        for obstacle in self.obstacles:
            obstacle_rect = {
                "x1": obstacle["x"], 
                "y1": obstacle["y"], 
                "x2": obstacle["x"] + len(obstacle["char"]), 
                "y2": obstacle["y"] + 1
            }
            
            # Check for collision (simplified rectangle collision)
            if (player_rect["x1"] < obstacle_rect["x2"] and
                player_rect["x2"] > obstacle_rect["x1"] and
                player_rect["y1"] < obstacle_rect["y2"] and
                player_rect["y2"] > obstacle_rect["y1"]):
                return True
        
        return False
    
    def draw(self, stdscr):
        """Draw the game elements on the screen."""
        try:
            stdscr.clear()
            screen_height, screen_width = stdscr.getmaxyx()
            
            # Draw sky decorations
            self.draw_sky_decorations(stdscr)
            
            # No ground in space - removed ground drawing
                
            # Draw collectibles
            if curses.has_colors():
                stdscr.attron(curses.color_pair(3))  # Collectible color
            for collectible in self.collectibles:
                x, y = collectible["x"], collectible["y"]
                if 0 <= x < screen_width - 1 and 0 <= y < screen_height - 1:
                    stdscr.addstr(y, x, collectible["char"])
            
            # Draw player
            if curses.has_colors():
                stdscr.attron(curses.color_pair(1))  # Player color
            if 0 <= self.player_y < screen_height - 1 and 0 <= self.player_x < screen_width - 1:
                stdscr.addstr(self.player_y, self.player_x, self.player_char)
            
            # Draw obstacles
            if curses.has_colors():
                stdscr.attron(curses.color_pair(2))  # Obstacle color
            for obstacle in self.obstacles:
                x, y = obstacle["x"], obstacle["y"]
                if 0 <= x < screen_width - 1 and 0 <= y < screen_height - 1:
                    stdscr.addstr(y, x, obstacle["char"])
            
            # Reset color for text
            if curses.has_colors():
                stdscr.attroff(curses.color_pair(2))
                stdscr.attron(curses.color_pair(5))  # Use white for text
                
            # Draw score and level information
            score_text = f"Score: {self.score}"
            level_text = f"Level: {self.level}"
            speed_text = f"Speed: {int((1/self.game_speed) * 10)}"
            items_text = f"Items: {self.collected_items}"
            
            # Only display info if there's room
            if screen_height > 2:
                if 0 + len(score_text) + 2 < screen_width:
                    stdscr.addstr(1, 2, score_text)
                
                if 0 + len(score_text) + len(level_text) + 7 < screen_width:
                    stdscr.addstr(1, len(score_text) + 5, level_text)
                
                if 0 + len(score_text) + len(level_text) + len(speed_text) + 12 < screen_width:
                    stdscr.addstr(1, len(score_text) + len(level_text) + 10, speed_text)
                
                if 0 + len(score_text) + len(level_text) + len(speed_text) + len(items_text) + 17 < screen_width:
                    stdscr.addstr(1, len(score_text) + len(level_text) + len(speed_text) + 15, items_text)
            
            # Instructions - only if there's room
            instr_text = "w:up s:down q:quit"
            if screen_height > 4 and len(instr_text) + 2 < screen_width:
                stdscr.addstr(self.height - 1, 2, instr_text)
            
            # Refresh the screen
            stdscr.refresh()
            
        except curses.error:
            # Catch any curses errors silently to prevent crashing
            pass
        
    def draw_sky_decorations(self, stdscr):
        """Draw decorative elements in the sky."""
        try:
            # Get current screen dimensions
            screen_height, screen_width = stdscr.getmaxyx()
            
            # We'll create a semi-persistent sky pattern that moves slower than obstacles
            sky_time = int(time.time() * 2) # Changes every half second
            
            # Create a pseudo-random pattern based on time
            random.seed(sky_time)
            
            # Set sky element color
            if curses.has_colors():
                stdscr.attron(curses.color_pair(4))  # Sky decoration color
            
            # Draw more sky elements for space effect, but only if we have enough screen space
            if screen_height > 3:  # Make sure we have at least some space for stars
                for i in range(8):  # Increased from 3 to 8
                    x_pos = (sky_time + i * 10) % max(1, min(self.width, screen_width - 1))
                    # Ensure we have a valid range for y_pos
                    max_y = max(1, min(self.height - 3, screen_height - 2))
                    min_y = min(2, max_y)
                    y_pos = random.randint(min_y, max_y)
                    sky_char = random.choice(self.sky_chars)
                    
                    if 0 <= x_pos < screen_width - 1 and 0 <= y_pos < screen_height - 1:
                        stdscr.addstr(y_pos, x_pos, sky_char)
                    
            # Reset the random seed
            random.seed()
            
        except curses.error:
            # Catch any curses errors silently to prevent crashing
            pass
    
    def handle_input(self, stdscr):
        """Handle keyboard input."""
        stdscr.nodelay(True)  # Non-blocking input
        key = stdscr.getch()
        
        if key == ord('q'):
            self.running = False
        elif key == ord('w'):  # Move up
            self.player_y = max(1, self.player_y - 1)  # Changed from 2 to 1
        elif key == ord('s'):  # Move down
            self.player_y = min(self.height - 2, self.player_y + 1)  # Changed from 2 to 1
    
    def game_over(self, stdscr):
        """Display game over screen with animated stars and wait for input to restart or quit."""
        try:
            # Adjust time control for animations
            animation_speed = 0.1  # seconds between frames
            quit_game = False
            
            # Start time for animated stars
            start_time = time.time()
            
            # Non-blocking input during animation
            stdscr.nodelay(True)
            
            # Game over animation loop
            while not quit_game:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                # Draw animated stars in the background
                current_time = time.time()
                sky_time = int(current_time * 2)  # Changes every half second
                random.seed(sky_time)
                
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(4))  # Sky color
                
                # Draw more stars for the menu background, but only if we have enough screen space
                if height > 3:  # Make sure we have at least some space for stars
                    for i in range(15):  # More stars for effect
                        x_pos = (sky_time + i * 7) % max(1, width - 1)
                        # Ensure we have a valid range for y_pos
                        max_y = max(1, height - 2)
                        min_y = min(1, max_y)
                        y_pos = random.randint(min_y, max_y)
                        sky_char = random.choice(self.sky_chars)
                        
                        if 0 <= x_pos < width - 1 and 0 <= y_pos < height - 1:
                            stdscr.addstr(y_pos, x_pos, sky_char)
                
                # Reset the random seed
                random.seed()
                
                # Set color for game over text if available
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(2))  # Red text for game over
                    
                game_over_text = "GAME OVER"
                # Calculate positions, ensuring they're within screen boundaries
                game_over_y = max(0, min(height//2 - 4, height-2))
                game_over_x = max(0, min((width - len(game_over_text))//2, width-len(game_over_text)-1))
                if game_over_y < height-1 and game_over_x < width-len(game_over_text):
                    stdscr.addstr(game_over_y, game_over_x, game_over_text)
                
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(5))  # White text for stats
                    
                # Show difficulty level
                difficulty_text = f"Difficulty: {self.difficulty.capitalize()}"
                score_text = f"Your score: {self.score}"
                level_text = f"Level reached: {self.level}"
                items_text = f"Items collected: {self.collected_items}"
                
                # Difficulty text
                diff_y = max(0, min(height//2 - 3, height-2))
                diff_x = max(0, min((width - len(difficulty_text))//2, width-len(difficulty_text)-1))
                if diff_y < height-1 and diff_x < width-len(difficulty_text):
                    stdscr.addstr(diff_y, diff_x, difficulty_text)
                
                # Score text
                score_y = max(0, min(height//2 - 1, height-2))
                score_x = max(0, min((width - len(score_text))//2, width-len(score_text)-1))
                if score_y < height-1 and score_x < width-len(score_text):
                    stdscr.addstr(score_y, score_x, score_text)
                    
                # Level text
                level_y = max(0, min(height//2 + 1, height-2))
                level_x = max(0, min((width - len(level_text))//2, width-len(level_text)-1))
                if level_y < height-1 and level_x < width-len(level_text):
                    stdscr.addstr(level_y, level_x, level_text)
                    
                # Items text
                items_y = max(0, min(height//2 + 3, height-2))
                items_x = max(0, min((width - len(items_text))//2, width-len(items_text)-1))
                if items_y < height-1 and items_x < width-len(items_text):
                    stdscr.addstr(items_y, items_x, items_text)
                
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(3))  # Yellow for instructions
                    
                restart_text = "Press 'r' to restart or 'q' to quit"
                restart_y = max(0, min(height//2 + 5, height-2))
                restart_x = max(0, min((width - len(restart_text))//2, width-len(restart_text)-1))
                if restart_y < height-1 and restart_x < width-len(restart_text):
                    stdscr.addstr(restart_y, restart_x, restart_text)
                
                stdscr.refresh()
                
                # Check for input
                key = stdscr.getch()
                if key == ord('r'):
                    # Reset game state with same difficulty level
                    self.__init__(self.difficulty)
                    return True
                elif key == ord('q'):
                    return False
                
                # Control animation speed
                time.sleep(animation_speed)
                    
        except curses.error:
            # If there's an error, default to quitting
            return False
    
    def run(self, stdscr):
        """Main game loop."""
        # Set up the screen
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        
        # Get the screen dimensions
        screen_height, screen_width = stdscr.getmaxyx()
        # Adjust game dimensions based on screen size
        self.width = min(80, screen_width - 2)  # Leave some margin
        self.height = min(20, screen_height - 2)  # Leave some margin
        
        # Update player position for the new dimensions
        self.player_y = self.height // 2  # Position player in the middle of the screen
        
        # Initialize obstacles again for the new dimensions
        self.obstacles = []  # Clear obstacles
        self.collectibles = []  # Clear collectibles
        self.init_obstacles()  # Re-init with new dimensions
        
        # Initialize color pairs if terminal supports it
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Player color
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Obstacle color
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Collectible color
            curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Sky decoration color
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Ground color
        
        # Main game loop
        while self.running:
            # Handle input
            self.handle_input(stdscr)
            
            # Update game state
            self.update_obstacles()
            
            # Check for collisions
            if self.check_collision():
                if not self.game_over(stdscr):
                    break
            
            # Draw everything
            self.draw(stdscr)
            
            # Control game speed
            time.sleep(self.game_speed)
            
            # Make the game slightly faster over time
            self.game_speed = max(self.min_speed, self.game_speed - self.speed_increase)

    def start(self):
        """Start the game."""
        try:
            # Initialize curses
            curses.wrapper(self.run)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            pass
        finally:
            # Clean up
            print("\nThanks for playing!")


def show_start_menu(stdscr):
    """Display an animated start menu with difficulty selection."""
    # Set up colors
    curses.start_color()
    curses.curs_set(0)  # Hide cursor
    
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Player color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Red text
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow text
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan text (stars)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)   # White text
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta (selection)
    
    # Menu options
    options = ["Easy", "Medium", "Hard", "Quit"]
    selection = 0
    animation_speed = 0.1
    
    # Start menu loop
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw animated stars in the background
        current_time = time.time()
        sky_time = int(current_time * 2)  # Changes every half second
        random.seed(sky_time)
        
        # Star characters
        sky_chars = ["*", ".", "+", "•"]
        
        # Draw stars
        if curses.has_colors():
            stdscr.attron(curses.color_pair(4))  # Sky color
        
        # Draw many stars for menu background, but only if we have enough screen space
        if height > 3:  # Make sure we have at least some space for stars
            for i in range(15):
                x_pos = (sky_time + i * 7) % max(1, width - 1)
                # Ensure we have a valid range for y_pos
                max_y = max(1, height - 2)
                min_y = min(1, max_y)
                y_pos = random.randint(min_y, max_y)
                sky_char = random.choice(sky_chars)
                
                if 0 <= x_pos < width - 1 and 0 <= y_pos < height - 1:
                    stdscr.addstr(y_pos, x_pos, sky_char)
        
        # Reset the random seed
        random.seed()
        
        # Draw title
        if curses.has_colors():
            stdscr.attron(curses.color_pair(3))  # Yellow for title
        
        title = "SPACE ADVENTURE"
        title_y = max(0, min(height//4, height-2))
        title_x = max(0, min((width - len(title))//2, width-len(title)-1))
        if title_y < height-1 and title_x < width-len(title):
            stdscr.addstr(title_y, title_x, title)
            
        # Draw subtitle
        subtitle = "Navigate the cosmos and avoid space debris!"
        subtitle_y = title_y + 2
        subtitle_x = max(0, min((width - len(subtitle))//2, width-len(subtitle)-1))
        if subtitle_y < height-1 and subtitle_x < width-len(subtitle):
            stdscr.addstr(subtitle_y, subtitle_x, subtitle)
        
        # Draw instructions
        if curses.has_colors():
            stdscr.attron(curses.color_pair(5))  # White for instructions
            
        instr1 = "Use arrow keys or w/s to navigate menu"
        instr2 = "Press Enter to select difficulty"
        
        instr1_y = subtitle_y + 3
        instr1_x = max(0, min((width - len(instr1))//2, width-len(instr1)-1))
        if instr1_y < height-1 and instr1_x < width-len(instr1):
            stdscr.addstr(instr1_y, instr1_x, instr1)
            
        instr2_y = instr1_y + 1
        instr2_x = max(0, min((width - len(instr2))//2, width-len(instr2)-1))
        if instr2_y < height-1 and instr2_x < width-len(instr2):
            stdscr.addstr(instr2_y, instr2_x, instr2)
        
        # Draw menu options
        menu_start_y = instr2_y + 3
        
        for i, option in enumerate(options):
            menu_y = menu_start_y + i
            menu_x = max(0, min((width - len(option))//2, width-len(option)-1))
            
            if i == selection:
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(6))  # Highlight selected option
                option_text = f"> {option} <"
            else:
                if curses.has_colors():
                    stdscr.attron(curses.color_pair(3))  # Yellow for unselected
                option_text = f"  {option}  "
                
            if menu_y < height-1 and menu_x < width-len(option_text):
                stdscr.addstr(menu_y, menu_x, option_text)
        
        # Draw difficulty descriptions
        if curses.has_colors():
            stdscr.attron(curses.color_pair(5))  # White for descriptions
            
        desc_y = menu_start_y + len(options) + 2
        
        if selection == 0:  # Easy
            desc = "Beginner friendly with fewer obstacles"
        elif selection == 1:  # Medium
            desc = "Balanced challenge with moderate obstacles"
        elif selection == 2:  # Hard
            desc = "Intense challenge with many obstacles"
        else:  # Quit
            desc = "Exit the game"
            
        desc_x = max(0, min((width - len(desc))//2, width-len(desc)-1))
        if desc_y < height-1 and desc_x < width-len(desc):
            stdscr.addstr(desc_y, desc_x, desc)
        
        # Refresh the screen
        stdscr.refresh()
        
        # Get user input
        stdscr.timeout(int(animation_speed * 1000))  # Convert to milliseconds
        key = stdscr.getch()
        
        # Handle input
        if key == curses.KEY_UP or key == ord('w'):
            selection = (selection - 1) % len(options)
        elif key == curses.KEY_DOWN or key == ord('s'):
            selection = (selection + 1) % len(options)
        elif key == ord('\n') or key == ord(' '):  # Enter or Space
            if selection == 3:  # Quit
                return None
            else:
                difficulty = options[selection].lower()
                return difficulty
        
        # Continue animation
        time.sleep(animation_speed)

def main():
    """Main entry point for the game."""
    # Clear the console before starting
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=== SPACE ADVENTURE GAME ===")
    print("\nWelcome to the ultimate ASCII space adventure!")
    print("\nInstructions:")
    print("- Press 'w' to fly up")
    print("- Press 's' to fly down")
    print("- Press 'q' to quit the game")
    print("\nCollect items to boost your score:")
    print("- $ = 5 points")
    print("- & = 15 points")
    print("- O = 30 points")
    print("\nAvoid space debris (#, ^, %, @) as you navigate through the cosmos!")
    print("Your ship will move faster as you progress. Good luck, pilot!")
    print("\nStarting the game...")
    
    # Use curses to show the animated menu
    difficulty = curses.wrapper(show_start_menu)
    
    # If user selected quit, exit
    if difficulty is None:
        print("\nThanks for considering to play!")
        return
    
    # Start the game with selected difficulty
    game = SpaceAdventureGame(difficulty)
    game.start()


if __name__ == "__main__":
    main()
