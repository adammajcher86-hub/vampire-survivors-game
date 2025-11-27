"""
Tank Enemy Configuration
Tank enemy variant - slow but tough
"""

from .base_enemy import BaseEnemyConfig
from ..common import Colors


class TankEnemyConfig(BaseEnemyConfig):
    """Tank enemy variant - slow but tough"""

    SIZE = 32
    SPEED = 50
    HEALTH = 150
    DAMAGE = 20
    XP_VALUE = 15
    COLOR = Colors.GRAY
