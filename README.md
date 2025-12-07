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
├── main.py                     # Entry point
├── src/
│   ├── game_engine.py          # Main game controller
│   ├── camera.py               # Camera system
│   │
│   ├── config/                 # Game configuration
│   │   ├── common/             # Shared configs (window, colors)
│   │   ├── enemies/            # Enemy type configs
│   │   ├── weapons/            # Weapon configs
│   │   ├── game.py             # Game settings
│   │   ├── player.py           # Player settings
│   │   └── spawn_manager.py    # Spawn Manager
│   │
│   ├── entities/               # Game entities
│   │   ├── player.py           # Player character
│   │   ├── enemies/            # Enemy types (polymorphic)
│   │   │   ├── base_enemy.py
│   │   │   ├── basic_enemy.py
│   │   │   ├── fast_enemy.py
│   │   │   ├── tank_enemy.py
│   │   │   └── elite_enemy.py  # With dash attack
│   │   ├── weapons/            # Weapon types (polymorphic)
│   │   │   ├── base_weapon.py
│   │   │   └── basic_weapon.py
│   │   ├── projectiles/        # Projectile types (polymorphic)
│   │   │   ├── base_projectile.py
│   │   │   └── basic_projectile.py
│   │   └── pickups/            # Pickup types (polymorphic)
│   │       ├── base_pickup.py
│   │       ├── xp_orb.py
│   │       └── health_pickup.py
│   │
│   ├── systems/                # Game systems
│   │   ├── wave_system.py    # wave system
│   │   ├── enemy_spawner.py    # Enemy spawning
│   │   ├── xp_system.py        # XP & leveling
│   │   ├── upgrade_system.py   # Upgrade management
│   │   └── pickups/            # Pickup systems
│   │       ├── pickup_manager.py   # Pickup spawning/collection
│   │       └── drop_tables.py      # Drop rate configuration
│   │
│   ├── ui/                     # User interface
│   │   └── upgrade_menu.py     # Level-up menu
│   │
│   └── upgrades/               # Upgrade types (polymorphic)
│       ├── base_upgrade.py
│       ├── new_weapon_upgrade.py
│       ├── weapon_level_upgrade.py
│       └── stat_upgrade.py
│
└── assets/                     # (Future) Game assets
    └── sprites/                # Sprites and animations
```
