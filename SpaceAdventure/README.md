# Space Adventure Game

A console-based space-flying game with ASCII graphics, obstacle avoidance, and score tracking.

## Description

Space Adventure is a terminal-based game where you pilot a spaceship (represented by "D") through a field of space debris while collecting valuable items. The game features:

- Colorful ASCII graphics for a retro gaming experience
- Three difficulty levels (Easy, Medium, Hard)
- Animated start menu and game over screen with twinkling stars
- Changing difficulty as you play through levels
- Score tracking based on obstacles passed and items collected

## How to Play

1. Navigate your spaceship using the following controls:
   - `W` key: Move up
   - `S` key: Move down
   - `Q` key: Quit the game

2. Avoid red obstacles (represented by `#`, `^`, `%`, `@`) as they move across the screen.

3. Collect yellow items to increase your score:
   - `$` = 5 points
   - `&` = 15 points
   - `O` = 30 points

## Requirements

- Python 3.6 or higher
- Terminal/console with support for:
  - ANSI colors
  - Arrow keys (or W/S keys)
  - Minimum terminal size of 80x24 characters (larger recommended)
- Python `curses` library (included in standard Python distribution on Linux/OSX)

## How to Download

You can get the game files in one of these ways:

### Option 1: Clone the repository

If you have Git installed, you can clone the repository:

```bash
git clone https://github.com/R1te-t4/python-arcade/
cd python-arcade/SpaceAdventure
```

### Option 2: Download ZIP file

1. Download the ZIP file containing all game files
2. Extract the ZIP file to a folder on your computer
3. Navigate to that folder in your terminal

## How to Run

### On Linux/macOS

1. Open a terminal window
2. Navigate to the directory containing the game files
3. Make sure the terminal window is sized appropriately (at least 80x24 characters)
4. Run the game with:

```bash
python3 running_game.py
```

### On Windows

Windows requires additional setup because `curses` is not included by default:

1. Download the game files to your computer
2. Install the `windows-curses` package:

```bash
pip install windows-curses
```

3. Open a command prompt or PowerShell window
4. Navigate to the directory containing the game files
5. Make sure the console window is sized appropriately (at least 80x24 characters)
6. Run the game with:

```bash
python running_game.py
```

### Navigation

When the game starts, use the arrow keys or W/S to navigate the menu and select your difficulty level by pressing Enter.

### Terminal Size Issues

If you encounter errors related to terminal size:
- Try maximizing your terminal window
- Decrease the font size to fit more characters 
- Some terminal emulators allow you to adjust the number of columns and rows in their settings

## Difficulty Levels

1. **Easy**: Beginner friendly with fewer obstacles
2. **Medium**: Balanced challenge with moderate obstacles
3. **Hard**: Intense challenge with many obstacles
