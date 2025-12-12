"""
Particle System
Manages all particles in the game
"""

import random
import math
from .particle import Particle


class ParticleSystem:
    """Manages particle effects"""

    def __init__(self):
        """Initialize particle system"""
        self.particles = []

    def update(self, dt):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update(dt)]

    def render(self, screen, camera):
        """Render all particles"""
        for particle in self.particles:
            particle.render(screen, camera)

    def emit_explosion(
        self, x, y, count=20, color=(255, 100, 0), speed=200, size=4, lifetime=0.8
    ):
        """
        Create explosion effect

        Args:
            x, y: Center position
            count: Number of particles
            color: RGB tuple
            speed: Base particle speed
            size: Particle size
            lifetime: How long particles live
        """
        for _ in range(count):
            # Random angle
            angle = random.uniform(0, math.pi * 2)

            # Random speed
            particle_speed = random.uniform(speed * 0.5, speed * 1.5)

            # Calculate velocity
            vx = math.cos(angle) * particle_speed
            vy = math.sin(angle) * particle_speed

            # Vary color slightly
            varied_color = (
                min(255, color[0] + random.randint(-30, 30)),
                min(255, color[1] + random.randint(-30, 30)),
                min(255, color[2] + random.randint(-30, 30)),
            )

            # Create particle
            particle = Particle(
                x,
                y,
                vx,
                vy,
                varied_color,
                random.uniform(size * 0.7, size * 1.3),
                random.uniform(lifetime * 0.8, lifetime * 1.2),
            )

            self.particles.append(particle)

    def emit_impact(self, x, y, direction, count=8, color=(255, 255, 100)):
        """
        Create impact/hit effect

        Args:
            x, y: Impact position
            direction: Vector2 - direction of impact
            count: Number of particles
            color: RGB tuple
        """
        # Normalize direction
        if direction.length() > 0:
            direction = direction.normalize()

        for _ in range(count):
            # Spread around impact direction
            angle_offset = random.uniform(-math.pi / 3, math.pi / 3)
            angle = math.atan2(direction.y, direction.x) + angle_offset

            speed = random.uniform(100, 300)

            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            particle = Particle(
                x, y, vx, vy, color, random.uniform(2, 4), random.uniform(0.3, 0.6)
            )

            self.particles.append(particle)

    def emit_death(self, x, y, enemy_color=(200, 50, 50)):
        """
        Create enemy death effect

        Args:
            x, y: Death position
            enemy_color: Color based on enemy type
        """
        self.emit_explosion(
            x, y, count=30, color=enemy_color, speed=250, size=5, lifetime=1.0
        )

    def emit_laser_hit(self, x, y):
        """
        Create laser hit effect

        Args:
            x, y: Hit position
        """
        self.emit_explosion(
            x, y, count=5, color=(255, 100, 100), speed=100, size=3, lifetime=0.3
        )

    def emit_trail(self, x, y, velocity, color=(255, 200, 0)):
        """
        Create trail particle (for projectiles, etc.)

        Args:
            x, y: Trail position
            velocity: Vector2 - object velocity
            color: RGB tuple
        """
        # Create particle moving opposite to velocity
        vx = -velocity.x * 0.3 + random.uniform(-20, 20)
        vy = -velocity.y * 0.3 + random.uniform(-20, 20)

        particle = Particle(
            x, y, vx, vy, color, random.uniform(2, 3), random.uniform(0.2, 0.4)
        )

        self.particles.append(particle)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()

    def get_particle_count(self):
        """Get number of active particles"""
        return len(self.particles)
