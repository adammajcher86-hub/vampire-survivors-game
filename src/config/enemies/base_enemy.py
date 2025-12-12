"""
Base Enemy Configuration
Default enemy settings
"""

from ..common import Colors


class BaseEnemyConfig:
    """Base enemy settings"""

    # Stats
    SIZE = 24
    SPEED = 80
    CONTACT_DAMAGE = 0.5
    HEALTH = 50
    XP_VALUE = 5

    # Appearance
    COLOR = Colors.RED

    @classmethod
    def get_radius(cls):
        """Get enemy collision radius"""
        return cls.SIZE // 2
