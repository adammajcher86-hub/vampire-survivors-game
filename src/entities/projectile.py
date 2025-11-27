"""
Projectile Entity
Bullets/projectiles fired by weapons
"""

import pygame
from src.config import BaseWeaponConfig


class Projectile(pygame.sprite.Sprite):
    """Projectile fired from weapons"""

    def __init__(
        self, x, y, target_pos, damage=None, speed=None, color=None, size=None
    ):
        """
        Initialize projectile

        Args:
            x: Starting x position
            y: Starting y position
            target_pos: Vector2 of target position (for direction)
            damage: Damage dealt (default from config)
            speed: Projectile speed (default from config)
            color: Projectile color (default from config)
            size: Projectile size (default from config)
        """
        super().__init__()
        self.position = pygame.math.Vector2(x, y)

        # Calculate direction to target
        direction = pygame.math.Vector2(target_pos.x - x, target_pos.y - y)
        if direction.length() > 0:
            direction = direction.normalize()

        # Properties
        self.damage = (
            damage if damage is not None else BaseWeaponConfig.PROJECTILE_DAMAGE
        )
        self.speed = speed if speed is not None else BaseWeaponConfig.PROJECTILE_SPEED
        self.color = color if color is not None else BaseWeaponConfig.PROJECTILE_COLOR
        self.size = size if size is not None else BaseWeaponConfig.PROJECTILE_SIZE
        self.radius = self.size // 2

        # Movement
        self.velocity = direction * self.speed

        # Lifetime
        self.lifetime = BaseWeaponConfig.PROJECTILE_LIFETIME
        self.age = 0.0

        # For sprite collision
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

    def update(self, dt):
        """Update projectile state"""
        # Move
        self.position += self.velocity * dt

        # Update age
        self.age += dt

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def is_expired(self):
        """Check if projectile has expired"""
        return self.age >= self.lifetime

    def collides_with(self, entity):
        """
        Check collision with an entity

        Args:
            entity: Entity to check collision with

        Returns:
            bool: True if colliding
        """
        distance = self.position.distance_to(entity.position)
        return distance < (self.radius + entity.radius)

    def render(self, screen, camera):
        """
        Draw the projectile

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        screen_pos = camera.apply(self.position)

        # Draw projectile as a circle
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )
