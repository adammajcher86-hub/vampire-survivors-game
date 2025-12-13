"""
Fast Enemy
Fast, agile enemy that circles player and performs dash attacks
"""

import pygame
import random
from src.entities.enemies.base_enemy import Enemy
from src.config.enemies.fast_enemy import FastEnemyConfig
from src.config.common.colors import Colors


class FastEnemy(Enemy):
    """Fast enemy - circles player and dashes"""

    def __init__(self, x, y):
        """Initialize fast enemy"""
        super().__init__(x, y, FastEnemyConfig)

        # Stats
        self.max_health = 5
        self.health = self.max_health
        self.speed = 120
        self.damage = 3
        self.xp_value = 2

        # Visual
        self.color = (255, 200, 100)  # Orange
        self.size = 15
        self.radius = self.size // 2

        # Circling behavior
        self.circle_direction = random.choice([1, -1])  # Random rotation direction

        # Dash state
        self.can_dash = True
        self.is_telegraphing = False
        self.telegraph_timer = 0.0
        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_direction = pygame.math.Vector2(0, 0)
        self.dash_cooldown = random.uniform(
            FastEnemyConfig.DASH_COOLDOWN_MIN, FastEnemyConfig.DASH_COOLDOWN_MAX
        )

        # Visual state
        self.visible = True
        self.blink_timer = 0.0

    def update(self, dt, player_position):
        """Update fast enemy with circling and dash behavior"""
        distance_to_player = self.position.distance_to(player_position)

        # Update dash cooldown
        if not self.is_telegraphing and not self.is_dashing and self.can_dash:
            self.dash_cooldown -= dt

        # Check if should start telegraph
        if (
            self.can_dash
            and not self.is_telegraphing
            and not self.is_dashing
            and self.dash_cooldown <= 0
        ):
            # Only dash when orbiting (not too far, not too close)
            if (
                abs(distance_to_player - FastEnemyConfig.ORBIT_DISTANCE)
                < FastEnemyConfig.ORBIT_THRESHOLD * 2
            ):
                self._start_telegraph(player_position)

        # Handle telegraph (warning)
        if self.is_telegraphing:
            self.telegraph_timer -= dt

            # Blink effect
            self.blink_timer += dt
            if self.blink_timer >= 0.1:
                self.visible = not self.visible
                self.blink_timer = 0.0

            if self.telegraph_timer <= 0:
                self.is_telegraphing = False
                self.visible = True
                self._start_dash()

        # Handle dash movement
        elif self.is_dashing:
            self.dash_timer -= dt

            if self.dash_timer <= 0:
                # Dash ended
                self.is_dashing = False

                # 30% chance to explode!
                if random.random() < FastEnemyConfig.EXPLOSION_CHANCE:
                    # Mark for explosion (game_engine will spawn lasers)
                    self.ready_to_explode = True
                else:
                    # Normal dash end - reset cooldown
                    self.dash_cooldown = random.uniform(
                        FastEnemyConfig.DASH_COOLDOWN_MIN,
                        FastEnemyConfig.DASH_COOLDOWN_MAX,
                    )
                    # Reverse circle direction after dash
                    self.circle_direction *= -1
            else:
                # Continue dash movement
                velocity = self.dash_direction * FastEnemyConfig.DASH_SPEED
                self.position += velocity * dt

        # Normal circling movement
        else:
            direction = player_position - self.position
            if direction.length() > 0:
                direction = direction.normalize()

            if (
                distance_to_player
                > FastEnemyConfig.ORBIT_DISTANCE + FastEnemyConfig.ORBIT_THRESHOLD
            ):
                # Too far - chase
                velocity = direction * self.speed
            elif (
                distance_to_player
                < FastEnemyConfig.ORBIT_DISTANCE - FastEnemyConfig.ORBIT_THRESHOLD
            ):
                # Too close - back away
                velocity = -direction * self.speed * FastEnemyConfig.RADIAL_SPEED_MULT
            else:
                # Orbit - circle around player
                perpendicular = pygame.math.Vector2(
                    -direction.y * self.circle_direction,
                    direction.x * self.circle_direction,
                )

                distance_error = distance_to_player - FastEnemyConfig.ORBIT_DISTANCE
                radial_correction = (
                    direction * distance_error * FastEnemyConfig.RADIAL_SPEED_MULT
                )

                velocity = (perpendicular * self.speed) - radial_correction

            self.position += velocity * dt

        # Update rect
        self.rect.center = (int(self.position.x), int(self.position.y))

    def _start_telegraph(self, player_position):
        """Start telegraph warning before dash"""
        self.is_telegraphing = True
        self.telegraph_timer = FastEnemyConfig.TELEGRAPH_DURATION
        self.visible = True
        self.blink_timer = 0.0

        # Calculate dash direction to opposite side
        # Mirror enemy position across player
        # If enemy is left of player, dash to right side
        enemy_to_player = player_position - self.position

        # Opposite position = player + (player - enemy) = mirror across player
        opposite_position = player_position + enemy_to_player

        # Direction from current position to opposite side
        dash_vector = opposite_position - self.position
        if dash_vector.length() > 0:
            self.dash_direction = dash_vector.normalize()

    def _start_dash(self):
        """Start the dash attack"""
        self.is_dashing = True
        self.dash_timer = FastEnemyConfig.DASH_DURATION
        self.dash_hit_player = False

    def render(self, screen, camera, player_position):
        """Render fast enemy with blink effect"""
        if not self.visible:
            return

        screen_pos = camera.apply(self.position)

        # Color changes during telegraph
        color = FastEnemyConfig.TELEGRAPH_COLOR if self.is_telegraphing else self.color

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

        pygame.draw.rect(screen, Colors.RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, Colors.GREEN, (bar_x, bar_y, health_width, bar_height))

    def should_explode(self):
        """Check if enemy should explode"""
        return hasattr(self, "ready_to_explode") and self.ready_to_explode

    def get_explosion_position(self):
        """Get position for laser explosion"""
        return self.position.copy()
