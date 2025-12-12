"""
Fast Enemy Configuration
Fast, low health enemy with circling and dash behavior
"""


class FastEnemyConfig:
    """Fast enemy configuration"""

    # Stats
    HEALTH = 5
    SPEED = 120  # Fast movement
    CONTACT_DAMAGE = 3
    SIZE = 15
    XP_VALUE = 2
    COLOR = (255, 200, 100)  # Orange

    # Circling behavior
    ORBIT_DISTANCE = 250  # Target distance from player
    ORBIT_THRESHOLD = 50  # +/- tolerance (200-300px)
    RADIAL_SPEED_MULT = 0.5  # How fast to adjust distance

    # Dash attack
    DASH_COOLDOWN_MIN = 3.0  # seconds
    DASH_COOLDOWN_MAX = 5.0  # seconds
    DASH_SPEED = 600  # Very fast dash
    DASH_DURATION = 1
    TELEGRAPH_DURATION = 0.5  # Warning before dash
    TELEGRAPH_COLOR = (255, 50, 50)  # Red flash

    EXPLOSION_CHANCE = 0.3  # 30% chance to explode after dash
    EXPLOSION_LASER_COUNT = 8  # Number of lasers in radial burst
    EXPLOSION_LASER_DAMAGE = 20  # Damage per laser
    EXPLOSION_LASER_SPEED = 500  # Laser speed
