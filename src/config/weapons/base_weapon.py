"""
Base Weapon Configuration
Weapon settings and variants
"""

from ..common import Colors


class BaseWeaponConfig:
    """Base weapon settings"""

    # Weapon stats
    ATTACK_COOLDOWN = 1.0
    RANGE = 300

    # Projectile stats
    PROJECTILE_SPEED = 300
    PROJECTILE_SIZE = 8
    PROJECTILE_DAMAGE = 25
    PROJECTILE_LIFETIME = 2.0
    PROJECTILE_COLOR = Colors.YELLOW

    @classmethod
    def get_projectile_radius(cls):
        """Get projectile collision radius"""
        return cls.PROJECTILE_SIZE // 2


class SpreadWeaponConfig(BaseWeaponConfig):
    """Spread weapon - fires multiple projectiles"""

    ATTACK_COOLDOWN = 1.5
    PROJECTILE_COUNT = 3
    SPREAD_ANGLE = 30
    PROJECTILE_DAMAGE = 18
    PROJECTILE_COLOR = Colors.ORANGE


class LaserWeaponConfig(BaseWeaponConfig):
    """Laser weapon - fast, high damage, long cooldown"""

    ATTACK_COOLDOWN = 2.0
    PROJECTILE_SPEED = 500
    PROJECTILE_SIZE = 12
    PROJECTILE_DAMAGE = 50
    PROJECTILE_COLOR = Colors.CYAN


class RapidFireConfig(BaseWeaponConfig):
    """Rapid fire weapon - low damage, high fire rate"""

    ATTACK_COOLDOWN = 0.3
    PROJECTILE_DAMAGE = 10
    PROJECTILE_SIZE = 6
    PROJECTILE_COLOR = Colors.MAGENTA
