"""
Level Editor - Create and edit level files for ASCII Platformer
"""
import os
import curses
import time
from level_loader import LevelLoader


class LevelEditor:
    """
    Simple level editor for creating ASCII Platformer levels
    """
    def __init__(self, stdscr):
        """
        Initialize the level editor
        
        Args:
            stdscr: Curses standard screen
        """
        self.stdscr = stdscr
        self.loader = LevelLoader()
        
        # Get terminal size
        self.height, self.width = stdscr.getmaxyx()
        
        # Set up curses
        curses.curs_set(1)  # Show cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Player
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Platform
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Obstacle
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Coin
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # UI Text
        
        # Initialize grid and editor state
        self.level_width = min(40, self.width - 2)
        self.level_height = min(20, self.height - 2)
        self.grid = [[' ' for _ in range(self.level_width)] for _ in range(self.level_height)]
        
        # Add ground at the bottom
        for x in range(self.level_width):
            self.grid[self.level_height - 1][x] = '='
            
        # Set player position
        self.grid[self.level_height - 2][1] = 'P'
        
        # Editor state
        self.current_tool = '='  # Default tool (platform)
        self.cursor_x = 1
        self.cursor_y = 1
        self.running = True
        self.current_file = None
        self.message = "Welcome to Level Editor! Press 'h' for help."
        
    def render(self):
        """Render the level editor UI"""
        self.stdscr.clear()
        
        # Draw the grid
        for y in range(self.level_height):
            for x in range(self.level_width):
                char = self.grid[y][x]
                color_pair = 0
                
                if char == 'P':
                    color_pair = 1
                elif char == '=':
                    color_pair = 2
                elif char == 'X':
                    color_pair = 3
                elif char == 'o':
                    color_pair = 4
                
                try:
                    self.stdscr.addch(y + 1, x + 1, char, curses.color_pair(color_pair))
                except:
                    pass
                
        # Draw UI elements
        if self.height > self.level_height + 2:
            status_line = f"Tool: {self.current_tool} | "
            status_line += f"Cursor: ({self.cursor_x}, {self.cursor_y}) | "
            status_line += f"Size: {self.level_width}x{self.level_height}"
            
            try:
                self.stdscr.addstr(self.level_height + 2, 1, status_line, curses.color_pair(5))
                
                if self.current_file:
                    self.stdscr.addstr(self.level_height + 3, 1, f"Current file: {self.current_file}", curses.color_pair(5))
                else:
                    self.stdscr.addstr(self.level_height + 3, 1, "No file loaded/saved", curses.color_pair(5))
                    
                self.stdscr.addstr(self.level_height + 4, 1, self.message, curses.color_pair(5))
            except:
                pass
                
        # Draw cursor
        try:
            self.stdscr.move(self.cursor_y + 1, self.cursor_x + 1)
        except:
            pass
            
        self.stdscr.refresh()
        
    def handle_input(self):
        """Handle keyboard input"""
        try:
            key = self.stdscr.getch()
            
            # Movement
            if key == curses.KEY_UP:
                self.cursor_y = max(0, self.cursor_y - 1)
            elif key == curses.KEY_DOWN:
                self.cursor_y = min(self.level_height - 1, self.cursor_y + 1)
            elif key == curses.KEY_LEFT:
                self.cursor_x = max(0, self.cursor_x - 1)
            elif key == curses.KEY_RIGHT:
                self.cursor_x = min(self.level_width - 1, self.cursor_x + 1)
            
            # Tool selection
            elif key == ord('p'):
                self.current_tool = 'P'
                self.message = "Selected: Player start position"
            elif key == ord('='):
                self.current_tool = '='
                self.message = "Selected: Platform"
            elif key == ord('x'):
                self.current_tool = 'X'
                self.message = "Selected: Obstacle"
            elif key == ord('o'):
                self.current_tool = 'o'
                self.message = "Selected: Coin"
            elif key == ord(' '):
                self.current_tool = ' '
                self.message = "Selected: Eraser"
                
            # Place the current tool at cursor position
            elif key == 10:  # Enter key
                # If this is the player position, remove any existing player marker
                if self.current_tool == 'P':
                    for y in range(self.level_height):
                        for x in range(self.level_width):
                            if self.grid[y][x] == 'P':
                                self.grid[y][x] = ' '
                                
                self.grid[self.cursor_y][self.cursor_x] = self.current_tool
                
            # File operations
            elif key == ord('s'):
                self.save_level()
            elif key == ord('l'):
                self.load_level()
            elif key == ord('n'):
                self.new_level()
                
            # Exit
            elif key == ord('q'):
                self.running = False
                
            # Help
            elif key == ord('h'):
                self.show_help()
                
        except Exception as e:
            self.message = f"Error: {str(e)}"
            
    def save_level(self):
        """Save the current level to a file"""
        try:
            # Extract level data from grid
            platforms = []
            obstacles = []
            coins = []
            player_pos = (0, 0)
            
            # Find platform segments
            for y in range(self.level_height):
                platform_start = None
                for x in range(self.level_width):
                    char = self.grid[y][x]
                    
                    if char == '=':
                        if platform_start is None:
                            platform_start = x
                    elif platform_start is not None:
                        # End of a platform segment
                        platform_width = x - platform_start
                        platforms.append((platform_start, y, platform_width))
                        platform_start = None
                        
                    if char == 'o':
                        coins.append((x, y))
                    elif char == 'X':
                        obstacles.append((x, y))
                    elif char == 'P':
                        player_pos = (x, y)
                        
                # Handle platform at the end of a line
                if platform_start is not None:
                    platform_width = self.level_width - platform_start
                    platforms.append((platform_start, y, platform_width))
            
            # Prompt for filename
            self.stdscr.addstr(self.level_height + 5, 1, "Enter filename (without .txt): ", curses.color_pair(5))
            curses.echo()
            filename = self.stdscr.getstr(self.level_height + 5, 35, 20).decode('utf-8')
            curses.noecho()
            
            if not filename:
                self.message = "Save cancelled"
                return
                
            # Create full path
            os.makedirs('levels', exist_ok=True)
            path = os.path.join('levels', f"{filename}.txt")
            
            # Save the level
            self.loader.create_level_file(
                path,
                self.level_width,
                self.level_height,
                platforms,
                obstacles,
                coins,
                player_pos
            )
            
            self.current_file = path
            self.message = f"Level saved to {path}"
            
        except Exception as e:
            self.message = f"Error saving level: {str(e)}"
            
    def load_level(self):
        """Load a level from file"""
        try:
            level_files = self.loader.get_level_list()
            
            if not level_files:
                self.message = "No level files found"
                return
                
            # Display available levels
            menu_y = self.level_height + 5
            self.stdscr.addstr(menu_y, 1, "Select a level to load:", curses.color_pair(5))
            
            for i, file in enumerate(level_files):
                try:
                    self.stdscr.addstr(menu_y + i + 1, 1, f"{i+1}. {os.path.basename(file)}", curses.color_pair(5))
                except:
                    pass
            
            self.stdscr.addstr(menu_y + len(level_files) + 1, 1, "Enter number: ", curses.color_pair(5))
            curses.echo()
            choice = self.stdscr.getstr(menu_y + len(level_files) + 1, 15, 2).decode('utf-8')
            curses.noecho()
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(level_files):
                    selected_file = level_files[choice_idx]
                    
                    # Load the level data
                    platforms, obstacles, coins, player_pos, width, height = self.loader.load_level(selected_file)
                    
                    # Update level dimensions if necessary
                    if width != self.level_width or height != self.level_height:
                        self.level_width = min(width, self.width - 2)
                        self.level_height = min(height, self.height - 2)
                        self.grid = [[' ' for _ in range(self.level_width)] for _ in range(self.level_height)]
                    
                    # Clear the grid
                    for y in range(self.level_height):
                        for x in range(self.level_width):
                            self.grid[y][x] = ' '
                    
                    # Add platforms
                    for x, y, width in platforms:
                        for i in range(width):
                            if 0 <= x + i < self.level_width and 0 <= y < self.level_height:
                                self.grid[y][x + i] = '='
                    
                    # Add obstacles
                    for x, y in obstacles:
                        if 0 <= x < self.level_width and 0 <= y < self.level_height:
                            self.grid[y][x] = 'X'
                    
                    # Add coins
                    for x, y in coins:
                        if 0 <= x < self.level_width and 0 <= y < self.level_height:
                            self.grid[y][x] = 'o'
                    
                    # Add player
                    if player_pos is not None:
                        px, py = player_pos
                        if 0 <= px < self.level_width and 0 <= py < self.level_height:
                            self.grid[py][px] = 'P'
                    
                    self.current_file = selected_file
                    self.message = f"Loaded level from {selected_file}"
                    
                else:
                    self.message = "Invalid selection"
            except ValueError:
                self.message = "Invalid input, please enter a number"
                
        except Exception as e:
            self.message = f"Error loading level: {str(e)}"
            
    def new_level(self):
        """Create a new blank level"""
        try:
            self.stdscr.addstr(self.level_height + 5, 1, "Enter level width (10-80): ", curses.color_pair(5))
            curses.echo()
            width_str = self.stdscr.getstr(self.level_height + 5, 28, 3).decode('utf-8')
            
            self.stdscr.addstr(self.level_height + 6, 1, "Enter level height (10-40): ", curses.color_pair(5))
            height_str = self.stdscr.getstr(self.level_height + 6, 29, 3).decode('utf-8')
            curses.noecho()
            
            try:
                width = int(width_str)
                height = int(height_str)
                
                # Enforce reasonable limits
                width = max(10, min(80, width))
                height = max(10, min(40, height))
                
                # Create a new level with those dimensions
                self.level_width = min(width, self.width - 2)
                self.level_height = min(height, self.height - 2)
                self.grid = [[' ' for _ in range(self.level_width)] for _ in range(self.level_height)]
                
                # Add ground platform
                for x in range(self.level_width):
                    self.grid[self.level_height - 1][x] = '='
                    
                # Set player position
                self.grid[self.level_height - 2][1] = 'P'
                
                self.current_file = None
                self.message = f"Created new level with size {self.level_width}x{self.level_height}"
                
            except ValueError:
                self.message = "Invalid dimensions, using defaults"
                
        except Exception as e:
            self.message = f"Error creating new level: {str(e)}"
            
    def show_help(self):
        """Show help information"""
        help_text = [
            "Level Editor Controls:",
            "Arrow keys: Move cursor",
            "Enter: Place current tool at cursor position",
            "Tool Selection:",
            "  p: Player starting position",
            "  =: Platform",
            "  x: Obstacle",
            "  o: Coin",
            "  Space: Eraser (clear cell)",
            "File Operations:",
            "  s: Save level",
            "  l: Load level",
            "  n: New level",
            "Other:",
            "  h: Show this help",
            "  q: Quit editor",
            "",
            "Press any key to continue..."
        ]
        
        # Clear screen and show help
        self.stdscr.clear()
        for i, line in enumerate(help_text):
            try:
                self.stdscr.addstr(i + 1, 1, line, curses.color_pair(5))
            except:
                pass
                
        self.stdscr.refresh()
        self.stdscr.getch()  # Wait for a key press
        
    def run(self):
        """Run the level editor main loop"""
        while self.running:
            self.render()
            self.handle_input()
            time.sleep(0.05)  # To reduce CPU usage
            

def main(stdscr):
    """
    Main function to initialize and run the level editor
    
    Args:
        stdscr: Standard screen provided by curses
    """
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    editor = LevelEditor(stdscr)
    editor.run()
    

if __name__ == "__main__":
    curses.wrapper(main)