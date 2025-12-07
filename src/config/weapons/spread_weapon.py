"""
Spread Weapon Configuration
Parameters for player spread shot weapon
"""


class SpreadWeaponConfig:
    """Spread weapon configuration"""

    # Firing
    FIRE_COOLDOWN = 2  # seconds between shots

    # Projectiles
    PROJECTILE_COUNT = 3  # Number of projectiles per shot
    SPREAD_ANGLE = 30  # Total spread angle in degrees
    PROJECTILE_SPEED = 600  # pixels per second
    PROJECTILE_DAMAGE = 10  # damage per projectile
    PROJECTILE_LIFETIME = 2.0  # seconds
    PROJECTILE_SIZE = 3  # radius in pixels

    # Visual
    PROJECTILE_COLOR = (255, 215, 0)  # Gold/yellow
    PROJECTILE_GLOW_COLOR = (255, 240, 150)  # Light yellow glow

    # Crosshair
    CROSSHAIR_SIZE = 15  # pixels
    CROSSHAIR_COLOR = (255, 215, 0)  # Gold to match projectiles
    CROSSHAIR_THICKNESS = 2  # line width
