"""
Base Weapon Configuration
Default weapon settings
"""

from ..common import Colors


class BaseWeaponConfig:
    """Base weapon settings"""

    # Attack properties
    ATTACK_COOLDOWN = 1.0  # Seconds between shots
    RANGE = 300  # Targeting range

    # Projectile properties
    PROJECTILE_SPEED = 300
    PROJECTILE_DAMAGE = 20
    PROJECTILE_LIFETIME = 2.0  # Seconds
    PROJECTILE_SIZE = 8
    PROJECTILE_COLOR = Colors.YELLOW
