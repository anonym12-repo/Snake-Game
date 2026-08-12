# 🐍 Snake Game

A classic Snake game built from scratch in Python with **Pygame**, featuring a start menu with
selectable difficulty, a live score bar, and a game-over screen with a one-click restart.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-Game%20Engine-green?logo=python&logoColor=white)

## Features

- **Start menu** — click "Start Game" or press Enter, with a clickable difficulty selector
  (Easy / Medium / Hard) that controls game speed.
- **Classic snake mechanics** — grid-based movement, growing tail, self-collision and
  wall-collision detection.
- **Live score bar** — a dedicated top bar renders the current score during play, separate from
  the game grid.
- **Game-over screen** — shows the final score with **Restart** and **Exit** buttons (or press
  Enter to restart), so you can keep playing without relaunching the script.

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move the snake |
| Enter | Start / Restart |
| Mouse click | Menu buttons (Start, difficulty, Restart, Exit) |

## Getting Started

### Prerequisites
- Python 3.x

### Installation & Run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/snake-game.git
cd snake-game

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the game
python snake.py
```

## Project Structure

```
snake-game/
├── snake.py            # Game logic, rendering, menus
└── requirements.txt     # Dependencies (pygame)
```

## Tech Stack

- **Python** — core game logic
- **Pygame** — rendering, input handling, game loop

## Possible Improvements

- Persistent high-score tracking (save best score between sessions)
- Sound effects for eating/game over
- Adjustable grid size or board themes
