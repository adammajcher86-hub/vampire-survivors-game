"""
Laser Beam
Instant beam that deals continuous damage
"""

import pygame


class LaserBeam:
    """Represents an active laser beam"""

    def __init__(
        self, start_pos, end_pos, damage_per_second, color=(255, 0, 0), width=3
    ):
        """
        Initialize laser beam

        Args:
            start_pos: Vector2 - weapon tip position
            end_pos: Vector2 - target position
            damage_per_second: Damage dealt per second
            color: RGB tuple
            width: Beam thickness
        """
        self.start_pos = pygame.math.Vector2(start_pos)
        self.end_pos = pygame.math.Vector2(end_pos)
        self.damage_per_second = damage_per_second
        self.color = color
        self.width = width

        # Beam duration
        self.lifetime = 0.1  # Visual beam lasts 0.1 seconds
        self.age = 0.0

    def update(self, dt):
        """Update beam age"""
        self.age += dt
        return self.is_alive()

    def is_alive(self):
        """Check if beam should still be rendered"""
        return self.age < self.lifetime

    def render(self, screen, camera):
        """
        Render laser beam

        Args:
            screen: Pygame surface
            camera: Camera for world-to-screen conversion
        """
        # Convert to screen coordinates
        start_screen = camera.apply(self.start_pos)
        end_screen = camera.apply(self.end_pos)

        # Calculate alpha based on age (fade out)
        alpha = int(255 * (1.0 - self.age / self.lifetime))

        # Draw main beam
        # color_with_alpha = (*self.color, alpha)

        # Draw glow (thicker, semi-transparent)
        glow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.line(
            glow_surface,
            (*self.color, alpha // 3),
            (int(start_screen.x), int(start_screen.y)),
            (int(end_screen.x), int(end_screen.y)),
            self.width * 3,
        )
        screen.blit(glow_surface, (0, 0))

        # Draw core beam (brighter)
        pygame.draw.line(
            screen,
            self.color,
            (int(start_screen.x), int(start_screen.y)),
            (int(end_screen.x), int(end_screen.y)),
            self.width,
        )
