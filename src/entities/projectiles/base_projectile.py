"""
Base Projectile
Abstract base class for all projectiles with polymorphism
"""

import pygame
from abc import ABC, abstractmethod


class BaseProjectile(pygame.sprite.Sprite, ABC):
    """Base class for all projectiles"""

    def __init__(self, x, y, damage, speed, lifetime=2.0):
        """
        Initialize base projectile

        Args:
            x: Starting x position
            y: Starting y position
            damage: Damage dealt on hit
            speed: Projectile speed
            lifetime: Time before projectile expires (seconds)
        """
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.damage = damage
        self.speed = speed

        # Lifetime
        self.lifetime = lifetime
        self.age = 0.0

        # Collision radius (set by subclass)
        self.radius = 0

        # For sprite collision
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.rect.center = (int(self.position.x), int(self.position.y))

    def update(self, dt):
        """
        Update projectile state - calls subclass movement

        Args:
            dt: Delta time in seconds
        """
        # Update movement (implemented by subclass)
        self._update_movement(dt)

        # Update age
        self.age += dt

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    @abstractmethod
    def _update_movement(self, dt):
        """
        Update projectile movement - MUST be implemented by subclass

        Args:
            dt: Delta time in seconds
        """
        pass

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

    @abstractmethod
    def render(self, screen, camera):
        """
        Draw the projectile - MUST be implemented by subclass

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        pass
