"""
XP Orb Pickup
Green orb that gives XP and chases the player
"""

import pygame
from src.entities.pickups.base_pickup import BasePickup
from src.config import Colors


class XPOrb(BasePickup):
    """XP orb that chases player and gives XP on collection"""

    def __init__(self, x, y, xp_value=1):
        """
        Initialize XP orb

        Args:
            x: Starting x position
            y: Starting y position
            xp_value: Amount of XP this orb gives
        """
        super().__init__(x, y, radius=8)

        # XP value
        self.xp_value = xp_value

        # Visual properties
        self.color = Colors.CYAN

        # Animation
        self.pulse_timer = 0.0
        self.pulse_speed = 3.0

        # Movement
        self.magnetic_speed = 200.0

    def update(self, dt, player):
        """
        Update XP orb with acceleration toward player

        Args:
            dt: Delta time in seconds
            player: Player entity
        """
        # Update pulse animation
        self.pulse_timer += dt * self.pulse_speed

        # Check if player is close enough for magnetic pull
        distance = self.position.distance_to(player.position)

        # Chase at 2x the pickup range
        chase_distance = player.xp_pickup_range * 2

        if distance < chase_distance:
            # Calculate acceleration based on distance
            # Closer = faster! (1x at edge, up to 5x when very close)
            distance_ratio = distance / chase_distance  # 1.0 at edge, 0.0 at center
            speed_multiplier = 1.0 + (4.0 * (1.0 - distance_ratio))  # 1x to 5x

            current_speed = self.magnetic_speed * speed_multiplier

            # Move toward player with accelerating speed
            direction = player.position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * current_speed * dt

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def render(self, screen, camera):
        """
        Draw the XP orb with pulse effect

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        screen_pos = camera.apply(self.position)

        # Calculate pulse size (oscillates between 0.8 and 1.2)
        pulse_scale = (
            1.0 + 0.2 * pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 180).x
        )
        pulse_radius = int(self.radius * pulse_scale)

        # Draw main orb
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), pulse_radius
        )

        # Draw white center
        pygame.draw.circle(
            screen,
            Colors.WHITE,
            (int(screen_pos.x), int(screen_pos.y)),
            max(1, pulse_radius // 2),
        )

    def on_collect(self, player):
        """
        Called when player collects this orb

        Args:
            player: Player entity

        Returns:
            int: XP value given to player
        """
        return self.xp_value
