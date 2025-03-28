"""
Level Loader - Load level data from level files
"""
import os
import glob

class LevelLoader:
    """
    Load levels from text files
    """
    def __init__(self):
        """
        Initialize the level loader
        """
        self.levels_dir = "levels"
        # Ensure levels directory exists
        if not os.path.exists(self.levels_dir):
            os.makedirs(self.levels_dir)
    
    def get_level_list(self):
        """
        Get a list of available level files
        
        Returns:
            list: List of level file paths
        """
        # Search for level files in the levels directory
        level_files = glob.glob(os.path.join(self.levels_dir, "*.txt"))
        # Sort them to ensure consistent order
        level_files.sort()
        return level_files
    
    def load_level(self, level_path):
        """
        Load a level from a text file
        
        Args:
            level_path: Path to the level file
            
        Returns:
            tuple: (platforms, obstacles, coins, player_pos, level_width, level_height)
        """
        with open(level_path, 'r') as file:
            lines = file.readlines()
        
        # Parse level metadata from first lines
        header_lines = []
        level_data = []
        header_section = True
        
        for line in lines:
            line = line.rstrip()
            if header_section:
                if line.startswith('#'):
                    header_lines.append(line)
                else:
                    header_section = False
                    
            if not header_section and line:
                level_data.append(line)
        
        # Process header data to get dimensions
        level_width = max(len(line) for line in level_data) if level_data else 0
        level_height = len(level_data)
        
        # Parse level data and identify game elements
        platforms = []  # List of (x, y, width) tuples
        obstacles = []  # List of (x, y) tuples
        coins = []      # List of (x, y) tuples
        player_pos = None  # (x, y) tuple for player start position
        
        # Parse level layout
        for y, line in enumerate(level_data):
            platform_start = None
            for x, char in enumerate(line):
                if char == '=':  # Platform
                    if platform_start is None:
                        platform_start = x
                elif platform_start is not None:
                    # End of current platform
                    width = x - platform_start
                    if width > 0:
                        platforms.append((platform_start, y, width))
                    platform_start = None
                    
                if char == 'X':  # Obstacle
                    obstacles.append((x, y))
                elif char == 'o':  # Coin
                    coins.append((x, y))
                elif char == '@':  # Player start position
                    player_pos = (x, y)
            
            # Handle platform at the end of line
            if platform_start is not None:
                width = len(line) - platform_start
                if width > 0:
                    platforms.append((platform_start, y, width))
        
        return platforms, obstacles, coins, player_pos, level_width, level_height
    
    def create_level_file(self, path, width, height, platforms, obstacles, coins, player_pos):
        """
        Create a new level file
        
        Args:
            path: Path to save the level file
            width: Level width
            height: Level height
            platforms: List of (x, y, width) tuples
            obstacles: List of (x, y) tuples
            coins: List of (x, y) tuples
            player_pos: (x, y) tuple for player starting position
        """
        # Create a 2D grid of empty spaces
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Place platforms in the grid
        for x, y, w in platforms:
            for i in range(w):
                if 0 <= x + i < width and 0 <= y < height:
                    grid[y][x + i] = '='
        
        # Place obstacles
        for x, y in obstacles:
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = 'X'
        
        # Place coins
        for x, y in coins:
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = 'o'
        
        # Place player start position
        if player_pos:
            x, y = player_pos
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = '@'
        
        # Write the grid to the file
        with open(path, 'w') as file:
            # Add header with metadata
            file.write(f"# Level dimensions: {width}x{height}\n")
            file.write(f"# Legend: '@'=Player start, '='=Platform, 'o'=Coin, 'X'=Obstacle\n")
            file.write("\n")
            
            # Write the grid
            for row in grid:
                file.write(''.join(row) + '\n')
        
        print(f"Level saved to {path}")