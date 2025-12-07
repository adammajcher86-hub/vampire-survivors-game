"""
Spread Projectile
Gold projectiles fired in spread pattern
"""

import pygame
from src.entities.projectiles.base_projectile import BaseProjectile
from src.config.weapons.spread_weapon import SpreadWeaponConfig


class SpreadProjectile(BaseProjectile):
    """Spread weapon projectile"""

    def __init__(self, x, y, direction):
        """
        Initialize spread projectile

        Args:
            x: Starting x position
            y: Starting y position
            direction: Direction vector (normalized)
        """
        super().__init__(
            x,
            y,
            damage=SpreadWeaponConfig.PROJECTILE_DAMAGE,
            speed=SpreadWeaponConfig.PROJECTILE_SPEED,
            lifetime=SpreadWeaponConfig.PROJECTILE_LIFETIME,
        )

        # Movement
        self.direction = direction
        self.velocity = direction * SpreadWeaponConfig.PROJECTILE_SPEED

        # Visual
        self.radius = SpreadWeaponConfig.PROJECTILE_SIZE
        self.color = SpreadWeaponConfig.PROJECTILE_COLOR
        self.glow_color = SpreadWeaponConfig.PROJECTILE_GLOW_COLOR

    def _update_movement(self, dt):
        """Move projectile in direction"""
        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))

    def collides_with(self, entity):
        """
        Check collision with entity

        Args:
            entity: Entity to check collision with

        Returns:
            bool: True if colliding
        """
        distance = self.position.distance_to(entity.position)
        return distance < (self.radius + entity.radius)

    def render(self, screen, camera):
        """
        Render spread projectile with glow

        Args:
            screen: Pygame surface
            camera: Camera for position conversion
        """
        screen_pos = camera.apply(self.position)

        # Draw outer glow (larger, lighter)
        pygame.draw.circle(
            screen,
            self.glow_color,
            (int(screen_pos.x), int(screen_pos.y)),
            self.radius + 2,
        )

        # Draw inner projectile (smaller, brighter)
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

    def is_expired(self):
        """Projectile expires after lifetime"""
        return self.lifetime <= 0
