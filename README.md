# 🐍 Snake Game

<img width="626" height="725" alt="{375C1B9F-A9C1-49AB-9982-00DCBE95C717}" src="https://github.com/user-attachments/assets/7bbb8743-f29b-41ec-b2c0-d7210a54a272" />

<img width="623" height="723" alt="{94B9B575-97A7-4E4C-853D-4D14EECA62D8}" src="https://github.com/user-attachments/assets/f1e20e4e-9a0d-436a-8186-e94bf7601b9f" />

<img width="629" height="724" alt="{73643284-7679-4155-835B-F07F7E5DCCDD}" src="https://github.com/user-attachments/assets/ca4a5808-d93d-49e9-afd0-b5c98ddbb0a5" />


A classic Snake game built from scratch in Python with **Pygame**, featuring a full menu system with
selectable difficulty and visual themes, a persistent all-time high score, sound effects, and smooth
navigation between the start menu, gameplay, and game-over screen.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-Game%20Engine-green?logo=python&logoColor=white)

## Features

- **Start menu** — click "Start Game" or press Enter, with clickable selectors for difficulty
  (Easy / Medium / Hard) and visual theme.
- **Multiple themes** — cycle between *Classic Dark*, *Retro Neon*, and *Matrix Green*, each with its
  own background, grid, snake, and snack colors.
- **Persistent high score** — the all-time best score is saved to `highscore.txt` and shown on both the
  menu and the live score bar, so it survives between sessions.
- **Sound effects** — optional eat and game-over sounds (`eat.wav`, `gameover.wav`), loaded automatically
  if present, with graceful fallback if they're missing.
- **Classic snake mechanics** — grid-based movement, growing tail, self-collision and wall-collision
  detection.
- **Game-over screen** — shows the final score and high score, with **Restart**, **Main Menu**, and
  **Exit** options (or press Enter to restart instantly).

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move the snake |
| Enter | Start / Restart |
| Mouse click | Menu buttons (Start, Mode, Theme, Restart, Main Menu, Exit) |

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

> **Optional:** drop `eat.wav` and `gameover.wav` files into the project folder to enable sound effects —
> the game runs fine without them.

## Project Structure

```
snake-game/
├── snake.py            # Game logic, rendering, menus, themes, high score, sound
├── requirements.txt    # Dependencies (pygame)
├── highscore.txt        # Auto-created on first run to persist the best score
├── eat.wav              # Optional — eat sound effect
└── gameover.wav          # Optional — game-over sound effect
```

## Tech Stack

- **Python** — core game logic
- **Pygame** — rendering, input handling, sound, and the game loop

## Possible Improvements

- On-screen theme preview before selection
- Adjustable grid size or board dimensions
- Leaderboard with multiple saved scores instead of a single high score
