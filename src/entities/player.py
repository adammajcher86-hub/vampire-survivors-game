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
        self.attack_speed_multiplier = 1.0
        self.hp_regen = 0.5

        # Visual properties
        self.size = PlayerConfig.SIZE
        self.color = PlayerConfig.COLOR
        self.radius = PlayerConfig.get_radius()

        # For sprite collision
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.xp_pickup_range = 50.0

        self.max_stamina = 100.0
        self.stamina = 30
        self.stamina_regen = 5.0  # per second

        # Dash mechanics - NEW!
        self.dash_cost = 30.0
        self.dash_speed = 800.0  # Much faster than normal speed
        self.dash_duration = 0.2  # 0.2 seconds
        self.dash_cooldown_time = 0.5  # Can dash again after 0.5 sec

        # Dash state
        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.dash_direction = pygame.math.Vector2(0, 0)
        self.invulnerable = False  # Brief invincibility during dash

    def update(self, dt, dx, dy):
        """Update player state"""

        # Update dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt

        # Handle dashing
        if self.is_dashing:
            self.dash_timer -= dt

            if self.dash_timer <= 0:
                # Dash ended
                self.is_dashing = False
                self.invulnerable = False
                self.dash_cooldown = self.dash_cooldown_time
                self.velocity = pygame.math.Vector2(0, 0)
            else:
                # Continue dash movement
                self.velocity = self.dash_direction * self.dash_speed
                self.position += self.velocity * dt
        else:
            # Normal movement
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
        if self.hp_regen > 0:
            self.health = min(self.health + self.hp_regen * dt, self.max_health)

        # Stamina regeneration
        self.stamina = min(self.stamina + self.stamina_regen * dt, self.max_stamina)

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


    def try_dash(self, dx, dy):
        """
        Attempt to dash in direction

        Args:
            dx: X direction (-1, 0, 1)
            dy: Y direction (-1, 0, 1)

        Returns:
            bool: True if dash started
        """
        # Can't dash if already dashing or on cooldown
        if self.is_dashing or self.dash_cooldown > 0:
            return False

        # Need stamina
        if self.stamina < self.dash_cost:
            return False

        # Need a direction
        if dx == 0 and dy == 0:
            return False

        # Start dash!
        self.stamina -= self.dash_cost
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.invulnerable = True

        # Normalize dash direction
        self.dash_direction = pygame.math.Vector2(dx, dy)
        if self.dash_direction.length() > 0:
            self.dash_direction = self.dash_direction.normalize()

        return True