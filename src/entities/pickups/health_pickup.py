"""
Health Pickup
Red heart that heals the player
"""

import pygame
import math
from src.entities.pickups.base_pickup import BasePickup
from src.config import Colors


class HealthPickup(BasePickup):
    """Health pickup that heals player on collection"""

    def __init__(self, x, y, heal_amount=20):
        """
        Initialize health pickup

        Args:
            x: Starting x position
            y: Starting y position
            heal_amount: Amount of HP restored
        """
        super().__init__(x, y, radius=10)

        # Heal value
        self.heal_amount = heal_amount

        # Visual properties
        self.color = Colors.RED

        # Animation
        self.pulse_timer = 0.0
        self.pulse_speed = 4.0

    def update(self, dt, player):
        """
        Update health pickup (no chasing, just sits there)

        Args:
            dt: Delta time in seconds
            player: Player entity
        """
        # Update pulse animation
        self.pulse_timer += dt * self.pulse_speed

        # Health pickups don't chase - they just sit there!
        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def render(self, screen, camera):
        """
        Draw the health pickup as a red heart/cross

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        screen_pos = camera.apply(self.position)

        # Pulsing size effect
        pulse = math.sin(self.pulse_timer) * 0.2 + 1.0
        render_radius = int(self.radius * pulse)

        # Draw as red circle (or you can make it a cross/heart later)
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), render_radius
        )

        # Draw white center
        pygame.draw.circle(
            screen,
            Colors.WHITE,
            (int(screen_pos.x), int(screen_pos.y)),
            max(3, render_radius - 3),
        )

    def on_collect(self, player):
        """
        Called when player collects this health pickup

        Args:
            player: Player entity

        Returns:
            int: Heal amount given to player
        """
        player.heal(self.heal_amount)
        return self.heal_amount
