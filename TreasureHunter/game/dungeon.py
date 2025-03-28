"""
Dungeon generation module for the Treasure Hunter game.
Creates random dungeon layouts with rooms, corridors, and entities.
"""

import random
import time

class DungeonGenerator:
    """
    Generates a random dungeon layout for the Treasure Hunter game.
    Creates rooms, corridors, and places entities like treasure, traps, and monsters.
    """
    
    def __init__(self, width=30, height=15, complexity=0.75, density=0.45):
        """
        Initialize the dungeon generator with size and generation parameters.
        
        Args:
            width: Width of the dungeon
            height: Height of the dungeon
            complexity: Controls the number of tunnels
            density: Controls the size and spread of rooms
        """
        # Optimize size for faster generation
        self.width = width
        self.height = height
        self.complexity = complexity
        self.density = density
        
        # Create a dungeon filled with walls initially
        self.dungeon = [['#' for _ in range(width)] for _ in range(height)]
        
        # Track positions of key elements
        self.player_start = None
        self.exit_pos = None
        self.treasure_pos = None
        
        # Track empty spaces for faster entity placement
        self.empty_spaces = []
    
    def generate(self):
        """
        Generate a random dungeon layout with optimized performance.
        
        Returns:
            tuple: (dungeon grid, player start position)
        """
        # Generate the basic maze structure (optimized)
        self._generate_maze()
        
        # Collect all empty spaces for faster placement
        self._collect_empty_spaces()
        
        # Place the entrance (player start)
        self._place_entrance()
        
        # Place the exit
        self._place_exit()
        
        # Place treasure
        self._place_treasure()
        
        # Place traps and monsters with fixed counts for reliability
        self._place_traps(max(3, int(len(self.empty_spaces) * 0.05)))  # 5% of empty cells are traps
        self._place_monsters(max(2, int(len(self.empty_spaces) * 0.03)))  # 3% of empty cells are monsters
        
        return self.dungeon, self.player_start
    
    def _generate_maze(self):
        """Generate a maze-like dungeon using a faster algorithm."""
        # Create a simpler room-based layout for faster generation
        # Create some random rooms
        room_count = int((self.width * self.height) * 0.01)  # 1% of cells become room centers
        
        for _ in range(room_count):
            room_x = random.randint(2, self.width - 3)
            room_y = random.randint(2, self.height - 3)
            room_size = random.randint(3, 5)
            
            # Carve out the room
            for y in range(max(1, room_y - room_size // 2), min(self.height - 1, room_y + room_size // 2)):
                for x in range(max(1, room_x - room_size // 2), min(self.width - 1, room_x + room_size // 2)):
                    self.dungeon[y][x] = '.'
        
        # Add some random corridors to connect rooms
        for _ in range(self.width + self.height):
            x1 = random.randint(1, self.width - 2)
            y1 = random.randint(1, self.height - 2)
            
            # Pick a random direction and length
            direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            length = random.randint(3, 8)
            
            # Create the corridor
            for i in range(length):
                x = x1 + direction[0] * i
                y = y1 + direction[1] * i
                
                if 1 <= x < self.width - 1 and 1 <= y < self.height - 1:
                    self.dungeon[y][x] = '.'
        
        # Ensure the dungeon is surrounded by walls
        for x in range(self.width):
            self.dungeon[0][x] = '#'
            self.dungeon[self.height - 1][x] = '#'
        
        for y in range(self.height):
            self.dungeon[y][0] = '#'
            self.dungeon[y][self.width - 1] = '#'
    
    def _collect_empty_spaces(self):
        """Collect all empty spaces for faster entity placement."""
        self.empty_spaces = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.dungeon[y][x] == '.':
                    self.empty_spaces.append((x, y))
        
        # Shuffle the list for random access
        random.shuffle(self.empty_spaces)
    
    def _place_entrance(self):
        """Place the player start position in the dungeon."""
        if not self.empty_spaces:
            # Fallback - find any open space
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if self.dungeon[y][x] == '.':
                        self.player_start = (x, y)
                        # Clear area around player start
                        self._clear_area_around(x, y, 1)
                        return
            
            # If still no open space, force create one
            x, y = self.width // 4, self.height // 2
            self.dungeon[y][x] = '.'
            self.player_start = (x, y)
            self._clear_area_around(x, y, 1)
            return
            
        # Use first space from the shuffled list
        x, y = self.empty_spaces.pop(0)
        self.player_start = (x, y)
        
        # Ensure there's some open space around the player
        self._clear_area_around(x, y, 1)
    
    def _clear_area_around(self, x, y, radius):
        """Clear walls around a point to create open space."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                ny, nx = y + dy, x + dx
                if (0 < ny < self.height - 1 and 0 < nx < self.width - 1):
                    if self.dungeon[ny][nx] == '#':
                        self.dungeon[ny][nx] = '.'
                        # Add to empty spaces if not already used
                        if (nx, ny) not in self.empty_spaces and (nx, ny) != self.player_start:
                            self.empty_spaces.append((nx, ny))
    
    def _place_exit(self):
        """Place the exit in the dungeon, far from the entrance."""
        # The exit should be some distance from the start
        min_distance = max(5, (self.width + self.height) // 5)
        
        # Try from existing empty spaces
        for i, (x, y) in enumerate(self.empty_spaces):
            # Calculate Manhattan distance from start
            distance = abs(x - self.player_start[0]) + abs(y - self.player_start[1])
            
            if distance >= min_distance:
                self.dungeon[y][x] = 'E'
                self.exit_pos = (x, y)
                # Remove from empty spaces
                self.empty_spaces.pop(i)
                return
        
        # If no suitable position found, force placement
        farthest_x, farthest_y = self.width - self.player_start[0] - 2, self.height - self.player_start[1] - 2
        self.dungeon[farthest_y][farthest_x] = 'E'
        self.exit_pos = (farthest_x, farthest_y)
        
        # Clear area around exit to ensure it's accessible
        self._clear_area_around(farthest_x, farthest_y, 1)
    
    def _place_treasure(self):
        """Place the treasure in the dungeon, ideally between start and exit."""
        if not self.exit_pos:
            # Can't place treasure without an exit
            return
            
        # Try to place between start and exit
        if self.empty_spaces:
            best_pos = None
            best_score = float('inf')
            
            # Check up to 10 random positions to find a good spot
            for _ in range(min(10, len(self.empty_spaces))):
                pos_index = random.randint(0, len(self.empty_spaces) - 1)
                x, y = self.empty_spaces[pos_index]
                
                # Calculate distances
                distance_to_start = abs(x - self.player_start[0]) + abs(y - self.player_start[1])
                distance_to_exit = abs(x - self.exit_pos[0]) + abs(y - self.exit_pos[1])
                
                # Lower score means better positioned (not too close to start, but on path to exit)
                score = abs(distance_to_start - 3) + abs(distance_to_exit - distance_to_start)
                
                if score < best_score:
                    best_score = score
                    best_pos = (pos_index, x, y)
            
            if best_pos:
                pos_index, x, y = best_pos
                self.dungeon[y][x] = '$'
                self.treasure_pos = (x, y)
                self.empty_spaces.pop(pos_index)
                return
        
        # Fallback - place somewhere between start and exit
        mid_x = (self.player_start[0] + self.exit_pos[0]) // 2
        mid_y = (self.player_start[1] + self.exit_pos[1]) // 2
        
        if self.dungeon[mid_y][mid_x] == '.':
            self.dungeon[mid_y][mid_x] = '$'
            self.treasure_pos = (mid_x, mid_y)
        else:
            # Find nearest empty space
            for d in range(1, max(self.width, self.height)):
                for dy in range(-d, d+1):
                    for dx in range(-d, d+1):
                        if abs(dx) + abs(dy) == d:  # Check only perimeter at distance d
                            nx, ny = mid_x + dx, mid_y + dy
                            if (0 < nx < self.width - 1 and 0 < ny < self.height - 1 and 
                                self.dungeon[ny][nx] == '.'):
                                self.dungeon[ny][nx] = '$'
                                self.treasure_pos = (nx, ny)
                                return
    
    def _place_traps(self, count):
        """Place traps randomly in the dungeon with improved reliability."""
        count = min(count, len(self.empty_spaces))
        
        for _ in range(count):
            if not self.empty_spaces:
                break
                
            # Get a random empty position
            pos_index = random.randint(0, len(self.empty_spaces) - 1)
            x, y = self.empty_spaces[pos_index]
            
            # Don't place traps too close to the start point
            if abs(x - self.player_start[0]) + abs(y - self.player_start[1]) > 3:
                self.dungeon[y][x] = 'T'
                self.empty_spaces.pop(pos_index)
    
    def _place_monsters(self, count):
        """Place monsters randomly in the dungeon with improved reliability."""
        count = min(count, len(self.empty_spaces))
        
        for _ in range(count):
            if not self.empty_spaces:
                break
                
            # Get a random empty position
            pos_index = random.randint(0, len(self.empty_spaces) - 1)
            x, y = self.empty_spaces[pos_index]
            
            # Don't place monsters too close to the start point
            if abs(x - self.player_start[0]) + abs(y - self.player_start[1]) > 4:
                self.dungeon[y][x] = 'M'
                self.empty_spaces.pop(pos_index)
