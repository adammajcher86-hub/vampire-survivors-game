"""
Base Enemy Configuration
Default enemy settings and variants
"""

from ..common import Colors


class BaseEnemyConfig:
    """Base enemy settings"""

    # Stats
    SIZE = 24
    SPEED = 80
    DAMAGE = 10
    HEALTH = 50
    XP_VALUE = 5

    # Appearance
    COLOR = Colors.RED

    @classmethod
    def get_radius(cls):
        """Get enemy collision radius"""
        return cls.SIZE // 2


class FastEnemyConfig(BaseEnemyConfig):
    """Fast enemy variant - high speed, low health"""

    SIZE = 20
    SPEED = 150
    HEALTH = 30
    DAMAGE = 8
    COLOR = Colors.ORANGE


class TankEnemyConfig(BaseEnemyConfig):
    """Tank enemy variant - slow but tough"""

    SIZE = 32
    SPEED = 50
    HEALTH = 150
    DAMAGE = 20
    XP_VALUE = 15
    COLOR = Colors.GRAY


class EliteEnemyConfig(BaseEnemyConfig):
    """Elite enemy variant - balanced and dangerous"""

    SIZE = 28
    SPEED = 100
    HEALTH = 100
    DAMAGE = 15
    XP_VALUE = 20
    COLOR = Colors.PURPLE
