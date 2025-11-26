"""
Camera System
Handles camera positioning and smooth following
"""

import pygame
from src.config import GameConfig


class Camera:
    """Camera that smoothly follows the player"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2(0, 0)
        self.target = pygame.math.Vector2(0, 0)

    def update(self, player):
        """Update camera to follow player"""
        # Target position (center player on screen)
        self.target.x = player.position.x - self.width // 2
        self.target.y = player.position.y - self.height // 2

        # Smooth interpolation
        self.offset.x += (self.target.x - self.offset.x) * GameConfig.CAMERA_SMOOTHING
        self.offset.y += (self.target.y - self.offset.y) * GameConfig.CAMERA_SMOOTHING

    def apply(self, position):
        """Apply camera offset to a position"""
        return pygame.math.Vector2(
            position.x - self.offset.x, position.y - self.offset.y
        )

    def get_visible_rect(self):
        """Get the rectangle of visible world space"""
        return pygame.Rect(self.offset.x, self.offset.y, self.width, self.height)
