```
                    _ _                           
     /\            (_(_)                          
    /  \   ___  ___ _ _   _ __ __ _  ___ ___ _ __ 
   / /\ \ / __|/ __| | | | '__/ _` |/ __/ _ | '__|
  / ____ \\__ | (__| | | | | | (_| | (_|  __| |   
 /_/    \_|___/\___|_|_| |_|  \__,_|\___\___|_|   
```                                              
                                                  

An endless racing game that runs in the terminal. 100% Python.

## Instructions

Collect as many alcoholic drinks as possible, while avoiding the `Beer` drinks. The game is only key-based.

| Keys | Role        |
|------|-------------|
| a    | Move Left   |
| d    | Move Right  |
| w    | Accelerate  |
| s    |  Decelerate |
| q    |  Quit game  |

### Installation

> ```diff
> + Please report issues if you try to install and run into problems!
> ```

Make sure you are running at least Python 3.6.0

Install using pip:
```bash
pip3 install asciiracer
```
or clone the repository and install manually:

```bash
$ git clone https://github.com/UpGado/ascii_racer.git
$ cd ascii_racer && python3 setup.py install
```

### Start Game
To start the game, run either:
```bash
$ asciiracer
$ python -m asciiracer
```

### Scoring
There are four different types of drinks that you can collect on the racetrack. 
* Vodka - 10 Points
* Gin - 5 Points
* $ - 1 Point
* Beer - Negative 20 points

#### Possible Improvements

- Color support.
- Curvy roads and more interesting tracks.
- Multiplayer/Competitive racing.
- *Your* creative idea.
