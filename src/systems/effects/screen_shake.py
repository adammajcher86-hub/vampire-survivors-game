"""
Screen Shake
Adds camera shake effects
"""

import random


class ScreenShake:
    """Manages screen shake effects"""

    def __init__(self):
        """Initialize screen shake"""
        self.trauma = 0.0  # Shake intensity (0.0 to 1.0)
        self.trauma_decay = 1.5  # How fast shake fades
        self.max_offset = 20  # Maximum screen offset
        self.current_offset_x = 0
        self.current_offset_y = 0

    def add_trauma(self, amount):
        """
        Add trauma to trigger shake

        Args:
            amount: Trauma amount (0.0 to 1.0)
                   0.3 = small shake
                   0.6 = medium shake
                   1.0 = big shake
        """
        self.trauma = min(1.0, self.trauma + amount)

    def update(self, dt):
        """
        Update shake and calculate offset

        Args:
            dt: Delta time
        """
        # Decay trauma over time
        self.trauma = max(0.0, self.trauma - self.trauma_decay * dt)

        if self.trauma > 0:
            # Calculate shake amount (trauma^2 for smoother curve)
            shake = self.trauma * self.trauma

            # Random offset based on shake amount
            self.current_offset_x = random.uniform(-1, 1) * self.max_offset * shake
            self.current_offset_y = random.uniform(-1, 1) * self.max_offset * shake
        else:
            self.current_offset_x = 0
            self.current_offset_y = 0

    def get_offset(self):
        """
        Get current shake offset

        Returns:
            tuple: (offset_x, offset_y)
        """
        return (self.current_offset_x, self.current_offset_y)

    def is_shaking(self):
        """Check if currently shaking"""
        return self.trauma > 0.01
