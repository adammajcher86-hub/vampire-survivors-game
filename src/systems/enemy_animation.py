"""
Enemy Animation System
Handles sprite animation for enemies
"""

import pygame
from typing import List


class EnemyAnimation:
    """Manages sprite-based animation for enemies"""

    def __init__(self, sprite_paths: List[str], frame_duration: float = 0.1):
        """
        Initialize enemy animation

        Args:
            sprite_paths: List of paths to sprite frames
            frame_duration: Time per frame in seconds (default 0.1 = 10 FPS)
        """
        self.frames = []
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_accumulated = 0.0

        # Load all frames
        for path in sprite_paths:
            try:
                frame = pygame.image.load(path).convert_alpha()
                self.frames.append(frame)
            except pygame.error as e:
                print(f"⚠️ Failed to load {path}: {e}")

        if not self.frames:
            raise ValueError("No frames loaded for enemy animation!")

        print(f"Loaded {len(self.frames)} frames for enemy animation")

    def update(self, dt: float):
        """
        Update animation

        Args:
            dt: Delta time in seconds
        """
        self.time_accumulated += dt

        # Advance frame when enough time has passed
        if self.time_accumulated >= self.frame_duration:
            self.time_accumulated -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self) -> pygame.Surface:
        """Get current animation frame"""
        return self.frames[self.current_frame]

    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.time_accumulated = 0.0


class EnemyAnimationConfig:
    """Configuration for enemy animations"""

    # Base enemy animation frames
    BASE_ENEMY_FRAMES = [
        "src/assets/sprites/enemies/base_enemy1.png",
        "src/assets/sprites/enemies/base_enemy2.png",
        "src/assets/sprites/enemies/base_enemy3.png",
        "src/assets/sprites/enemies/base_enemy4.png",
    ]

    # Animation speed (seconds per frame)
    FRAME_DURATION = 0.15  # ~6.7 FPS animation

    # Fast enemy (faster animation)
    FAST_ENEMY_FRAME_DURATION = 0.1  # ~10 FPS

    # Tank enemy (slower animation)
    TANK_ENEMY_FRAME_DURATION = 0.2  # ~5 FPS


def create_base_enemy_animation() -> EnemyAnimation:
    """
    Create animation for base enemy

    Returns:
        EnemyAnimation instance
    """
    return EnemyAnimation(
        EnemyAnimationConfig.BASE_ENEMY_FRAMES,
        frame_duration=EnemyAnimationConfig.FRAME_DURATION,
    )
