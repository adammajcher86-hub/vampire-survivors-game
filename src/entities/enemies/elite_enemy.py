"""
Elite Enemy
Balanced enemy with high XP value
"""

import pygame
import random
from src.entities.enemies.base_enemy import Enemy
from src.config.enemies.elite_enemy import EliteEnemyConfig
from src.config.common.colors import Colors


class EliteEnemy(Enemy):
    """Elite enemy - balanced stats, high XP reward"""

    def __init__(self, x, y):
        """Initialize elite enemy"""
        super().__init__(x, y, EliteEnemyConfig)

        # Enhanced stats
        self.max_health = 50
        self.health = self.max_health
        self.speed = 100
        self.damage = 15
        self.xp_value = 5

        # Visual
        self.color = (255, 215, 0)  # Gold
        self.size = 35
        self.radius = self.size // 2

        # Dash mechanics - PARAMETERS
        self.dash_probability = 0.9  # 90% chance to have dash ability
        self.dash_speed_multiplier = 5  # 5x normal speed
        self.dash_duration = 0.8  # Fixed duration - always long! ← SINGLE VALUE
        self.dash_cooldown_min = 3.0  # seconds
        self.dash_cooldown_max = 5.0  # seconds
        self.dash_min_distance = self.size * 2  # Don't get closer than 2x size
        # Telegraph (warning blink) - ADJUSTABLE# Telegraph (warning blink)
        self.telegraph_duration = 0.5  # seconds to blink before dash
        self.telegraph_blink_speed = 8.0  # blinks per second

        # Determine if THIS enemy can dash
        self.can_dash = random.random() < self.dash_probability

        # Dash state
        self.is_telegraphing = False
        self.telegraph_timer = 0.0
        self.is_dashing = False
        self.dash_timer = 0.0
        self.invulnerable = False
        self.dash_direction = pygame.math.Vector2(0, 0)
        self.dash_cooldown_timer = random.uniform(
            self.dash_cooldown_min, self.dash_cooldown_max
        )

        # Visual state for blinking
        self.visible = True
        self.blink_timer = 0.0

        # Dash debuff parameters
        self.dash_slow_duration = 2.0  # 2 seconds of slow
        self.dash_slow_strength = 0.5  # 50% speed reduction

    def update(self, dt, player_position):
        """
        Update elite enemy with telegraph and dash ability

        Args:
            dt: Delta time in seconds
            player_position: Vector2 of player position
        """
        distance_to_player = self.position.distance_to(player_position)

        # Update dash cooldown (when not telegraphing or dashing)
        if not self.is_telegraphing and not self.is_dashing and self.can_dash:
            self.dash_cooldown_timer -= dt

        # Check if should start telegraph (warning before dash)
        if (
            self.can_dash
            and not self.is_telegraphing
            and not self.is_dashing
            and self.dash_cooldown_timer <= 0
        ):
            self._start_telegraph(player_position, distance_to_player)

        # Handle telegraph (blinking warning)
        if self.is_telegraphing:
            self.telegraph_timer -= dt

            # Update blink effect
            self.blink_timer += dt
            blink_interval = 1.0 / self.telegraph_blink_speed
            if self.blink_timer >= blink_interval:
                self.visible = not self.visible  # Toggle visibility
                self.blink_timer = 0.0

            # Telegraph finished - start dash!
            if self.telegraph_timer <= 0:
                self.is_telegraphing = False
                self.visible = True  # Make sure visible when dashing
                self.invulnerable = False
                self._start_dash()

        # Handle dashing movement
        elif self.is_dashing:
            self.dash_timer -= dt

            if self.dash_timer <= 0:
                # Dash duration ended
                self.is_dashing = False
                self.dash_cooldown_timer = random.uniform(
                    self.dash_cooldown_min, self.dash_cooldown_max
                )
            else:
                # Continue dash movement
                dash_velocity = (
                    self.dash_direction * self.speed * self.dash_speed_multiplier
                )
                self.position += dash_velocity * dt

        # Normal movement toward player (when not telegraphing or dashing)
        else:
            direction = player_position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * self.speed * dt

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def _start_telegraph(self, player_position, distance_to_player):
        """
        Start telegraph (warning blink) before dash

        Args:
            player_position: Vector2 of player position
            distance_to_player: Current distance to player (not used now)
        """
        self.is_telegraphing = True
        self.telegraph_timer = self.telegraph_duration
        self.visible = True
        self.blink_timer = 0.0
        self.invulnerable = True

        # Calculate dash direction (save for later)
        direction = player_position - self.position
        if direction.length() > 0:
            self.dash_direction = direction.normalize()
        else:
            self.dash_direction = pygame.math.Vector2(0, 0)

    def _start_dash(self):
        """Start the dash (after telegraph)"""
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_hit_player = False

    def render(self, screen, camera, player_position):
        """
        Render elite enemy with blink effect during telegraph

        Args:
            screen: Pygame surface to draw on
            camera: Camera object for world-to-screen conversion
        """
        # Don't draw if blinking (during telegraph)
        if not self.visible:
            return

        # Get screen position
        screen_pos = camera.apply(self.position)

        # Draw enemy circle
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

        # Add visual indicator if telegraphing (about to dash)
        if self.is_telegraphing:
            # Draw warning circle around enemy (pulsing effect)
            warning_radius = self.radius + 10
            pygame.draw.circle(
                screen,
                (255, 0, 0),  # Red warning
                (int(screen_pos.x), int(screen_pos.y)),
                warning_radius,
                3,  # Line width
            )

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

    def take_damage(self, damage):
        """
        Take damage (immune during telegraph)

        Args:
            damage: Amount of damage to take

        Returns:
            bool: True if enemy died
        """
        # Immune during telegraph!
        if self.invulnerable:
            return False

        # Normal damage
        return super().take_damage(damage)
