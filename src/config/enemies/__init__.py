"""
Enemy Configurations
All enemy config classes
"""

from .base_enemy import BaseEnemyConfig
from .fast_enemy import FastEnemyConfig
from .tank_enemy import TankEnemyConfig
from .elite_enemy import EliteEnemyConfig

__all__ = [
    "BaseEnemyConfig",
    "FastEnemyConfig",
    "TankEnemyConfig",
    "EliteEnemyConfig",
]
