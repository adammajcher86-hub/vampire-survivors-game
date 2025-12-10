"""
Weapon Fire Animation
Handles weapon fire animation with multi-frame cycling
"""

import pygame


class WeaponFireAnimation:
    """Manages weapon fire animation state"""

    def __init__(
        self, animation_sprite_path, frame_width=32, frame_height=16, frame_count=3
    ):
        """
        Initialize weapon fire animation

        Args:
            animation_sprite_path: Path to animation sprite sheet
            frame_width: Width of each frame
            frame_height: Height of each frame
            frame_count: Number of animation frames
        """
        # Load sprite sheet
        self.sprite_sheet = pygame.image.load(animation_sprite_path).convert_alpha()

        # Frame properties
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count

        # Extract frames from horizontal strip
        self.frames = []
        for i in range(frame_count):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            # Extract from horizontal strip (x = i * frame_width)
            frame.blit(
                self.sprite_sheet,
                (0, 0),
                (i * frame_width, 0, frame_width, frame_height),
            )
            self.frames.append(frame)

        # Animation state
        self.is_playing = False
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.frame_duration = 0.05  # Each frame shows for 0.05 seconds
        self.total_duration = self.frame_duration * (
            frame_count - 1
        )  # Don't count idle frame

    def start(self):
        """Start fire animation from beginning"""
        self.is_playing = True
        self.current_frame_index = 0  # Start from frame 0
        self.animation_timer = 0.0

    def update(self, dt):
        """
        Update animation state - cycles through frames

        Args:
            dt: Delta time
        """
        if not self.is_playing:
            return

        self.animation_timer += dt

        # Calculate which frame to show based on time
        frame_progress = self.animation_timer / self.frame_duration
        self.current_frame_index = min(int(frame_progress), self.frame_count - 1)

        # Check if animation finished (reached last frame)
        if self.animation_timer >= self.total_duration:
            self.is_playing = False
            self.current_frame_index = 0  # Return to idle frame
            self.animation_timer = 0.0

    def get_current_frame(self):
        """
        Get current animation frame

        Returns:
            pygame.Surface: Current frame sprite
        """
        return self.frames[self.current_frame_index]

    def is_animating(self):
        """Check if animation is currently playing"""
        return self.is_playing

    def reset(self):
        """Reset animation to idle state"""
        self.is_playing = False
        self.current_frame_index = 0
        self.animation_timer = 0.0
