"""
Entities module for the Treasure Hunter game.
Handles game entities like monsters, traps, and items.
"""

class Entity:
    """Base class for all entities in the game."""
    
    def __init__(self, x, y, symbol, name, description):
        """Initialize an entity with position and basic information."""
        self.x = x
        self.y = y
        self.symbol = symbol
        self.name = name
        self.description = description
    
    def interact(self, player):
        """Base interact method, to be overridden by subclasses."""
        pass

class Trap(Entity):
    """A trap that damages the player when stepped on."""
    
    def __init__(self, x, y, damage=1):
        """Initialize a trap with a position and damage amount."""
        super().__init__(x, y, 'T', 'Trap', 'A dangerous trap')
        self.damage = damage
        self.triggered = False
    
    def interact(self, player):
        """Interact with the player, dealing damage if not already triggered."""
        message = ""
        if not self.triggered:
            player.take_damage(self.damage)
            self.triggered = True
            message = f"You triggered a trap and took {self.damage} damage!"
        else:
            message = "This trap has already been triggered."
        return message

class Monster(Entity):
    """A monster that attacks the player when encountered."""
    
    def __init__(self, x, y, damage=1):
        """Initialize a monster with a position and damage amount."""
        super().__init__(x, y, 'M', 'Monster', 'A dangerous monster')
        self.damage = damage
    
    def interact(self, player):
        """Interact with the player, dealing damage."""
        player.take_damage(self.damage)
        return f"The monster attacks you for {self.damage} damage!"

class Treasure(Entity):
    """The main treasure that the player needs to find to win."""
    
    def __init__(self, x, y):
        """Initialize the treasure with a position."""
        super().__init__(x, y, '$', 'Treasure', 'The legendary treasure')
    
    def interact(self, player):
        """Interact with the player, giving them the treasure."""
        player.has_treasure = True
        return "You found the treasure! Now find the exit to win!"

class Exit(Entity):
    """The exit that the player needs to reach with the treasure to win."""
    
    def __init__(self, x, y):
        """Initialize the exit with a position."""
        super().__init__(x, y, 'E', 'Exit', 'The exit from the dungeon')
    
    def interact(self, player):
        """Interact with the player, checking if they have the treasure."""
        if player.has_treasure:
            return "You've escaped with the treasure! You win!"
        else:
            return "You need to find the treasure before you can leave."
