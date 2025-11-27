"""
Basic Projectile
Standard yellow bullet projectile
"""

import pygame
from src.entities.projectiles.base_projectile import BaseProjectile
from src.config import BasicWeaponConfig


class BasicProjectile(BaseProjectile):
    """Basic yellow bullet projectile"""

    def __init__(
        self, x, y, target_pos, damage=None, speed=None, color=None, size=None
    ):
        """
        Initialize basic projectile

        Args:
            x: Starting x position
            y: Starting y position
            target_pos: Vector2 of target position (for direction)
            damage: Damage dealt (default from config)
            speed: Projectile speed (default from config)
            color: Projectile color (default from config)
            size: Projectile size (default from config)
        """
        # Use config defaults if not specified
        damage = damage if damage is not None else BasicWeaponConfig.PROJECTILE_DAMAGE
        speed = speed if speed is not None else BasicWeaponConfig.PROJECTILE_SPEED

        # Initialize base
        super().__init__(
            x, y, damage, speed, lifetime=BasicWeaponConfig.PROJECTILE_LIFETIME
        )

        # Visual properties
        self.color = color if color is not None else BasicWeaponConfig.PROJECTILE_COLOR
        self.size = size if size is not None else BasicWeaponConfig.PROJECTILE_SIZE
        self.radius = self.size // 2

        # Calculate direction to target
        direction = pygame.math.Vector2(target_pos.x - x, target_pos.y - y)
        if direction.length() > 0:
            direction = direction.normalize()

        # Movement velocity (straight line)
        self.velocity = direction * self.speed

        # Update rect size
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

    def _update_movement(self, dt):
        """
        Update basic projectile movement (straight line)

        Args:
            dt: Delta time in seconds
        """
        # Simple straight-line movement
        self.position += self.velocity * dt

    def render(self, screen, camera):
        """
        Draw the basic projectile (yellow circle)

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        screen_pos = camera.apply(self.position)

        # Draw projectile as a circle
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )
