"""
Spread Weapon
Mouse-controlled spread shot weapon
"""

import pygame
import math
from src.entities.weapons.base_weapon import BaseWeapon
from src.entities.projectiles.spread_projectile import SpreadProjectile
from src.config.weapons.spread_weapon import SpreadWeaponConfig


class SpreadWeapon(BaseWeapon):
    """Spread weapon - fires multiple projectiles in arc toward mouse"""

    def __init__(self):
        """Initialize spread weapon"""
        super().__init__(
            cooldown=SpreadWeaponConfig.FIRE_COOLDOWN,
            damage=SpreadWeaponConfig.PROJECTILE_DAMAGE,
            projectile_speed=SpreadWeaponConfig.PROJECTILE_SPEED,
            range=SpreadWeaponConfig.PROJECTILE_LIFETIME
            * SpreadWeaponConfig.PROJECTILE_SPEED,
        )
        self.cooldown = SpreadWeaponConfig.FIRE_COOLDOWN
        self.cooldown_timer = 0.0
        self.level = 1

    def fire(self, player, target, projectiles):
        """
        Fire method (required by BaseWeapon)
        Not used - SpreadWeapon uses update() with mouse position instead

        Args:
            player: Player entity
            target: Target entity (not used)
            projectiles: Projectile sprite group
        """
        pass  # SpreadWeapon handles firing in update() method

    def update(self, dt, player, enemies, projectiles, mouse_world_pos=None):
        """
        Update spread weapon - fires toward mouse cursor

        Args:
            dt: Delta time
            player: Player entity
            enemies: Enemy sprite group (not used for this weapon)
            projectiles: Projectile sprite group
            mouse_world_pos: Mouse position in world coordinates (Vector2)
        """
        # Update cooldown
        self.cooldown_timer -= dt

        # Check if can fire
        if self.cooldown_timer <= 0 and mouse_world_pos:
            self._fire_spread(player, projectiles, mouse_world_pos)
            self.cooldown_timer = self.cooldown / player.attack_speed_multiplier

    def _fire_spread(self, player, projectiles, mouse_world_pos):
        """
        Fire spread of projectiles toward mouse

        Args:
            player: Player entity
            projectiles: Projectile sprite group
            mouse_world_pos: Mouse position in world coordinates
        """
        # Calculate direction to mouse
        direction = mouse_world_pos - player.position
        if direction.length() == 0:
            return

        direction = direction.normalize()

        # Calculate base angle (direction to mouse)
        base_angle = math.atan2(direction.y, direction.x)

        # Calculate spread angles
        projectile_count = SpreadWeaponConfig.PROJECTILE_COUNT
        spread_angle_rad = math.radians(SpreadWeaponConfig.SPREAD_ANGLE)

        # Create projectiles in spread pattern
        for i in range(projectile_count):
            # Calculate offset angle for this projectile
            if projectile_count > 1:
                offset = (i / (projectile_count - 1) - 0.5) * spread_angle_rad
            else:
                offset = 0

            projectile_angle = base_angle + offset

            # Calculate direction vector for this projectile
            proj_direction = pygame.math.Vector2(
                math.cos(projectile_angle), math.sin(projectile_angle)
            )

            # Create projectile
            projectile = SpreadProjectile(
                player.position.x, player.position.y, proj_direction
            )

            projectiles.add(projectile)

    def level_up(self):
        """Increase weapon level"""
        self.level += 1

    def get_description(self):
        """Get weapon description"""
        return f"Spread Shot (Level {self.level})"
