# ASCII Platformer

A terminal-based ASCII platformer game built with Python using the curses library for input handling and terminal rendering.

## Features

- ASCII-based graphics for game elements (player, platforms, obstacles, coins)
- Player movement: left, right, and jump
- Physics with gravity and collision detection
- File-based level system with predefined level designs
- Multiple levels with different layouts and challenges
- Scoring system based on coin collection
- Built-in level editor for creating custom levels

### Prerequisites

- Python 3.x
- Terminal that supports curses (most Unix terminals, Windows Terminal with WSL)

### Starting the Game

Run the game from your terminal:

```bash
python main.py
```

### Controls

- Arrow keys or WASD for movement:
  - Left/Right or A/D: Move left/right
  - Up/W/Space: Jump
- Q: Quit the game
- R: Restart (after game over or winning)

## Level System

The game uses a file-based level system instead of randomly generated levels. This provides several benefits:
- Consistent gameplay experience
- Carefully designed levels with appropriate difficulty progression
- Better control over platform placement, coin collection, and obstacle avoidance challenges

### Level Files

Level files are stored in the `levels/` directory with the `.txt` extension. The game automatically loads these files in alphabetical order.

Level files use a simple text-based format:
- '@' represents the player's starting position
- '=' represents platforms
- 'o' represents coins to collect
- 'X' represents obstacles to avoid

### Level Editor

You can create your own custom levels using the built-in level editor:

```bash
python level_editor.py
```

Controls for the level editor:
- Arrow keys: Move cursor
- P: Place/remove platform
- O: Place/remove coin
- X: Place/remove obstacle
- @: Set player start position
- S: Save level
- L: Load existing level
- N: New blank level
- H: Show help
- Q: Quit editor
