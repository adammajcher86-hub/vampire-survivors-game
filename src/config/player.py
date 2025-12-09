"""
Player Configuration
Player character settings
"""

from .common import Colors


class PlayerConfig:
    """Player character settings"""

    # Stats
    SIZE = 50
    SPEED = 200
    MAX_HEALTH = 100
    HEALTH_REGEN = 0.5  # HP per second

    # Appearance
    COLOR = Colors.BLUE

    # Collision
    @classmethod
    def get_radius(cls):
        """Get player collision radius"""
        return cls.SIZE // 2
