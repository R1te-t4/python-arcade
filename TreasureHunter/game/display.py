"""
Display module for the Treasure Hunter game.
Handles terminal output formatting and rendering.
"""

import os
import sys
import time

# ANSI color codes
COLORS = {
    'reset': '\033[0m',
    'black': '\033[30m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'gray': '\033[90m',
    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m',
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color='white'):
    """Print text with the specified color."""
    print(f"{COLORS.get(color, COLORS['white'])}{text}{COLORS['reset']}")

def format_colored(text, color='white'):
    """Format text with the specified color."""
    return f"{COLORS.get(color, COLORS['white'])}{text}{COLORS['reset']}"

def slow_print(text, delay=0.03):
    """Print text character by character with a delay."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def render_dungeon(dungeon, player, revealed_cells, score, health, turns):
    """Render the dungeon map with player, enemies, and items."""
    clear_screen()
    
    # Header
    print_colored("=" * 60, 'yellow')
    print_colored(" TREASURE HUNTER ", 'yellow')
    print_colored("=" * 60, 'yellow')
    print(f"Score: {format_colored(str(score), 'green')}  |  "
          f"Health: {format_colored('♥' * health, 'red')}  |  "
          f"Turns: {format_colored(str(turns), 'cyan')}")
    print_colored("-" * 60, 'yellow')
    
    # Render the dungeon
    for y in range(len(dungeon)):
        line = ""
        for x in range(len(dungeon[0])):
            # Check if this is the player's position
            if player.x == x and player.y == y:
                line += format_colored('@', 'white')
            # Check if the cell is revealed or within view distance
            elif (x, y) in revealed_cells:
                cell = dungeon[y][x]
                if cell == '#':  # Wall
                    line += format_colored('#', 'gray')
                elif cell == '.':  # Empty
                    line += format_colored('.', 'gray')
                elif cell == 'T':  # Trap
                    line += format_colored('T', 'red')
                elif cell == 'M':  # Monster
                    line += format_colored('M', 'red')
                elif cell == '$':  # Treasure
                    line += format_colored('$', 'green')
                elif cell == 'E':  # Exit
                    line += format_colored('E', 'blue')
                else:
                    line += ' '
            else:
                # Fog of war - unexplored area
                line += ' '
        print(line)
    
    print_colored("-" * 60, 'yellow')
    print("Controls: W/↑=Up, A/←=Left, S/↓=Down, D/→=Right, H=Help, Q=Quit")

def show_help():
    """Display the help screen."""
    clear_screen()
    print_colored("TREASURE HUNTER - HELP", 'yellow')
    print_colored("=" * 60, 'yellow')
    print("\nGoal: Find the treasure and reach the exit without dying.")
    print("\nControls:")
    print("  - W or ↑: Move up")
    print("  - A or ←: Move left")
    print("  - S or ↓: Move down")
    print("  - D or →: Move right")
    print("  - H: Show this help screen")
    print("  - Q: Quit game")
    
    print("\nSymbols:")
    print(f"  - {format_colored('@', 'white')}: Player (you)")
    print(f"  - {format_colored('$', 'green')}: Treasure")
    print(f"  - {format_colored('T', 'red')}: Trap (reduces health)")
    print(f"  - {format_colored('M', 'red')}: Monster (reduces health)")
    print(f"  - {format_colored('E', 'blue')}: Exit (escape with treasure to win)")
    print(f"  - {format_colored('#', 'gray')}: Wall (can't walk through)")
    print(f"  - {format_colored('.', 'gray')}: Empty space")
    
    print("\nTips:")
    print("- You have limited health, so avoid traps and monsters when possible.")
    print("- You need to find the treasure before you can exit.")
    print("- The more efficient your route, the higher your score.")
    
    print_colored("\nReturning to game in 3 seconds...", 'yellow')
    # Replace input with a timed delay
    time.sleep(3)

def game_over(win, score, turns):
    """Display the game over screen."""
    clear_screen()
    
    if win:
        # ASCII art for win
        victory_art = r"""
        __   __  _______  __   __    _     _  ___   __    _  __   __
        |  | |  ||       ||  | |  |  | | _ | ||   | |  |  | ||  | |  |
        |  |_|  ||   _   ||  | |  |  | || || ||   | |   |_| ||  |_|  |
        |       ||  | |  ||  |_|  |  |       ||   | |       ||       |
        |_     _||  |_|  ||       |  |       ||   | |  _    ||       |
          |   |  |       ||       |  |   _   ||   | | | |   ||   _   |
          |___|  |_______||_______|  |__| |__||___| |_|  |__||__| |__|
        """
        print_colored(victory_art, 'green')
        print_colored(f"\nCongratulations! You escaped with the treasure!", 'green')
    else:
        # ASCII art for loss
        game_over_art = r"""
         _______  _______  __   __  _______    _______  __   __  _______  ______   
        |       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  
        |    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  
        |   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ 
        |   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |
        |   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |
        |_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|
        """
        print_colored(game_over_art, 'red')
        print_colored(f"\nYou failed in your quest!", 'red')
    
    print_colored(f"\nFinal Score: {score}", 'yellow')
    print_colored(f"Turns Taken: {turns}", 'yellow')
    
    print_colored("\nGame will restart in 5 seconds...", 'cyan')
    time.sleep(5)  # Give time to read the game over screen
    
    # Automatically restart the game
    from game.game_engine import GameEngine
    game = GameEngine()
    game.start_game()

def display_event_message(message, color='white'):
    """Display an event message at the bottom of the screen."""
    print_colored(message, color)
    time.sleep(1.5)  # Show the message for a short time
