"""
Laser Weapon Configuration (Player)
Parameters for player laser weapon (future)
"""


class LaserWeaponConfig:
    """Player laser weapon configuration"""

    FIRE_COOLDOWN = 0.2  # Fires 5 times per second
    DAMAGE = 1.5  # Damage per shot
    RANGE = 200  # Max laser range
    BOUNCE_RANGE = 130  # Max distance for bounce
    BEAM_COLOR = (255, 50, 50)  # Red
    BEAM_WIDTH = 3
    BASE_BOUNCES = 2
