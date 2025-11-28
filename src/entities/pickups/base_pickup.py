"""
Base Pickup
Abstract base class for all pickups (XP, health, powerups, etc.)
"""

import pygame
from abc import ABC, abstractmethod


class BasePickup(pygame.sprite.Sprite, ABC):
    """Base class for all pickups"""

    def __init__(self, x, y, radius=8):
        """
        Initialize base pickup

        Args:
            x: Starting x position
            y: Starting y position
            radius: Pickup collision radius
        """
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius

        # For sprite collision
        self.rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        self.rect.center = (int(self.position.x), int(self.position.y))

    @abstractmethod
    def update(self, dt, player):
        """
        Update pickup state - MUST be implemented by subclass

        Args:
            dt: Delta time in seconds
            player: Player entity
        """
        pass

    @abstractmethod
    def render(self, screen, camera):
        """
        Draw the pickup - MUST be implemented by subclass

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        pass

    @abstractmethod
    def on_collect(self, player):
        """
        Called when player collects this pickup - MUST be implemented by subclass

        Args:
            player: Player entity

        Returns:
            Any value the pickup provides (XP amount, heal amount, etc.)
        """
        pass

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
