"""
Bomb Pickup
Gives player bombs when collected
"""

import pygame
from src.entities.pickups.base_pickup import BasePickup


class BombPickup(BasePickup):
    """Bomb pickup - restores bombs to player inventory"""

    def __init__(self, x, y, bomb_amount=1):
        """
        Initialize bomb pickup

        Args:
            x: X position
            y: Y position
            bomb_amount: Number of bombs to give
        """
        super().__init__(x, y)
        self.bomb_amount = bomb_amount

        # Visual
        self.radius = 12
        self.color = (50, 50, 50)  # Dark gray (bomb color)
        self.highlight_color = (255, 215, 0)  # Gold outline

    def update(self, dt, player):
        """Bomb pickups are stationary (don't chase)"""
        pass

    def on_collect(self, player):
        """
        Give bombs to player

        Args:
            player: Player entity

        Returns:
            int: Number of bombs given
        """
        player.add_bombs(self.bomb_amount)
        return self.bomb_amount

    def render(self, screen, camera):
        """
        Render bomb pickup

        Args:
            screen: Pygame surface
            camera: Camera for position conversion
        """
        screen_pos = camera.apply(self.position)

        # Draw outer gold circle
        pygame.draw.circle(
            screen,
            self.highlight_color,
            (int(screen_pos.x), int(screen_pos.y)),
            self.radius + 2,
        )

        # Draw inner bomb
        pygame.draw.circle(
            screen, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius
        )

        # Draw fuse (small line on top)
        fuse_start = (int(screen_pos.x), int(screen_pos.y) - self.radius)
        fuse_end = (int(screen_pos.x), int(screen_pos.y) - self.radius - 5)
        pygame.draw.line(screen, (255, 140, 0), fuse_start, fuse_end, 2)
