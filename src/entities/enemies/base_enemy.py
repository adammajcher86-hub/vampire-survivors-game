"""
Base Enemy Entity
Base class for all enemy types with common behavior
"""

import pygame
from src.config import Colors


class Enemy(pygame.sprite.Sprite):
    """Base enemy class - all enemies inherit from this"""

    def __init__(self, x, y, config):
        """
        Initialize enemy with configuration

        Args:
            x: Initial x position
            y: Initial y position
            config: Enemy configuration class (BaseEnemyConfig, FastEnemyConfig, etc.)
        """
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        # Stats from config
        self.max_health = config.HEALTH
        self.health = self.max_health
        self.speed = config.SPEED
        self.contact_damage = config.CONTACT_DAMAGE
        self.xp_value = config.XP_VALUE

        # Visual properties from config
        self.size = config.SIZE
        self.color = config.COLOR
        self.radius = config.SIZE // 2

        # For sprite collision
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

        # State
        self.is_dead = False

    def update(self, dt, player_position):
        """
        Update enemy state

        Args:
            dt: Delta time in seconds
            player_position: Vector2 of player position
        """
        if self.is_dead:
            return

        # Calculate direction to player
        direction = player_position - self.position
        if direction.length() > 0:
            direction = direction.normalize()

        # Move towards player
        self.velocity = direction * self.speed
        self.position += self.velocity * dt

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def take_damage(self, damage):
        """
        Take damage from player weapons

        Args:
            damage: Amount of damage to take

        Returns:
            bool: True if enemy died from this damage
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            return True
        return False

    def get_xp_value(self):
        """Get XP value for this enemy"""
        return self.xp_value

    def collides_with(self, other):
        """
        Check collision with another entity

        Args:
            other: Entity to check collision with

        Returns:
            bool: True if colliding
        """
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)

    def render(self, screen, camera):
        """
        Draw the enemy

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        if self.is_dead:
            return

        screen_pos = camera.apply(self.position)

        # Draw enemy as a circle
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

        # Draw health bar
        self._draw_health_bar(screen, screen_pos)

    def _draw_health_bar(self, screen, screen_pos):
        """Draw health bar above enemy"""
        if self.health >= self.max_health:
            return  # Don't show full health bar

        bar_width = self.size
        bar_height = 4
        bar_x = screen_pos.x - bar_width // 2
        bar_y = screen_pos.y - self.radius - 10

        # Background (red)
        pygame.draw.rect(screen, Colors.RED, (bar_x, bar_y, bar_width, bar_height))

        # Foreground (green) - current health
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, Colors.GREEN, (bar_x, bar_y, health_width, bar_height))
