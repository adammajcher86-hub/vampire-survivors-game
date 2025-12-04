"""
Bomb Projectile
Delayed explosion that damages all entities in radius (including player!)
"""

import pygame
import math
from src.entities.projectiles.base_projectile import BaseProjectile
from src.config.weapons.bomb import BombConfig


class BombProjectile(BaseProjectile):
    """Bomb projectile with delayed explosion"""

    def __init__(self, x, y):
        """
        Initialize bomb projectile

        Args:
            x: Starting x position
            y: Starting y position
        """
        super().__init__(
            x,
            y,
            damage=BombConfig.EXPLOSION_DAMAGE,
            speed=0,
            lifetime=BombConfig.EXPLOSION_DELAY,
        )

        # Explosion parameters from config
        self.explosion_radius = BombConfig.EXPLOSION_RADIUS
        self.delay = BombConfig.EXPLOSION_DELAY
        self.timer = self.delay

        # Visual from config
        self.radius = BombConfig.BOMB_SIZE
        self.color = BombConfig.BOMB_COLOR
        self.warning_color = BombConfig.WARNING_COLOR
        self.pulse_speed = BombConfig.PULSE_SPEED

        # State
        self.has_exploded = False

    def update(self, dt):
        """Update bomb timer"""
        self.timer -= dt

        if self.timer <= 0 and not self.has_exploded:
            self.has_exploded = True

    def _update_movement(self, dt):
        """Bombs don't move"""
        pass

    def collides_with(self, entity):
        """Bombs don't use collision (AOE instead)"""
        return False

    def is_expired(self):
        """Bomb expires after explosion"""
        return self.has_exploded

    def render(self, screen, camera):
        """Render bomb with pulsing warning circle"""
        screen_pos = camera.apply(self.position)

        # Draw bomb body
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

        # Draw pulsing warning circle
        pulse = math.sin(self.timer * 8) * 0.3 + 0.7
        warning_radius = int(self.explosion_radius * pulse)

        # Draw warning circles
        for i in range(3):
            radius_offset = i * 5
            pygame.draw.circle(
                screen,
                self.warning_color,
                (int(screen_pos.x), int(screen_pos.y)),
                warning_radius + radius_offset,
                2,
            )

    def get_explosion_data(self):
        print(f"💥 Explosion radius: {self.explosion_radius}px")
        """Get explosion data for damage calculation"""
        return {
            "position": self.position,
            "radius": self.explosion_radius,
            "damage": self.damage,
        }
