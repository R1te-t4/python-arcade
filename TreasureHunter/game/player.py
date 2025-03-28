"""
Player module for the Treasure Hunter game.
Handles player state, movement, and actions.
"""

import random

class Player:
    """
    Represents the player character in the Treasure Hunter game.
    Tracks position, health, inventory, and handles movement.
    """
    
    def __init__(self, x, y, max_health=3):
        """Initialize the player with starting position and health."""
        self.x = x
        self.y = y
        self.max_health = max_health
        self.health = max_health
        self.has_treasure = False
        self.view_distance = 3  # Increased view distance for better gameplay
        self.score = 0  # Track score directly on player
        
        # For gameplay variety
        self.trap_messages = [
            "Ouch! You stepped on a trap and lost 1 health!",
            "A spike trap activates beneath you! You lose 1 health!",
            "You triggered a hidden trap! -1 health!",
            "The floor gives way slightly as you step on a pressure plate. A dart hits you! -1 health!"
        ]
        
        self.monster_messages = [
            "A monster attacks you! You lost 1 health!",
            "A dungeon creature lunges at you! -1 health!",
            "A shadowy figure strikes from the darkness! You lose 1 health!",
            "A guardian of the dungeon blocks your path and attacks! -1 health!"
        ]
    
    def move(self, dx, dy, dungeon):
        """
        Attempt to move the player in the specified direction with improved error handling.
        
        Args:
            dx: Change in x coordinate (-1, 0, or 1)
            dy: Change in y coordinate (-1, 0, or 1)
            dungeon: The dungeon grid
            
        Returns:
            tuple: (moved successfully, cell content, message)
        """
        # Safety check for dungeon integrity
        if not dungeon or not isinstance(dungeon, list) or len(dungeon) == 0:
            return False, None, "The dungeon seems unstable. Try again."
            
        try:
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Check boundaries
            if (new_x < 0 or new_x >= len(dungeon[0]) or 
                new_y < 0 or new_y >= len(dungeon)):
                return False, None, "You can't move outside the dungeon!"
            
            # Check if the destination is a wall
            if dungeon[new_y][new_x] == '#':
                return False, None, "You bump into a solid wall."
            
            # Store the content of the cell we're moving to
            cell_content = dungeon[new_y][new_x]
            
            # Update position
            self.x = new_x
            self.y = new_y
            
            # Generate appropriate message based on cell content
            message = ""
            if cell_content == '.':
                # Occasionally find small bonuses in empty spaces
                if random.random() < 0.05:  # 5% chance
                    self.score += 5
                    message = "You found a small cache of valuables! (+5 points)"
                else:
                    message = "You move into an empty space."
            elif cell_content == 'T':
                self.take_damage(1)
                message = random.choice(self.trap_messages)
                # Disarm the trap after triggering it
                dungeon[new_y][new_x] = '.'
            elif cell_content == 'M':
                # 10% chance to dodge monster attack
                if random.random() < 0.1:
                    message = "You narrowly avoid the monster's attack!"
                else:
                    self.take_damage(1)
                    message = random.choice(self.monster_messages)
                # Monster moves away after attacking
                dungeon[new_y][new_x] = '.'
            elif cell_content == '$':
                self.has_treasure = True
                self.score += 50
                message = "You found the treasure! Now find the exit! (+50 points)"
                # Clear the treasure from the map
                dungeon[new_y][new_x] = '.'
            elif cell_content == 'E':
                if self.has_treasure:
                    message = "You reached the exit with the treasure! Victory!"
                else:
                    message = "This is the exit, but you need to find the treasure first!"
            
            return True, cell_content, message
            
        except Exception as e:
            # Fallback for any unexpected errors during movement
            print(f"Movement error: {e}")
            return False, None, "Something strange happens as you try to move."
    
    def take_damage(self, amount):
        """Reduce player health by the specified amount."""
        self.health = max(0, self.health - amount)
        
    def heal(self, amount):
        """Increase player health by the specified amount, up to max_health."""
        self.health = min(self.max_health, self.health + amount)
    
    def is_alive(self):
        """Check if the player is still alive."""
        return self.health > 0
    
    def get_visible_cells(self, dungeon):
        """
        Calculate which cells are visible to the player with improved error handling.
        
        Args:
            dungeon: The dungeon grid
            
        Returns:
            set: Coordinates of cells visible to the player
        """
        visible = set()
        
        # Safety check
        if not dungeon or not isinstance(dungeon, list) or len(dungeon) == 0:
            return visible
            
        try:
            # Get dungeon dimensions
            height = len(dungeon)
            width = len(dungeon[0]) if height > 0 else 0
            
            # Calculate visible area
            for y in range(max(0, self.y - self.view_distance), 
                           min(height, self.y + self.view_distance + 1)):
                for x in range(max(0, self.x - self.view_distance), 
                              min(width, self.x + self.view_distance + 1)):
                    # Simple distance check for visibility (using Manhattan distance for speed)
                    if abs(x - self.x) + abs(y - self.y) <= self.view_distance:
                        visible.add((x, y))
            
        except Exception as e:
            # If anything goes wrong, at least show the immediate area
            print(f"Visibility calculation error: {e}")
            # Fallback to just showing immediate surroundings
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= ny < len(dungeon) and 0 <= nx < len(dungeon[0]):
                        visible.add((nx, ny))
        
        return visible
