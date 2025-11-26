"""
Configuration Package
Centralized game configuration using classes

Usage:
    from src.config import WindowConfig, PlayerConfig, BaseEnemyConfig

    screen = pygame.display.set_mode((WindowConfig.WIDTH, WindowConfig.HEIGHT))
    player_speed = PlayerConfig.SPEED
"""

from src.config.common.window import WindowConfig
from src.config.common.game import GameConfig
from .player import PlayerConfig
from .enemies import BaseEnemyConfig, FastEnemyConfig, TankEnemyConfig
from .weapons import BaseWeaponConfig, SpreadWeaponConfig, LaserWeaponConfig
from .spawn_manager import SpawnManagerConfig

__all__ = [
    'WindowConfig',
    'GameConfig',
    'PlayerConfig',
    'BaseEnemyConfig',
    'FastEnemyConfig',
    'TankEnemyConfig',
    'BaseWeaponConfig',
    'SpreadWeaponConfig',
    'LaserWeaponConfig',
    'SpawnManagerConfig',
]