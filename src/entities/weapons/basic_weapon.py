"""
Basic Weapon
Starting weapon - single auto-aim projectile
"""

from src.entities.weapons.base_weapon import BaseWeapon
from src.entities.projectiles.basic_projectile import BasicProjectile
from src.config import BasicWeaponConfig


class BasicWeapon(BaseWeapon):
    """Basic auto-aim weapon - fires single projectile at nearest enemy"""

    def __init__(self):
        """Initialize basic weapon with default stats"""
        super().__init__(
            cooldown=BasicWeaponConfig.ATTACK_COOLDOWN,
            damage=BasicWeaponConfig.PROJECTILE_DAMAGE,
            projectile_speed=BasicWeaponConfig.PROJECTILE_SPEED,
            range=BasicWeaponConfig.RANGE,
            level=1,
            auto_aim=True,
        )

        # Visual properties
        self.projectile_color = BasicWeaponConfig.PROJECTILE_COLOR
        self.projectile_size = BasicWeaponConfig.PROJECTILE_SIZE

    def fire_from_position(self, weapon_tip, target_pos, projectiles):
        """
        Fire projectile from weapon tip toward target

        Args:
            weapon_tip: Vector2 position to fire from
            target_pos: Vector2 position to fire toward
            projectiles: Sprite group
        """
        projectile = BasicProjectile(weapon_tip.x, weapon_tip.y, target_pos)
        projectiles.add(projectile)

    def get_name(self):
        """Get weapon name"""
        return "Basic Weapon"
