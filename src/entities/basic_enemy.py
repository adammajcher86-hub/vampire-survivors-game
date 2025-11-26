"""
Basic Enemy
Standard enemy with balanced stats
"""

from src.entities.base_enemy import Enemy
from src.config import BaseEnemyConfig


class BasicEnemy(Enemy):
    """Basic enemy - balanced stats, most common enemy type"""

    def __init__(self, x, y):
        """
        Initialize basic enemy

        Args:
            x: Initial x position
            y: Initial y position
        """
        super().__init__(x, y, BaseEnemyConfig)
