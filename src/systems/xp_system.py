"""
XP System
Manages experience points and leveling
"""

from src.config import GameConfig


class XPSystem:
    """Manages XP tracking and player leveling"""

    def __init__(self):
        self.current_level = 1
        self.current_xp = 0
        self.xp_to_next_level = GameConfig.BASE_XP_REQUIRED

        # Level up notification
        self.level_up_flash = False
        self.level_up_timer = 0.0
        self.level_up_duration = 2.0

    def update(self, dt, collected_xp=0):
        """
        Update XP system

        Args:
            dt: Delta time in seconds
            collected_xp: XP collected this frame (from PickupManager)

        Returns:
            bool: True if player leveled up this frame
        """
        leveled_up = False

        # Add collected XP
        if collected_xp > 0:
            self.current_xp += collected_xp

            # Check for level up
            while self.current_xp >= self.xp_to_next_level:
                self._level_up()
                leveled_up = True

        # Update level up flash
        if self.level_up_flash:
            self.level_up_timer += dt
            if self.level_up_timer >= self.level_up_duration:
                self.level_up_flash = False
                self.level_up_timer = 0.0

        return leveled_up

    def _level_up(self):
        """Handle level up"""
        # Consume XP
        self.current_xp -= self.xp_to_next_level

        # Increase level
        self.current_level += 1

        # Calculate XP needed for next level
        self.xp_to_next_level = int(
            GameConfig.BASE_XP_REQUIRED
            * (GameConfig.XP_MULTIPLIER ** (self.current_level - 1))
        )

        # Trigger level up notification
        self.level_up_flash = True
        self.level_up_timer = 0.0

        print(f"LEVEL UP! Now level {self.current_level}")
        print(f"XP to next level: {self.xp_to_next_level}")

    def get_xp_progress(self):
        """
        Get XP progress as a percentage

        Returns:
            float: Progress from 0.0 to 1.0
        """
        return self.current_xp / self.xp_to_next_level

    def render(self, screen):
        """
        Render XP bar (if you have rendering logic)

        Args:
            screen: Pygame surface to draw on
        """
        # TODO: Add XP bar rendering if needed
        pass
