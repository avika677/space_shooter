# Cyber-Shooter 2088

A high-performance, arcade-style space shooter built entirely in Python using Pygame. It features stunning retro-modern vector graphics with neon glow rendering, rich particle systems, screen shake feedback, multiple enemy archetypes, and an epic boss fight.

## Key Features
* **Stunning Neon Glow Aesthetics**: All graphics are drawn programmatically using layered vector shapes and alpha blending to create a true arcade CRT glow—no image asset files required!
* **Smooth Flight Mechanics**: Keyboard-driven spaceship controls with physical inertia and visual bank-tilting.
* **Upgrades & Combat**: 4 weapon tiers (Single, Double, Spread, and Quad-Beam) and power-ups (Shield Recharging, Weapon Upgrades, Hull Repair).
* **Multiple Enemy Types**: 
  * *Scouts*: Wavy sine-wave movement patterns.
  * *Strikers*: Aggressively track the player and shoot targeted lasers.
  * *Cruisers*: Heavy tank battleships shooting wide yellow laser spreads.
  * *Dreadnought Boss*: Spawns at 3000 points with multiple phase triggers, warning alarms, and screen-clearing bullet hell patterns.
* **On-the-fly Audio Synthesis**: Generates retro synth sound effects dynamically using math formulas. Silent fallback mode if no audio hardware is found.
* **Persistent High Scores**: Saves your high score locally in a text file.

## Setup Instructions

### 1. Install Python
Ensure Python (version 3.8 or higher) is installed on your system. You can check this by running in your terminal/powershell:
```bash
python --version
```

### 2. Install Pygame (or Pygame-CE)
We recommend **Pygame Community Edition (`pygame-ce`)** for better rendering speeds, but standard `pygame` works as well. Install it by running the requirements file:
```bash
pip install -r requirements.txt
```
*(Or manually install via `pip install pygame-ce`)*

### 3. Run the Game
Double-click `game.py` or run it from VSCode / terminal:
```bash
python game.py
```

## Game Controls

| Key | Action |
| --- | --- |
| **W / S / A / D** or **Arrow Keys** | Fly (Move spaceship with momentum) |
| **Spacebar** | Fire laser cannon (Hold to fire continuously) |
| **P** | Pause / Resume the game |
| **Enter** | Start game (from Menu) / Respawn (from Game Over) |
| **C** | View controls and settings (from Menu) |
| **Escape** | Quit game (or return to menu from gameplay) |

## Customization & Modding
Since the game is programmatically rendered, you can easily change colors, spaceship dimensions, and behaviors inside `game.py` without needing graphics software!
* Check `BG_COLOR`, `CYAN`, `MAGENTA`, etc. at the top of the file to tweak the neon themes.
* Speed and health properties are highly modular. Tweak `Player` or `Enemy` subclasses to make the game easier, harder, or faster.
