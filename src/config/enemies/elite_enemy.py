"""
Elite Enemy Configuration
Elite enemy variant - balanced and dangerous
"""

from .base_enemy import BaseEnemyConfig
from ..common import Colors


class EliteEnemyConfig(BaseEnemyConfig):
    """Elite enemy variant - balanced and dangerous"""

    SIZE = 28
    SPEED = 100
    HEALTH = 100
    DAMAGE = 15
    XP_VALUE = 20
    COLOR = Colors.PURPLE

    # Visual
    color = (255, 215, 0)  # Gold
    size = 35
    radius = size // 2
