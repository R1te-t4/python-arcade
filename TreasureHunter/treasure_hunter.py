#!/usr/bin/env python3
"""
Treasure Hunter - A console-based adventure game

Navigate through a randomly generated dungeon, find treasure,
avoid traps and monsters, and try to escape with the highest score!

Controls:
- W/A/S/D or arrow keys: Move
- Q: Quit the game
- H: Show help
"""

import os
import sys
import time
import random

# Pre-import game components to speed up startup
from game.game_engine import GameEngine

def clear_screen():
    """Clear the terminal screen based on operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_intro(fast_mode=False):
    """
    Display the game introduction and story.
    
    Args:
        fast_mode: If True, skip the delay between intro and game start
    """
    clear_screen()
    
    # Show ASCII logo
    print("\033[93m" + r"""
 _____                                    _   _             _            
|_   _|                                  | | | |           | |           
  | |_ __ ___  __ _ ___ _   _ _ __ ___  | |_| |_   _ _ __ | |_ ___ _ __ 
  | | '__/ _ \/ _` / __| | | | '__/ _ \ |  _  | | | | '_ \| __/ _ \ '__|
  | | | |  __/ (_| \__ \ |_| | | |  __/ | | | | |_| | | | | ||  __/ |   
  \_/_|  \___|\__,_|___/\__,_|_|  \___| \_| |_/\__,_|_| |_|\__\___|_|   
                                                                        
    """ + "\033[0m")
    
    # Show brief description and controls
    print("\033[96mYou are an adventurous explorer searching for the legendary lost treasure.")
    print("Explore the dungeon, collect treasure, and avoid dangers.")
    print("Find the treasure and make it to the exit alive to win!\033[0m")
    print("\n\033[93mControls:\033[0m")
    print("  - \033[97mW\033[0m: Move up")
    print("  - \033[97mA\033[0m: Move left")
    print("  - \033[97mS\033[0m: Move down")
    print("  - \033[97mD\033[0m: Move right")
    print("  - \033[97mH\033[0m: Show help")
    print("  - \033[97mQ\033[0m: Quit game")
    
    print("\n\033[93mSymbols:\033[0m")
    print("  - \033[97m@\033[0m: Player (you)")
    print("  - \033[92m$\033[0m: Treasure")
    print("  - \033[91mT\033[0m: Trap")
    print("  - \033[91mM\033[0m: Monster")
    print("  - \033[94mE\033[0m: Exit")
    print("  - \033[90m#\033[0m: Wall")
    print("  - \033[90m.\033[0m: Empty space")
    
    print("\n\033[93mStarting your adventure...\033[0m")
    # Use a shorter delay in fast mode
    if not fast_mode:
        time.sleep(1)

def handle_error(error):
    """Handle game errors gracefully."""
    clear_screen()
    print("\n\033[91mOops! Something went wrong.\033[0m")
    print(f"Error: {error}")
    print("\nTrying to restart the game...")
    time.sleep(2)
    return main(retry=True)

def main(retry=False):
    """
    Main game function with improved error handling.
    
    Args:
        retry: If True, skip the intro animation for faster restart
    """
    try:
        # Skip intro on retry for faster restart
        if not retry:
            display_intro()
        else:
            print("\033[93mRestarting game...\033[0m")
            time.sleep(1)
            clear_screen()
        
        # Create and start the game with optimized settings
        game = GameEngine()
        game.start_game()
        
    except KeyboardInterrupt:
        clear_screen()
        print("\n\033[93mGame terminated. Thanks for playing!\033[0m")
        sys.exit(0)
    except Exception as e:
        if retry:
            # If already retrying, just show the error and exit
            print(f"\n\033[91mUnable to start game: {e}\033[0m")
            sys.exit(1)
        else:
            # Try to recover from errors
            return handle_error(e)

if __name__ == "__main__":
    # Set the random seed for more consistent generation
    random.seed(time.time())
    main()
