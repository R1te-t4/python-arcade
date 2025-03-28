# Treasure Hunter

A console-based adventure game where you navigate through randomly generated dungeons, find treasure, avoid traps and monsters, and escape with the highest score!

## Game Description

In Treasure Hunter, you play as an adventurous explorer searching for legendary lost treasure. Your goal is to navigate through a dungeon, find the treasure, and make it to the exit alive. Watch out for traps and monsters that will damage your health along the way!

## Features

- Randomly generated dungeons - each game is different!
- Various entities: treasure, traps, and monsters
- Very simple keyboard controls (WASD)
- Scoring system that rewards efficiency and health preservation
- Fog of war - only areas you've explored are revealed

## Game Symbols

- `@` - Player (you)
- `$` - Treasure
- `T` - Trap
- `M` - Monster
- `E` - Exit
- `#` - Wall
- `.` - Empty space

## Controls

- `W` - Move up
- `A` - Move left
- `S` - Move down
- `D` - Move right
- `H` - Show help
- `Q` - Quit game

## Requirements

- Python 3.6 or higher

## How to Run the Game

### Option 1: Running from Source

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/R1te-t4/python-arcade
   cd python-arcade/TreasureHunter
   ```

2. Run the game:
   ```
   python treasure_hunter.py
   ```

### Option 2: Direct Execution (Windows)

1. Make sure Python is installed and in your PATH
2. Double-click on `treasure_hunter.py` or run it from the command prompt:
   ```
   python treasure_hunter.py
   ```

### Option 3: Running on OSX/Linux

1. Open Terminal
2. Navigate to the directory containing the game:
   ```
   cd path/to/TreasureHunter
   ```
3. Run the game:
   ```
   python3 treasure_hunter.py
   ```

## File Map

```
treasure-hunter/
├── game/
│   ├── __init__.py
│   ├── display.py      # Handles terminal output and rendering
│   ├── dungeon.py      # Generates random dungeon layouts
│   ├── entities.py     # Defines game entities (treasure, traps, monsters)
│   ├── game_engine.py  # Core game mechanics and input handling
│   └── player.py       # Player state and movement
└── treasure_hunter.py  # Main game file
```

## Troubleshooting

If you encounter any issues:

1. Make sure you have Python 3.6+ installed
2. Try running the game with `python -u treasure_hunter.py` to disable output buffering
3. If your terminal doesn't support color codes, edit `display.py` and set `use_colors = False`
4. On some terminals, you may need to press Enter after each key press
