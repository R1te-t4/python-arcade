"""
Level class - Handle level loading and management
"""
import os
from level_loader import LevelLoader


class Level:
    """
    Level management
    """
    def __init__(self, width, height):
        """
        Initialize level with screen dimensions
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.width = max(10, width)
        self.height = max(10, height)
        self.platforms = []  # List of (x, y, width) tuples
        self.obstacles = []  # List of (x, y) tuples
        self.coins = []      # List of (x, y) tuples
        self.player_pos = None  # Default player position (x, y)
        self.loader = LevelLoader()
        self.level_files = self.loader.get_level_list()
        self.current_level_idx = 0
        
    def generate_level(self, level_num):
        """
        Load a level from file or generate a simple default level if no files exist
        
        Args:
            level_num: Level number (used to select from available level files)
        """
        self.platforms = []
        self.obstacles = []
        self.coins = []
        
        # Check if we have level files
        if self.level_files:
            # Determine which level file to load
            idx = (level_num - 1) % len(self.level_files)
            self.current_level_idx = idx
            
            print(f"Loading level {level_num} from file: {self.level_files[idx]}")
            print(f"Available level files: {len(self.level_files)}")
            
            try:
                # Load the level data
                platforms, obstacles, coins, player_pos, level_width, level_height = self.loader.load_level(self.level_files[idx])
                
                # Log level information for debugging
                print(f"Level loaded - Platforms: {len(platforms)}, Obstacles: {len(obstacles)}, Coins: {len(coins)}")
                print(f"Level dimensions: {level_width}x{level_height}, Player position: {player_pos}")
                
                # Store the level data
                self.platforms = platforms
                self.obstacles = obstacles
                self.coins = coins
                self.player_pos = player_pos
                
                # Scale the level elements if necessary for screen size
                if level_width > self.width or level_height > self.height:
                    self._scale_level_elements(level_width, level_height)
                    
                return
            except Exception as e:
                print(f"Error loading level: {str(e)}")
                # Fall back to default level if loading fails
        
        # If no level files or loading failed, create a simple default level
        self._create_default_level()
        
    def _create_default_level(self):
        """Create a simple default level when no level files are available"""
        # Clear existing elements
        self.platforms = []
        self.obstacles = []
        self.coins = []
        
        # Add ground platform
        ground_y = max(3, self.height - 5)
        self.platforms.append((0, ground_y, self.width))
        
        # Add a few platforms
        if self.height > 10 and self.width > 15:
            platform_y1 = ground_y - 4
            platform_y2 = ground_y - 8
            
            # Platform 1
            platform_width1 = min(10, self.width // 3)
            platform_x1 = self.width // 4
            self.platforms.append((platform_x1, platform_y1, platform_width1))
            
            # Platform 2
            platform_width2 = min(8, self.width // 4)
            platform_x2 = (self.width // 2) + 2
            self.platforms.append((platform_x2, platform_y2, platform_width2))
            
            # Add coins
            self.coins.append((platform_x1 + 1, platform_y1 - 1))
            self.coins.append((platform_x1 + platform_width1 - 1, platform_y1 - 1))
            self.coins.append((platform_x2 + 1, platform_y2 - 1))
            self.coins.append((platform_x2 + platform_width2 - 1, platform_y2 - 1))
            
            # Add obstacle
            self.obstacles.append((platform_x2 + platform_width2 // 2, platform_y2 - 1))
            
        # Add a few coins on the ground
        for i in range(3):
            coin_x = 5 + (i * 5)
            if coin_x < self.width - 1:
                self.coins.append((coin_x, ground_y - 1))
                
    def _scale_level_elements(self, original_width, original_height):
        """
        Scale level elements to fit current screen size
        
        Args:
            original_width: Original level width
            original_height: Original level height
        """
        width_ratio = self.width / original_width
        height_ratio = self.height / original_height
        
        # Scale platforms
        scaled_platforms = []
        for x, y, width in self.platforms:
            new_x = int(x * width_ratio)
            new_y = int(y * height_ratio)
            new_width = max(1, int(width * width_ratio))
            scaled_platforms.append((new_x, new_y, new_width))
        self.platforms = scaled_platforms
        
        # Scale obstacles
        scaled_obstacles = []
        for x, y in self.obstacles:
            new_x = int(x * width_ratio)
            new_y = int(y * height_ratio)
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                scaled_obstacles.append((new_x, new_y))
        self.obstacles = scaled_obstacles
        
        # Scale coins
        scaled_coins = []
        for x, y in self.coins:
            new_x = int(x * width_ratio)
            new_y = int(y * height_ratio)
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                scaled_coins.append((new_x, new_y))
        self.coins = scaled_coins
        
    def regenerate(self, new_width, new_height, level_num):
        """
        Regenerate the level with new dimensions
        
        Args:
            new_width: New screen width
            new_height: New screen height
            level_num: Current level number
        """
        self.width = new_width
        self.height = new_height
        self.generate_level(level_num)