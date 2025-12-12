"""
Effect Manager
Coordinates all visual effects (particles, screen shake, etc.)
"""

from .particle_system import ParticleSystem
from .screen_shake import ScreenShake


class EffectManager:
    """Manages all visual effects"""

    def __init__(self):
        """Initialize effect manager"""
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()

    def update(self, dt):
        """
        Update all effects

        Args:
            dt: Delta time
        """
        self.particle_system.update(dt)
        self.screen_shake.update(dt)

    def render(self, screen, camera):
        """
        Render all effects

        Args:
            screen: Pygame surface
            camera: Camera for world-to-screen
        """
        self.particle_system.render(screen, camera)

    # Convenience methods for common effects

    def enemy_death(self, position, enemy_type="BasicEnemy"):
        """
        Trigger enemy death effects

        Args:
            position: Vector2 death position
            enemy_type: Enemy class name for color
        """
        # Color based on enemy type
        colors = {
            "BasicEnemy": (200, 50, 50),
            "FastEnemy": (50, 200, 50),
            "TankEnemy": (100, 100, 200),
            "EliteEnemy": (200, 50, 200),
        }
        color = colors.get(enemy_type, (200, 50, 50))

        # Particle explosion
        self.particle_system.emit_death(position.x, position.y, color)

        # Small screen shake
        self.screen_shake.add_trauma(0.2)

    def projectile_hit(self, position, direction):
        """
        Trigger projectile hit effects

        Args:
            position: Vector2 hit position
            direction: Vector2 projectile direction
        """
        # Impact particles
        self.particle_system.emit_impact(
            position.x, position.y, direction, count=8, color=(255, 255, 100)
        )

    def laser_hit(self, position):
        """
        Trigger laser hit effects

        Args:
            position: Vector2 hit position
        """
        self.particle_system.emit_laser_hit(position.x, position.y)

    def bomb_explosion(self, position):
        """
        Trigger bomb explosion effects

        Args:
            position: Vector2 explosion center
        """
        # Large explosion
        self.particle_system.emit_explosion(
            position.x,
            position.y,
            count=50,
            color=(255, 150, 0),
            speed=300,
            size=6,
            lifetime=1.2,
        )

        # Big screen shake
        self.screen_shake.add_trauma(0.8)

    def player_damage(self):
        """Trigger player damage effects"""
        # Medium screen shake
        self.screen_shake.add_trauma(0.4)

    def level_up(self, position):
        """
        Trigger level up effects

        Args:
            position: Vector2 player position
        """
        # Golden particles
        self.particle_system.emit_explosion(
            position.x,
            position.y,
            count=40,
            color=(255, 215, 0),
            speed=200,
            size=5,
            lifetime=1.5,
        )

    def get_shake_offset(self):
        """
        Get current screen shake offset

        Returns:
            tuple: (offset_x, offset_y)
        """
        return self.screen_shake.get_offset()

    def clear(self):
        """Clear all effects"""
        self.particle_system.clear()
        self.screen_shake.trauma = 0.0
