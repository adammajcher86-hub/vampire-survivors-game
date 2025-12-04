"""
Tank Laser Configuration
Parameters for Tank enemy laser attacks
"""


class TankLaserConfig:
    """Tank enemy laser projectile configuration"""

    # Shooting behavior
    SHOOT_COOLDOWN_MIN = 2.0  # seconds
    SHOOT_COOLDOWN_MAX = 3.5  # seconds
    SHOOT_RANGE = 400  # Only shoot if player within this range
    TELEGRAPH_DURATION = 0.3  # Warning flash before shooting

    # Laser projectile
    LASER_SPEED = 800  # pixels per second
    LASER_DAMAGE = 25
    LASER_LIFETIME = 6.0  # seconds

    # Visual
    LASER_LENGTH = 15  # pixels
    LASER_WIDTH = 4  # pixels
    LASER_COLOR = (255, 0, 0)  # Red (enemy laser)
    LASER_GLOW_COLOR = (255, 100, 100)  # Light red glow
