"""
Laser Projectile
Fast-moving beam projectile (configurable for different users)
"""

import pygame
from src.entities.projectiles.base_projectile import BaseProjectile


class LaserProjectile(BaseProjectile):
    """Fast laser beam projectile"""

    def __init__(self, x, y, target_position, config):
        """
        Initialize laser projectile

        Args:
            x: Starting x position
            y: Starting y position
            target_position: Target position (Vector2) to aim at
            config: Laser config class (e.g., TankLaserConfig)
        """
        # Calculate direction to target
        direction = target_position - pygame.math.Vector2(x, y)
        if direction.length() > 0:
            direction = direction.normalize()

        super().__init__(
            x,
            y,
            damage=config.LASER_DAMAGE,
            speed=config.LASER_SPEED,
            lifetime=config.LASER_LIFETIME,
        )

        # Movement
        self.direction = direction
        self.velocity = direction * config.LASER_SPEED

        # Visual properties from config
        self.length = config.LASER_LENGTH
        self.width = config.LASER_WIDTH
        self.color = config.LASER_COLOR
        self.glow_color = config.LASER_GLOW_COLOR

        # Beam endpoints
        self.beam_start = pygame.math.Vector2(0, 0)
        self.beam_end = pygame.math.Vector2(0, 0)

        # Calculate actual beam points
        self.update_beam_points()

    def update_beam_points(self):
        """Calculate the start and end points of the laser beam"""
        self.beam_start = self.position - (self.direction * self.length / 2)
        self.beam_end = self.position + (self.direction * self.length / 2)

    def update(self, dt):
        """Update laser position"""
        self._update_movement(dt)
        self.update_beam_points()

    def _update_movement(self, dt):
        """Move laser forward"""
        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))

    def collides_with(self, entity):
        """Check collision using laser beam line"""
        entity_pos = entity.position
        entity_radius = getattr(entity, "radius", 10)

        distance = self._point_to_line_distance(
            entity_pos, self.beam_start, self.beam_end
        )

        return distance <= entity_radius

    def _point_to_line_distance(self, point, line_start, line_end):
        """Calculate shortest distance from point to line segment"""
        line_vec = line_end - line_start
        line_len_sq = line_vec.length_squared()

        if line_len_sq == 0:
            return point.distance_to(line_start)

        point_vec = point - line_start
        t = max(0, min(1, point_vec.dot(line_vec) / line_len_sq))
        closest = line_start + (line_vec * t)

        return point.distance_to(closest)

    def render(self, screen, camera):
        """Render laser beam with glow effect"""
        screen_start = camera.apply(self.beam_start)
        screen_end = camera.apply(self.beam_end)

        # Draw outer glow
        pygame.draw.line(
            screen,
            self.glow_color,
            (int(screen_start.x), int(screen_start.y)),
            (int(screen_end.x), int(screen_end.y)),
            self.width + 2,
        )

        # Draw inner beam
        pygame.draw.line(
            screen,
            self.color,
            (int(screen_start.x), int(screen_start.y)),
            (int(screen_end.x), int(screen_end.y)),
            self.width,
        )

    def is_expired(self):
        """Laser expires after lifetime"""
        return self.lifetime <= 0
