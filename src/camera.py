"""
Camera
Follows player and handles screen shake
"""

import pygame


class Camera:
    """Camera that follows an entity with screen shake support"""

    def __init__(self, width, height):
        """
        Initialize camera

        Args:
            width: Camera width (screen width)
            height: Camera height (screen height)
        """
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2(0, 0)
        self.shake_offset = (0, 0)

    def update(self, target, shake_offset=(0, 0)):
        """
        Update camera to follow target with optional shake

        Args:
            target: Entity to follow (usually player)
            shake_offset: (x, y) tuple for screen shake offset
        """
        # ✅ Store shake offset
        self.shake_offset = shake_offset

        # Center camera on target
        self.offset.x = target.position.x - self.width // 2
        self.offset.y = target.position.y - self.height // 2

    def apply(self, entity_position):
        """
        Convert world position to screen position with shake

        Args:
            entity_position: Vector2 world position

        Returns:
            Vector2: Screen position with shake applied
        """
        return pygame.math.Vector2(
            entity_position.x - self.offset.x + self.shake_offset[0],
            entity_position.y - self.offset.y + self.shake_offset[1],
        )

    def apply_rect(self, rect):
        """
        Apply camera offset to a rect

        Args:
            rect: pygame.Rect in world coordinates

        Returns:
            pygame.Rect: Rect in screen coordinates
        """
        return rect.move(
            -self.offset.x + self.shake_offset[0], -self.offset.y + self.shake_offset[1]
        )
