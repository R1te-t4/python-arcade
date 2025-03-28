"""
Utility functions for the game
"""
import os
import time

def clear_screen():
    """
    Clear the terminal screen
    Compatible with different operating systems
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def delay(seconds):
    """
    Pause execution for the specified number of seconds
    
    Args:
        seconds: Time to pause in seconds
    """
    time.sleep(seconds)

def get_terminal_size():
    """
    Get the current terminal size
    
    Returns:
        tuple: (width, height) of terminal in characters
    """
    try:
        columns, lines = os.get_terminal_size()
        return columns, lines
    except (AttributeError, OSError):
        # Fallback values if unable to determine terminal size
        return 80, 24

def calculate_fps(start_time, frame_count):
    """
    Calculate frames per second
    
    Args:
        start_time: Starting time in seconds
        frame_count: Number of frames processed
        
    Returns:
        float: Frames per second
    """
    elapsed_time = time.time() - start_time
    if elapsed_time == 0:
        return 0
    return frame_count / elapsed_time
