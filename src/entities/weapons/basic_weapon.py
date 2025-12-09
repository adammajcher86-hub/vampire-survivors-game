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
        """Fire projectile at target"""
        if not target:
            return

        weapon_tip = player.get_weapon_tip_position()

        # Pass TARGET POSITION, not direction! ✅
        projectile = BasicProjectile(
            weapon_tip.x,
            weapon_tip.y,
            target.position,  # ✅ Pass position, not direction!
        )

        projectiles.add(projectile)

    def get_name(self):
        """Get weapon name"""
        return "Basic Weapon"
