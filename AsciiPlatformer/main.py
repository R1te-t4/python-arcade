#!/usr/bin/env python3
"""
Terminal ASCII Platformer - Main Entry Point
Start the game from this file
"""
import curses
from game import Game

def main(stdscr):
    """
    Main function to initialize and run the game
    Args:
        stdscr: Standard screen provided by curses
    """
    # Set up the screen
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    curses.start_color()  # Enable color support if available
    curses.use_default_colors()  # Use terminal's default colors
    
    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_GREEN, -1)    # Player
    curses.init_pair(2, curses.COLOR_WHITE, -1)    # Platforms
    curses.init_pair(3, curses.COLOR_RED, -1)      # Obstacles
    curses.init_pair(4, curses.COLOR_YELLOW, -1)   # Coins/points
    
    # Initialize game
    game = Game(stdscr)
    
    # Run the game
    game.run()

if __name__ == "__main__":
    try:
        # Initialize curses and pass control to main function
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Handle CTRL+C gracefully
        pass
    finally:
        print("Thanks for playing!")
