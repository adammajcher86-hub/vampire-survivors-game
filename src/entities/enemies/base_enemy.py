"""
Enemy with Shared Sprites but Individual Animation State
Sprites loaded once at class level, each enemy has own frame counter
"""

import math
import pygame
from typing import Optional, List
from src.systems.enemy_animation import EnemyAnimationConfig


class Enemy(pygame.sprite.Sprite):
    """
    Enemy with optimized animation
    - Sprites loaded ONCE at class level (efficient!)
    - Animation state per instance (correct timing!)
    """

    # CLASS VARIABLES - Sprite frames shared by all instances
    _sprite_frames: Optional[List[pygame.Surface]] = None
    _sprite_paths = EnemyAnimationConfig.BASE_ENEMY_FRAMES
    _frame_duration = EnemyAnimationConfig.FRAME_DURATION

    @classmethod
    def _load_sprites(cls):
        """Load sprite frames for this class (once per class)"""
        if cls._sprite_frames is None:
            cls._sprite_frames = []

            for path in cls._sprite_paths:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    cls._sprite_frames.append(sprite)
                except pygame.error as e:
                    print(f"⚠️ Failed to load {path}: {e}")
                    # Fallback: red square
                    sprite = pygame.Surface((24, 24))
                    sprite.fill((255, 0, 0))
                    cls._sprite_frames.append(sprite)

            if cls._sprite_frames:
                print(f"{cls.__name__}: Loaded {len(cls._sprite_frames)} sprite frames")

    def __init__(self, x, y, config, collision_config=None):
        """Initialize enemy instance"""
        super().__init__()

        # Load class sprites on first instance creation
        self._load_sprites()

        # Position and movement
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        # Stats from config
        self.max_health = config.HEALTH
        self.health = self.max_health
        self.speed = config.SPEED
        self.contact_damage = config.CONTACT_DAMAGE
        self.xp_value = config.XP_VALUE
        self.size = config.SIZE
        self.color = config.COLOR
        self.radius = config.SIZE // 2

        # Collision
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

        # Collision setup
        self.collision_shape = "circle"
        self.collision_radius = self.radius
        self.collision_offset = pygame.math.Vector2(0, 0)

        # State
        self.is_dead = False

        # INSTANCE-LEVEL animation state (each enemy has its own!)
        self.current_frame = 0
        self.frame_time_accumulated = 0.0
        self.use_sprite = len(self._sprite_frames) > 0 if self._sprite_frames else False

        # Performance
        self.current_sprite = None
        self.last_angle = 0

        # Debug
        self.show_collision_debug = False

    def update(self, dt, player_position):
        """Update enemy state"""
        if self.is_dead:
            return

        # Calculate direction to player
        direction = player_position - self.position
        if direction.length() > 0:
            direction = direction.normalize()

        # Move towards player
        self.velocity = direction * self.speed
        self.position += self.velocity * dt

        # Update INSTANCE animation state (not shared!)
        if self.use_sprite:
            self.frame_time_accumulated += dt

            # Advance frame when enough time has passed
            if self.frame_time_accumulated >= self._frame_duration:
                self.frame_time_accumulated -= self._frame_duration
                self.current_frame = (self.current_frame + 1) % len(self._sprite_frames)

        # Update collision
        self.rect.center = (int(self.position.x), int(self.position.y))

    def get_current_frame(self) -> pygame.Surface:
        """Get current animation frame from CLASS sprites"""
        if self.use_sprite and self._sprite_frames:
            return self._sprite_frames[self.current_frame]
        return None

    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            return True
        return False

    def get_xp_value(self):
        """Get XP value"""
        return self.xp_value

    def collides_with(self, other):
        """Check collision"""
        if hasattr(other, "rect"):
            return self.rect.colliderect(other.rect)
        return False

    def render(self, screen, camera, player_position):
        """Render enemy"""
        screen_pos = camera.apply(self.position)

        if self.use_sprite:
            current_frame = self.get_current_frame()

            if current_frame:
                # Calculate angle to player
                dx = player_position.x - self.position.x
                dy = player_position.y - self.position.y
                angle_deg = math.degrees(math.atan2(dy, dx)) + 90

                # Rotate and draw
                rotated = pygame.transform.rotate(current_frame, -angle_deg)
                rect = rotated.get_rect(center=(int(screen_pos.x), int(screen_pos.y)))
                screen.blit(rotated, rect)
            else:
                # Fallback to circle
                pygame.draw.circle(
                    screen, (255, 0, 0), (int(screen_pos.x), int(screen_pos.y)), 15
                )
        else:
            pygame.draw.circle(
                screen, self.color, (int(screen_pos.x), int(screen_pos.y)), 15
            )

        # Health bar
        if hasattr(self, "max_health") and self.health < self.max_health:
            self._render_health_bar(screen, screen_pos)

    def _render_health_bar(self, screen, screen_pos):
        """Render health bar"""
        bar_width = 30
        bar_height = 4
        bar_x = screen_pos.x - bar_width / 2
        bar_y = screen_pos.y - 25

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        health_ratio = max(0, self.health / self.max_health)
        pygame.draw.rect(
            screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height)
        )


# ============================================
# FAST ENEMY - FASTER ANIMATION
# ============================================


class FastEnemy(Enemy):
    """Fast enemy with faster animation"""

    # Own sprite frames
    _sprite_frames: Optional[List[pygame.Surface]] = None
    _sprite_paths = EnemyAnimationConfig.BASE_ENEMY_FRAMES
    _frame_duration = EnemyAnimationConfig.FAST_ENEMY_FRAME_DURATION  # Faster!


# ============================================
# TANK ENEMY - SLOWER ANIMATION
# ============================================


class TankEnemy(Enemy):
    """Tank enemy with slower animation"""

    # Own sprite frames
    _sprite_frames: Optional[List[pygame.Surface]] = None
    _sprite_paths = EnemyAnimationConfig.BASE_ENEMY_FRAMES
    _frame_duration = EnemyAnimationConfig.TANK_ENEMY_FRAME_DURATION  # Slower!
