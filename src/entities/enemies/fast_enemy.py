"""
Fast Enemy
Quick, low-health enemy that moves faster than the player
"""

from src.entities.enemies.base_enemy import Enemy
from src.config import FastEnemyConfig


class FastEnemy(Enemy):
    """Fast enemy - high speed, low health"""

    def __init__(self, x, y):
        """
        Initialize fast enemy

        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__(x, y, FastEnemyConfig)
