"""
Fast Enemy Configuration
Fast enemy variant - high speed, low health
"""

from .base_enemy import BaseEnemyConfig
from ..common import Colors


class FastEnemyConfig(BaseEnemyConfig):
    """Fast enemy variant - high speed, low health"""

    SIZE = 20
    SPEED = 150
    HEALTH = 30
    DAMAGE = 8
    COLOR = Colors.ORANGE
