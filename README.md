# Vampire Survivors Clone

A bullet-heaven style game built with Pygame, inspired by Vampire Survivors.

## Features (Work in Progress)

- Player movement and control
- Enemy spawning with difficulty scaling
- Automatic weapon system
- Experience and leveling

## Requirements

- Python 3.7+
- Pygame

## Installation
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python main.py
```

## Controls

- **WASD** - Move
- **ESC** - Pause
- **SPACE** - dash
- upgrade 1-3 keys

## Project Structure
```
vampire-survivors-game/
├── main.py           # Entry point
├── src/
│   ├── config.py     # Game configuration
│   ├── game_engine.py       # Main game controller
│   ├── entities/     # Game entities (Player, Enemy, etc.)
│   ├── systems/      # Game systems (Spawning, Weapons, etc.)
│   └── ui/           # User interface components
└── assets/
    └── sprites/      # Game sprites and animations
```

## License

Free to use for learning and personal projects.
