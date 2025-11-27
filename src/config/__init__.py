"""
Configuration Module
Centralized game configuration
"""

# Common configs
from .common import Colors, WindowConfig

# Game config
from .game import GameConfig

# Player config
from .player import PlayerConfig

# Enemy configs
from .enemies import (
    BaseEnemyConfig,
    FastEnemyConfig,
    TankEnemyConfig,
    EliteEnemyConfig,
)

# Weapon configs
from .weapons import (
    BaseWeaponConfig,
    BasicWeaponConfig,
)

# Spawn manager
from .spawn_manager import SpawnManagerConfig

__all__ = [
    # Common
    "Colors",
    "WindowConfig",
    # Game
    "GameConfig",
    # Player
    "PlayerConfig",
    # Enemies
    "BaseEnemyConfig",
    "FastEnemyConfig",
    "TankEnemyConfig",
    "EliteEnemyConfig",
    # Weapons
    "BaseWeaponConfig",
    "BasicWeaponConfig",
    # Spawn
    "SpawnManagerConfig",
]
