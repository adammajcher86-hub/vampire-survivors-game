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
        )

        # Visual properties
        self.projectile_color = BasicWeaponConfig.PROJECTILE_COLOR
        self.projectile_size = BasicWeaponConfig.PROJECTILE_SIZE

    def fire(self, player, target, projectiles):
        """
        Fire single projectile at target

        Args:
            player: Player entity (source position)
            target: Target enemy
            projectiles: Sprite group to add projectile to
        """
        # Create basic projectile aimed at target
        projectile = BasicProjectile(
            player.position.x,
            player.position.y,
            target.position,
            damage=self.damage,
            speed=self.projectile_speed,
            color=self.projectile_color,
            size=self.projectile_size,
        )
        projectiles.add(projectile)

    def get_name(self):
        """Get weapon name"""
        return "Basic Weapon"
