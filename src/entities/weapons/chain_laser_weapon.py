"""
Chain Laser Weapon
A continuous beam weapon that locks onto enemies and can chain between them
"""

from src.entities.weapons.base_weapon import BaseWeapon
from src.config.weapons.chain_laser import ChainLaserConfig
from src.entities.projectiles.chain_laser_projectile import ChainLaserProjectile


class ChainLaserWeapon(BaseWeapon):
    """Chain laser weapon - continuous beam with damage over time"""

    def __init__(self, level=1):
        super().__init__(
            cooldown=ChainLaserConfig.COOLDOWN,
            damage=ChainLaserConfig.DAMAGE_PER_SECOND,
            projectile_speed=0,  # Instant beam
            range=ChainLaserConfig.RANGE,
            level=level,
            auto_aim=ChainLaserConfig.AUTO_AIM,
        )

        self.active_beam = None  # Current beam instance

    def update_from_slot(
        self, dt, player, enemies, projectiles, mouse_world_pos, weapon_tip
    ):
        """
        Update weapon - manage continuous beam

        Args:
            dt: Delta time
            player: Player entity
            enemies: Enemy sprite group
            projectiles: Projectile sprite group (not used for beams)
            mouse_world_pos: Mouse world position
            weapon_tip: Vector2 position of weapon tip
        """
        # Update cooldown (for retargeting)
        self.cooldown_timer -= dt * player.attack_speed_multiplier

        # Update existing beam
        if self.active_beam is not None:
            # Update beam with current weapon tip position
            if not self.active_beam.update(dt, weapon_tip, enemies):
                # Beam expired (target died or out of range)
                self.active_beam = None

        # Try to acquire new target if no active beam and cooldown ready
        if self.active_beam is None and self.cooldown_timer <= 0:
            target = self._find_target_from_position(weapon_tip, enemies)
            if target:
                self.active_beam = ChainLaserProjectile(
                    weapon_tip, target, weapon_level=self.level
                )
                self.cooldown_timer = self.cooldown

                # Trigger fire callback
                if self.on_fire_callback:
                    self.on_fire_callback()

    def fire_from_position(self, weapon_tip, target_pos, projectiles):
        """
        Not used for chain laser - we manage beams in update_from_slot
        Keeping this for base class compatibility
        """
        pass

    def render_beams(self, screen, camera):
        """
        Render active beam

        Call this from game engine after rendering other projectiles
        """
        if self.active_beam:
            self.active_beam.render(screen, camera)

    def _apply_level_up_bonus(self):
        """Apply level up bonuses - update damage from config"""
        self.damage = ChainLaserConfig.get_damage_per_second(self.level)

        # Update active beam if it exists
        if self.active_beam:
            self.active_beam.weapon_level = self.level
            self.active_beam.damage_per_second = self.damage
            self.active_beam.max_chains = ChainLaserConfig.get_max_chains(self.level)

    def get_name(self):
        """Get weapon name"""
        return "Chain Laser"

    def get_description(self):
        """Get weapon description"""
        if self.level < ChainLaserConfig.CHAIN_ENABLED_AT_LEVEL:
            return f"Continuous beam weapon. Deals {int(self.damage)} DPS.\nChains at level {ChainLaserConfig.CHAIN_ENABLED_AT_LEVEL}!"
        else:
            max_chains = ChainLaserConfig.get_max_chains(self.level)
            return f"Continuous beam weapon. Deals {int(self.damage)} DPS.\nChains to {max_chains} additional enemies!"
