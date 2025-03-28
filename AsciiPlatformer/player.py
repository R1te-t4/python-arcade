"""
Player class - Handle player movement and physics
"""

class Player:
    """
    Player class with movement and physics
    """
    def __init__(self, x, y):
        """
        Initialize player position and physics attributes
        
        Args:
            x: Initial x position
            y: Initial y position
        """
        # Position
        self.x = x
        self.y = y
        
        # Velocity
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Physics constants
        self.gravity = 0.5
        self.jump_strength = -2.0
        self.move_speed = 1.0
        self.max_velocity_x = 2.0
        self.max_velocity_y = 5.0
        
        # State
        self.on_ground = False
        self.jumping = False

    def move_left(self):
        """Move player left"""
        self.velocity_x = max(self.velocity_x - self.move_speed, -self.max_velocity_x)

    def move_right(self):
        """Move player right"""
        self.velocity_x = min(self.velocity_x + self.move_speed, self.max_velocity_x)

    def jump(self):
        """Make the player jump if on ground"""
        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.jumping = True

    def apply_gravity(self):
        """Apply gravity to player's vertical velocity"""
        self.velocity_y += self.gravity
        # Limit max fall speed
        if self.velocity_y > self.max_velocity_y:
            self.velocity_y = self.max_velocity_y

    def check_platform_collision(self, platforms):
        """
        Check and handle collision with platforms
        
        Args:
            platforms: List of platform tuples (x, y, width)
            
        Returns:
            bool: True if player is on a platform, False otherwise
        """
        # Previous y position (before applying gravity)
        prev_y = self.y - self.velocity_y
        
        # Reset on_ground status
        self.on_ground = False
        
        for platform in platforms:
            platform_x, platform_y, platform_width = platform
            
            # Check if player is within the x-range of the platform
            if platform_x <= self.x < platform_x + platform_width:
                # Check if player is landing on the platform (was above, now at or below)
                if prev_y <= platform_y and self.y >= platform_y:
                    self.y = platform_y  # Place player on top of platform
                    self.velocity_y = 0  # Stop vertical movement
                    self.on_ground = True
                    return True
                
                # Check for hitting platform from below
                elif prev_y >= platform_y + 1 and self.y <= platform_y + 1:
                    self.y = platform_y + 1  # Push player down
                    self.velocity_y = 0.5  # Bounce slightly
        
        return False

    def update(self, level):
        """
        Update player position based on velocity and check collisions
        
        Args:
            level: Level object containing platforms
        """
        # Apply gravity
        self.apply_gravity()
        
        # Update position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Check collision with platforms
        self.check_platform_collision(level.platforms)
        
        # Apply friction when on ground
        if self.on_ground:
            self.velocity_x *= 0.8  # Friction
            if abs(self.velocity_x) < 0.1:
                self.velocity_x = 0
            self.jumping = False
        
        # Implement screen boundaries
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        elif self.x >= level.width:
            self.x = level.width - 1
            self.velocity_x = 0
