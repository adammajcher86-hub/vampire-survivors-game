"""
Basic Weapon
Starting weapon - single auto-aim projectile
"""

from src.entities.weapons.base_weapon import BaseWeapon
from src.entities.weapons.projectile import Projectile
from src.config import BaseWeaponConfig


class BasicWeapon(BaseWeapon):
    """Basic auto-aim weapon - fires single projectile at nearest enemy"""

    def __init__(self):
        """Initialize basic weapon with default stats"""
        super().__init__(
            cooldown=BaseWeaponConfig.ATTACK_COOLDOWN,
            damage=BaseWeaponConfig.PROJECTILE_DAMAGE,
            projectile_speed=BaseWeaponConfig.PROJECTILE_SPEED,
            range=BaseWeaponConfig.RANGE,
            level=1,
        )

        # Visual properties
        self.projectile_color = BaseWeaponConfig.PROJECTILE_COLOR
        self.projectile_size = BaseWeaponConfig.PROJECTILE_SIZE

    def fire(self, player, target, projectiles):
        """
        Fire single projectile at target

        Args:
            player: Player entity (source position)
            target: Target enemy
            projectiles: Sprite group to add projectile to
        """
        # Create projectile aimed at target
        projectile = Projectile(
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
