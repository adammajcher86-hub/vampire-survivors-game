"""
Configuration Package
Centralized game configuration

Usage:
    from src.config import WindowConfig, Colors, PlayerConfig

    screen = pygame.display.set_mode((WindowConfig.WIDTH, WindowConfig.HEIGHT))
    player_speed = PlayerConfig.SPEED
    bg_color = Colors.BACKGROUND
"""

# Common configs (used everywhere)
from .common import WindowConfig, Colors

# Game systems
from .game import GameConfig
from .player import PlayerConfig
from .spawn_manager import SpawnManagerConfig

# Enemies
from .enemies import BaseEnemyConfig, FastEnemyConfig, TankEnemyConfig, EliteEnemyConfig

# Weapons
from .weapons import (
    BaseWeaponConfig,
    SpreadWeaponConfig,
    LaserWeaponConfig,
    RapidFireConfig,
)

__all__ = [
    # Common
    "WindowConfig",
    "Colors",
    # Game
    "GameConfig",
    "PlayerConfig",
    "SpawnManagerConfig",
    # Enemies
    "BaseEnemyConfig",
    "FastEnemyConfig",
    "TankEnemyConfig",
    "EliteEnemyConfig",
    # Weapons
    "BaseWeaponConfig",
    "SpreadWeaponConfig",
    "LaserWeaponConfig",
    "RapidFireConfig",
]
