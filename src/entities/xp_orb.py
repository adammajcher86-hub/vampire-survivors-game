"""
XP Orb Entity
Experience orbs dropped by enemies
"""

import pygame
from src.config import Colors, GameConfig


class XPOrb(pygame.sprite.Sprite):
    """Experience orb that can be collected by the player"""

    def __init__(self, x, y, xp_value):
        """
        Initialize XP orb

        Args:
            x: Initial x position
            y: Initial y position
            xp_value: Amount of XP this orb gives
        """
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.xp_value = xp_value

        # Visual properties
        self.size = 8
        self.radius = self.size // 2
        self.color = Colors.CYAN

        # Animation (pulse effect)
        self.pulse_timer = 0.0
        self.pulse_speed = 3.0

        # For sprite collision
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

        # Collection range (will move toward player when close)
        self.collection_range = GameConfig.PICKUP_RANGE
        self.magnetic = False
        self.magnetic_speed = 200

    def update(self, dt, player):
        """
        Update XP orb state with acceleration

        Args:
            dt: Delta time in seconds
            player: Player entity (to get position and pickup range)
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

    def collides_with(self, entity):
        """
        Check collision with an entity (player)

        Args:
            entity: Entity to check collision with

        Returns:
            bool: True if colliding
        """
        distance = self.position.distance_to(entity.position)
        return distance < (self.radius + entity.radius)

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

        # Draw outer glow (semi-transparent)
        glow_surface = pygame.Surface(
            (pulse_radius * 4, pulse_radius * 4), pygame.SRCALPHA
        )
        pygame.draw.circle(
            glow_surface,
            (*self.color, 50),  # Semi-transparent cyan
            (pulse_radius * 2, pulse_radius * 2),
            pulse_radius * 2,
        )
        screen.blit(
            glow_surface,
            (screen_pos.x - pulse_radius * 2, screen_pos.y - pulse_radius * 2),
        )

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
