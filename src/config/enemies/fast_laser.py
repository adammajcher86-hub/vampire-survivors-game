"""
Fast Enemy Laser Configuration
Lasers fired in radial burst when FastEnemy explodes
"""

from src.config.projectiles import BaseProjectileConfig


class FastLaserConfig(BaseProjectileConfig):
    """Fast enemy explosion laser configuration"""

    # Laser projectile
    LASER_SPEED = 500
    LASER_DAMAGE = 20
    LASER_LIFETIME = 3.0

    # Visual (orange/yellow to match FastEnemy)
    LASER_LENGTH = 15
    LASER_WIDTH = 4
    LASER_COLOR = (255, 200, 100)  # Orange
    LASER_GLOW_COLOR = (255, 220, 150)  # Light orange
