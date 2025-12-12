"""
Particle
Individual particle for visual effects
"""

import pygame


class Particle:
    """Single particle with physics and rendering"""

    def __init__(self, x, y, velocity_x, velocity_y, color, size, lifetime):
        """
        Initialize particle

        Args:
            x, y: Starting position
            velocity_x, velocity_y: Initial velocity
            color: RGB tuple
            size: Particle radius
            lifetime: How long particle lives (seconds)
        """
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y)
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0.0
        self.gravity = 200.0  # Pixels per second^2

    def update(self, dt):
        """
        Update particle physics

        Args:
            dt: Delta time

        Returns:
            bool: True if particle is still alive
        """
        self.age += dt

        # Apply velocity
        self.position += self.velocity * dt

        # Apply gravity
        self.velocity.y += self.gravity * dt

        # Apply drag
        self.velocity *= 0.98

        return self.age < self.lifetime

    def render(self, screen, camera):
        """
        Render particle

        Args:
            screen: Pygame surface
            camera: Camera for world-to-screen
        """
        if self.age >= self.lifetime:
            return

        # Calculate alpha based on age (fade out)
        alpha = max(0, min(255, int(255 * (1.0 - self.age / self.lifetime))))

        # Convert to screen space
        screen_pos = camera.apply(self.position)

        # Calculate size (shrink over time)
        current_size = max(1, int(self.size * (1.0 - self.age / self.lifetime)))

        r = max(0, min(255, int(self.color[0])))
        g = max(0, min(255, int(self.color[1])))
        b = max(0, min(255, int(self.color[2])))

        # Create temporary surface with alpha
        particle_surface = pygame.Surface(
            (current_size * 2, current_size * 2), pygame.SRCALPHA
        )

        # Draw circle with validated RGBA color
        color_with_alpha = (r, g, b, alpha)

        try:
            pygame.draw.circle(
                particle_surface,
                color_with_alpha,
                (current_size, current_size),
                current_size,
            )

            # Blit to screen
            screen.blit(
                particle_surface,
                (int(screen_pos.x - current_size), int(screen_pos.y - current_size)),
            )
        except (ValueError, TypeError):
            # Debug: print what went wrong
            print(
                f"⚠️ Particle render error: color={self.color}, alpha={alpha}, size={current_size}"
            )
            pass  # Skip this particle if it fails
