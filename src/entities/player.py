"""
Player Entity
The main character controlled by the player
"""

import pygame
from src.config import PlayerConfig, Colors
from src.config.weapons.bomb import BombConfig
from src.entities.projectiles import BombProjectile
import random

from src.logger import logger


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

        # Dash mechanics
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
        # Debuffs
        self.is_slowed = False
        self.slow_timer = 0.0
        self.slow_multiplier = 1.0  # 1.0 = normal speed, 0.5 = 50% speed
        # Bombs
        self.bomb_count = BombConfig.STARTING_BOMBS
        self.max_bombs = BombConfig.MAX_BOMBS
        self.bomb_cooldown = BombConfig.PLACEMENT_COOLDOWN
        # Damage invulnerability
        self.damage_immunity = False
        self.damage_immunity_timer = 0.0
        self.damage_immunity_duration = (
            0.2  # 0.2 seconds after taking damage, not working for over time damage
        )

    def update(self, dt, dx, dy):
        """Update player state"""
        # Update debuff timers
        if self.is_slowed:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.is_slowed = False
                self.slow_multiplier = 1.0
                logger.info("✅ Slow effect ended!")

        if self.damage_immunity:
            self.damage_immunity_timer -= dt
            if self.damage_immunity_timer <= 0:
                self.damage_immunity = False

        # Update bomb cooldown
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= dt

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

                current_speed = self.speed * self.slow_multiplier
                self.velocity = direction * current_speed
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
        """
        Take damage (contact/continuous damage - no immunity frames)

        Args:
            damage: Amount of damage to take

        Returns:
            bool: True if player died
        """
        # Only skip if invulnerable (dash)
        if self.invulnerable:
            return False

        self.health -= damage

        # Check for death
        if self.health <= 0:
            self.health = 0
            from src.logger import logger

            logger.info("💀 Player died!")
            return True

        return False

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

    def apply_slow(self, duration, strength):
        """
        Apply movement slow debuff

        Args:
            duration: How long to slow (seconds)
            strength: Speed multiplier (0.5 = 50% speed)
        """
        self.is_slowed = True
        self.slow_timer = duration
        self.slow_multiplier = strength
        logger.info(
            f"⚠️ SLOWED! Speed reduced to {int(strength * 100)}% for {duration}s"
        )

    def can_place_bomb(self):
        """Check if player has bombs to place"""
        return self.bomb_count > 0

    def use_bomb(self):
        """
        Use one bomb (decrease count)

        Returns:
            bool: True if bomb was used
        """
        if self.bomb_count > 0:
            self.bomb_count -= 1
            logger.info(f"💣 Bomb placed! Remaining: {self.bomb_count}")
            return True
        else:
            logger.info("⚠️ No bombs remaining!")
            return False

    def add_bombs(self, amount):
        """
        Add bombs to inventory

        Args:
            amount: Number of bombs to add
        """
        old_count = self.bomb_count
        self.bomb_count = min(self.bomb_count + amount, self.max_bombs)
        added = self.bomb_count - old_count
        if added > 0:
            logger.info(f"💣 +{added} bomb(s)! Total: {self.bomb_count}")

    def place_bomb(self, projectiles):
        """
        Place a bomb near player's position

        Args:
            projectiles: Sprite group to add bomb to

        Returns:
            bool: True if bomb was placed
        """

        # Check cooldown
        if self.bomb_cooldown > 0:
            logger.info(f"⏱️ Bomb on cooldown! {self.bomb_cooldown:.1f}s remaining")
            return False

        # Check bomb count
        if self.bomb_count <= 0:
            logger.info("⚠️ No bombs remaining!")
            return False

        # Calculate position
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)
        bomb_x = self.position.x + offset_x
        bomb_y = self.position.y + offset_y

        # Create bomb
        bomb = BombProjectile(bomb_x, bomb_y)
        projectiles.add(bomb)

        # Decrease bomb count and start cooldown
        self.bomb_count -= 1
        self.bomb_cooldown = BombConfig.PLACEMENT_COOLDOWN  # ✅ Start cooldown!
        logger.info(f"💣 Bomb placed! Remaining: {self.bomb_count}")

        return True

    def take_projectile_damage(self, damage):
        """
        Take damage from projectile with immunity frames

        Args:
            damage: Amount of damage to take

        Returns:
            bool: True if damage was applied
        """
        # Skip if invulnerable (dash) or damage immunity
        if self.invulnerable or self.damage_immunity:
            return False

        self.health -= damage

        # Start damage immunity period (prevents multi-hit from projectiles)
        self.damage_immunity = True
        self.damage_immunity_timer = self.damage_immunity_duration

        # Check for death
        if self.health <= 0:
            self.health = 0

            logger.info("💀 Player died!")
            return True

        return True
