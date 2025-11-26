"""
Elite Enemy
Balanced enemy with high XP value
"""

from src.entities.base_enemy import Enemy
from src.config import EliteEnemyConfig


class EliteEnemy(Enemy):
    """Elite enemy - balanced stats, high XP reward"""

    def __init__(self, x, y):
        """
        Initialize elite enemy

        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__(x, y, EliteEnemyConfig)
