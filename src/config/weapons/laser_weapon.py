"""
Laser Weapon Configuration (Player)
Parameters for player laser weapon (future)
"""


class LaserWeaponConfig:
    """Player laser weapon configuration"""

    # Laser projectile
    LASER_SPEED = 1000  # Faster than enemy lasers
    LASER_DAMAGE = 40
    LASER_LIFETIME = 2.5

    # Visual (different from enemy)
    LASER_LENGTH = 20  # Longer beam
    LASER_WIDTH = 5
    LASER_COLOR = (0, 255, 255)  # Cyan (player laser)
    LASER_GLOW_COLOR = (100, 255, 255)  # Light cyan glow
