"""
Tank Enemy
Slow, high-health enemy that deals heavy damage
"""

from src.entities.enemies.base_enemy import Enemy
from src.config import TankEnemyConfig


class TankEnemy(Enemy):
    """Tank enemy - low speed, high health and damage"""

    def __init__(self, x, y):
        """
        Initialize tank enemy

        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__(x, y, TankEnemyConfig)
