"""
Player Entity
The main character controlled by the player
"""

import pygame
from src.config import PlayerConfig, Colors


class Player(pygame.sprite.Sprite):
    """Player character"""

    def __init__(self, x, y):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        # Stats
        self.max_health = PlayerConfig.MAX_HEALTH
        self.health = self.max_health
        self.speed = PlayerConfig.SPEED
        self.health_regen = PlayerConfig.HEALTH_REGEN

        # Visual properties
        self.size = PlayerConfig.SIZE
        self.color = PlayerConfig.COLOR
        self.radius = PlayerConfig.get_radius()

        # For sprite collision
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

    def update(self, dt, dx, dy):
        """Update player state"""
        # Movement
        if dx != 0 or dy != 0:
            # Normalize diagonal movement
            direction = pygame.math.Vector2(dx, dy)
            if direction.length() > 0:
                direction = direction.normalize()

            self.velocity = direction * self.speed
            self.position += self.velocity * dt
        else:
            self.velocity = pygame.math.Vector2(0, 0)

        # Health regeneration
        self.health = min(self.max_health, self.health + self.health_regen * dt)

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def take_damage(self, damage):
        """Take damage from enemies"""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.max_health, self.health + amount)

    def is_alive(self):
        """Check if player is still alive"""
        return self.health > 0

    def render(self, screen, camera):
        """Draw the player"""
        screen_pos = camera.apply(self.position)

        # Draw player as a circle
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

        # Draw directional indicator
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()
            end_pos = screen_pos + direction * (self.radius + 10)
            pygame.draw.line(
                screen,
                Colors.WHITE,
                (int(screen_pos.x), int(screen_pos.y)),
                (int(end_pos.x), int(end_pos.y)),
                3,
            )
