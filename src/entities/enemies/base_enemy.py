"""
Base Enemy Entity
Base class for all enemy types with common behavior
Supports both CIRCLE and RECTANGLE collision (configurable)
"""

import math
import pygame
from src.systems.enemy_animation import create_base_enemy_animation


class CollisionConfig:
    """Configuration for enemy collision - supports circles and rectangles"""

    def __init__(
        self,
        shape="circle",
        radius=None,
        width=None,
        height=None,
        offset_x=0,
        offset_y=0,
    ):
        """
        Initialize collision configuration

        Args:
            shape: 'circle' or 'rect'
            radius: Radius for circle collision (None = use sprite radius)
            width: Width for rect collision (None = use sprite size)
            height: Height for rect collision (None = use sprite size)
            offset_x: Horizontal offset (positive = right, negative = left)
            offset_y: Vertical offset (positive = down, negative = up)
        """
        self.shape = shape  # 'circle' or 'rect'
        self.radius = radius
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y


class Enemy(pygame.sprite.Sprite):
    """Base enemy class - all enemies inherit from this"""

    def __init__(self, x, y, config, collision_config=None):
        """
        Initialize enemy with configuration

        Args:
            x: Initial x position
            y: Initial y position
            config: Enemy configuration class (BaseEnemyConfig, FastEnemyConfig, etc.)
            collision_config: Optional CollisionConfig for custom collision
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

        # For sprite collision (legacy, kept for compatibility)
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.position.x), int(self.position.y))

        # COLLISION SYSTEM (Circle or Rectangle)
        self._setup_collision(collision_config)

        # State
        self.is_dead = False

        # Animation
        try:
            self.animation = create_base_enemy_animation()
            self.use_sprite = True
        except Exception as e:
            print(f"⚠️ Failed to load enemy animation: {e}")
            self.animation = None
            self.use_sprite = False

        self.current_sprite = None
        self.last_angle = 0

        # Debug
        self.show_collision_debug = False  # Set to True to see collision

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

        # Update animation
        if self.animation:
            self.animation.update(dt)

        # Update collision
        self.rect.center = (int(self.position.x), int(self.position.y))
        self._update_collision()

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

    def collides_with_circle(self, center, radius):
        """
        Check collision with a circle

        Args:
            center: Vector2 center of circle
            radius: Radius of circle

        Returns:
            bool: True if colliding
        """
        collision_center = self.get_collision_center()

        if self.collision_shape == "circle":
            # Circle vs Circle
            distance = collision_center.distance_to(center)
            return distance < (self.collision_radius + radius)
        else:
            # Rect vs Circle - use closest point method
            # Find closest point on rect to circle center
            closest_x = max(
                self.collision_rect.left, min(center.x, self.collision_rect.right)
            )
            closest_y = max(
                self.collision_rect.top, min(center.y, self.collision_rect.bottom)
            )
            closest = pygame.math.Vector2(closest_x, closest_y)

            distance = center.distance_to(closest)
            return distance < radius

    def collides_with_rect(self, rect):
        """
        Check collision with a rectangle

        Args:
            rect: pygame.Rect to check

        Returns:
            bool: True if colliding
        """
        if self.collision_shape == "rect":
            # Rect vs Rect
            return self.collision_rect.colliderect(rect)
        else:
            # Circle vs Rect - use closest point method
            collision_center = self.get_collision_center()

            # Find closest point on rect to circle center
            closest_x = max(rect.left, min(collision_center.x, rect.right))
            closest_y = max(rect.top, min(collision_center.y, rect.bottom))
            closest = pygame.math.Vector2(closest_x, closest_y)

            distance = collision_center.distance_to(closest)
            return distance < self.collision_radius

    def collides_with(self, other):
        """
        Check collision with another entity
        Auto-detects collision type

        Args:
            other: Entity to check collision with

        Returns:
            bool: True if colliding
        """
        # Check what collision type the other entity uses
        if hasattr(other, "collision_shape"):
            # Other entity has collision system
            if other.collision_shape == "circle":
                return self.collides_with_circle(
                    other.get_collision_center(), other.collision_radius
                )
            else:
                return self.collides_with_rect(other.collision_rect)
        elif hasattr(other, "collision_rect"):
            # Other entity has rect only
            return self.collides_with_rect(other.collision_rect)
        elif hasattr(other, "rect"):
            # Fallback to rect
            return self.collides_with_rect(other.rect)
        else:
            # Fallback to circle collision with position and radius
            other_pos = getattr(other, "position", pygame.math.Vector2(0, 0))
            other_radius = getattr(other, "radius", 10)
            return self.collides_with_circle(other_pos, other_radius)

    def render(self, screen, camera, player_position):
        """Render enemy with optional collision debug"""
        screen_pos = camera.apply(self.position)

        if self.use_sprite and self.animation:
            current_frame = self.animation.get_current_frame()

            # Calculate angle to player
            dx = player_position.x - self.position.x
            dy = player_position.y - self.position.y
            angle_deg = math.degrees(math.atan2(dy, dx)) + 90

            # Rotate and draw
            rotated = pygame.transform.rotate(current_frame, -angle_deg)
            rect = rotated.get_rect(center=(int(screen_pos.x), int(screen_pos.y)))
            screen.blit(rotated, rect)
        else:
            pygame.draw.circle(
                screen, self.color, (int(screen_pos.x), int(screen_pos.y)), 15
            )

        # DEBUG: Show collision
        # self._render_collision_debug(screen, camera)

        # Health bar
        if hasattr(self, "max_health") and self.health < self.max_health:
            self._render_health_bar(screen, screen_pos)

    def _render_collision_debug(self, screen, camera):
        """Render collision debug visualization"""
        collision_center = camera.apply(self.get_collision_center())

        if self.collision_shape == "circle":
            # Draw collision circle (green)
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (int(collision_center.x), int(collision_center.y)),
                int(self.collision_radius),
                2,
            )
        else:
            # Draw collision rect (green)
            collision_screen = pygame.Rect(
                self.collision_rect.x - int(camera.offset.x),
                self.collision_rect.y - int(camera.offset.y),
                self.collision_rect.width,
                self.collision_rect.height,
            )
            pygame.draw.rect(screen, (0, 255, 0), collision_screen, 2)

        # Draw sprite center (red)
        screen_pos = camera.apply(self.position)
        pygame.draw.circle(
            screen, (255, 0, 0), (int(screen_pos.x), int(screen_pos.y)), 3
        )

        # Draw collision center (yellow)
        pygame.draw.circle(
            screen, (255, 255, 0), (int(collision_center.x), int(collision_center.y)), 3
        )

        # Draw shape type text
        font = pygame.font.Font(None, 16)
        shape_text = f"{self.collision_shape.upper()}"
        text_surface = font.render(shape_text, True, (255, 255, 255))
        screen.blit(text_surface, (collision_center.x + 15, collision_center.y - 20))

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

    def _setup_collision(self, collision_config):
        """
        Setup collision with optional custom configuration
        Supports both circle and rectangle collision

        Args:
            collision_config: CollisionConfig or None for default
        """
        if collision_config is None:
            # Default: circle collision using sprite radius
            self.collision_shape = "circle"
            self.collision_radius = self.radius
            self.collision_offset = pygame.math.Vector2(0, 0)
            self.collision_rect = None  # Not used for circle
        elif collision_config.shape == "circle":
            # Circle collision
            self.collision_shape = "circle"
            self.collision_radius = (
                collision_config.radius
                if collision_config.radius is not None
                else self.radius
            )
            self.collision_offset = pygame.math.Vector2(
                collision_config.offset_x, collision_config.offset_y
            )
            self.collision_rect = None  # Not used for circle
        else:
            # Rectangle collision
            self.collision_shape = "rect"
            width = (
                collision_config.width
                if collision_config.width is not None
                else self.size
            )
            height = (
                collision_config.height
                if collision_config.height is not None
                else self.size
            )
            self.collision_rect = pygame.Rect(0, 0, width, height)
            self.collision_offset = pygame.math.Vector2(
                collision_config.offset_x, collision_config.offset_y
            )
            self.collision_radius = None  # Not used for rect

        # Update collision position
        self._update_collision()

    def _update_collision(self):
        """Update collision position based on sprite position and offset"""
        if self.collision_shape == "rect":
            self.collision_rect.centerx = int(self.position.x + self.collision_offset.x)
            self.collision_rect.centery = int(self.position.y + self.collision_offset.y)
        # Circle position is calculated dynamically from self.position + offset

    def get_collision_center(self):
        """Get the center of the collision area"""
        return self.position + self.collision_offset


# ============================================
# HELPER FUNCTIONS - CIRCLE COLLISION
# ============================================


def create_circle_collision(radius=None, offset_x=0, offset_y=0):
    """
    Create a circle collision configuration

    Args:
        radius: Collision radius (None = use sprite radius)
        offset_x: Horizontal offset (positive = right, negative = left)
        offset_y: Vertical offset (positive = down, negative = up)

    Returns:
        CollisionConfig instance

    Examples:
        # Default circle (sprite radius, centered)
        config = create_circle_collision()

        # Smaller circle (tight hitbox)
        config = create_circle_collision(radius=8)

        # Circle offset to the right (for tail on left)
        config = create_circle_collision(radius=10, offset_x=4)
    """
    return CollisionConfig(
        shape="circle", radius=radius, offset_x=offset_x, offset_y=offset_y
    )


def get_tight_circle(sprite_radius, tightness=0.7):
    """
    Get a tight circle collision (smaller than sprite)

    Args:
        sprite_radius: Radius of the sprite
        tightness: How tight (0.5 = half size, 0.7 = 70%, 1.0 = full size)

    Returns:
        CollisionConfig instance

    Examples:
        # Very tight hitbox (50%)
        config = get_tight_circle(12, 0.5)

        # Balanced hitbox (70%)
        config = get_tight_circle(12, 0.7)
    """
    collision_radius = int(sprite_radius * tightness)
    return CollisionConfig(shape="circle", radius=collision_radius)


def get_offset_circle(sprite_radius, offset_x=0, offset_y=0, tightness=0.7):
    """
    Get an offset circle collision (for sprites with tails/extensions)

    Args:
        sprite_radius: Radius of the sprite
        offset_x: Horizontal offset
        offset_y: Vertical offset
        tightness: Size multiplier

    Returns:
        CollisionConfig instance

    Examples:
        # Circle offset right (tail on left)
        config = get_offset_circle(12, offset_x=4)

        # Circle offset up (legs on bottom)
        config = get_offset_circle(12, offset_y=-3)
    """
    collision_radius = int(sprite_radius * tightness)
    return CollisionConfig(
        shape="circle", radius=collision_radius, offset_x=offset_x, offset_y=offset_y
    )


# ============================================
# HELPER FUNCTIONS - RECTANGLE COLLISION
# ============================================


def create_rect_collision(width=None, height=None, offset_x=0, offset_y=0):
    """
    Create a rectangle collision configuration

    Args:
        width: Width of collision box (None = use sprite size)
        height: Height of collision box (None = use sprite size)
        offset_x: Horizontal offset
        offset_y: Vertical offset

    Returns:
        CollisionConfig instance
    """
    return CollisionConfig(
        shape="rect", width=width, height=height, offset_x=offset_x, offset_y=offset_y
    )


def get_body_rect(sprite_size, tail_side="left"):
    """
    Get rectangle collision for sprites with tails/extensions

    Args:
        sprite_size: Size of the sprite
        tail_side: Which side has the tail ('left', 'right', 'top', 'bottom')

    Returns:
        CollisionConfig instance
    """
    collision_size = int(sprite_size * 0.6)
    offset = int(sprite_size * 0.2)

    if tail_side == "left":
        return CollisionConfig(
            shape="rect",
            width=collision_size,
            height=collision_size,
            offset_x=offset,
            offset_y=0,
        )
    elif tail_side == "right":
        return CollisionConfig(
            shape="rect",
            width=collision_size,
            height=collision_size,
            offset_x=-offset,
            offset_y=0,
        )
    elif tail_side == "top":
        return CollisionConfig(
            shape="rect",
            width=collision_size,
            height=collision_size,
            offset_x=0,
            offset_y=offset,
        )
    elif tail_side == "bottom":
        return CollisionConfig(
            shape="rect",
            width=collision_size,
            height=collision_size,
            offset_x=0,
            offset_y=-offset,
        )
    else:
        return CollisionConfig(
            shape="rect",
            width=collision_size,
            height=collision_size,
            offset_x=0,
            offset_y=0,
        )
