"""
Tank Enemy
Slow, high-health enemy that deals heavy damage
"""

import pygame
import random
from src.entities.enemies.base_enemy import Enemy
from src.config.enemies.tank_enemy import TankEnemyConfig
from src.config.enemies.tank_laser import TankLaserConfig
from src.config.common.colors import Colors


class TankEnemy(Enemy):
    """Tank enemy - low speed, high health and damage"""

    def __init__(self, x, y):
        """Initialize tank enemy"""
        super().__init__(x, y, TankEnemyConfig)

        # Stats
        self.max_health = 30
        self.health = self.max_health
        self.speed = 50
        self.damage = 10
        self.xp_value = 3

        # Visual
        self.color = (150, 150, 255)  # Blue
        self.size = 30
        self.radius = self.size // 2

        # Shooting state - NEW!
        self.can_shoot = True
        self.shoot_cooldown = random.uniform(
            TankLaserConfig.SHOOT_COOLDOWN_MIN, TankLaserConfig.SHOOT_COOLDOWN_MAX
        )
        self.is_telegraphing = False
        self.telegraph_timer = 0.0
        self.target_position = None  # Saved player position for shot

        # Visual state
        self.flash_color = (255, 100, 100)  # Red flash when telegraphing

    def update(self, dt, player_position):
        """
        Update tank enemy with shooting behavior

        Args:
            dt: Delta time in seconds
            player_position: Vector2 of player position
        """
        # distance_to_player = self.position.distance_to(player_position)

        # Update shoot cooldown
        if not self.is_telegraphing and self.can_shoot:
            self.shoot_cooldown -= dt

        # Check if should start telegraph (warning before shooting)
        if self.can_shoot and not self.is_telegraphing and self.shoot_cooldown <= 0:
            # Only shoot if player within range
            # if distance_to_player < TankLaserConfig.SHOOT_RANGE:
            self._start_telegraph(player_position)

        # Handle telegraph (warning flash)
        if self.is_telegraphing:
            self.telegraph_timer -= dt

            if self.telegraph_timer <= 0:
                # Telegraph finished - ready to shoot!
                self.is_telegraphing = False
                self.ready_to_shoot = True  # Flag for game_engine to spawn laser

        # Normal movement toward player
        if not self.is_telegraphing:
            direction = player_position - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * self.speed * dt

        # Update rect for collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def _start_telegraph(self, player_position):
        """Start telegraph warning before shooting"""
        self.is_telegraphing = True
        self.telegraph_timer = TankLaserConfig.TELEGRAPH_DURATION
        self.target_position = pygame.math.Vector2(player_position.x, player_position.y)
        self.ready_to_shoot = False

    def should_shoot(self):
        """Check if tank is ready to shoot"""
        return hasattr(self, "ready_to_shoot") and self.ready_to_shoot

    def get_shot_data(self):
        """Get data for creating laser shot"""
        return {"position": self.position.copy(), "target": self.target_position.copy()}

    def reset_shoot_state(self):
        """Reset shooting state after shot is fired"""
        self.ready_to_shoot = False
        self.shoot_cooldown = random.uniform(
            TankLaserConfig.SHOOT_COOLDOWN_MIN, TankLaserConfig.SHOOT_COOLDOWN_MAX
        )

    def render(self, screen, camera):
        """Render tank enemy with telegraph flash"""
        screen_pos = camera.apply(self.position)

        # Flash red when telegraphing
        color = self.flash_color if self.is_telegraphing else self.color

        # Draw enemy circle
        pygame.draw.circle(
            screen, color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

        self._draw_health_bar(screen, screen_pos)

    def _draw_health_bar(self, screen, screen_pos):
        """Draw health bar above enemy"""
        if self.health >= self.max_health:
            return

        bar_width = self.size
        bar_height = 4
        bar_x = screen_pos.x - bar_width // 2
        bar_y = screen_pos.y - self.radius - 10

        # Background (red)
        pygame.draw.rect(screen, Colors.RED, (bar_x, bar_y, bar_width, bar_height))

        # Foreground (green)
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, Colors.GREEN, (bar_x, bar_y, health_width, bar_height))
