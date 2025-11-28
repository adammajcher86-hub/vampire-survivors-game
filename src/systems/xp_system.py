"""
XP System
Manages experience collection and leveling
"""

from src.config import GameConfig
from src.entities.xp_orb import XPOrb


class XPSystem:
    """Manages XP collection and player leveling"""

    def __init__(self):
        self.current_level = 1
        self.current_xp = 0
        self.xp_to_next_level = GameConfig.BASE_XP_REQUIRED

        # Level up notification
        self.level_up_flash = False
        self.level_up_timer = 0.0
        self.level_up_duration = 2.0

    def update(self, dt, player, xp_orbs):
        """
        Update XP system

        Args:
            dt: Delta time in seconds
            player: Player entity
            xp_orbs: Sprite group of XP orbs

        Returns:
            bool: True if player leveled up this frame
        """
        leveled_up = False

        # Update XP orbs (magnetic pull toward player)
        for orb in xp_orbs:
            orb.update(dt, player)

        # Check orb collection
        collected_xp = self._collect_orbs(player, xp_orbs)

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

    def _collect_orbs(self, player, xp_orbs):
        """
        Collect XP orbs that visually touch the player

        Args:
            player: Player entity
            xp_orbs: Sprite group of XP orbs

        Returns:
            int: Total XP collected this frame
        """
        collected_xp = 0

        for orb in list(xp_orbs):
            # Use actual visual collision (orb radius + player radius)
            distance = orb.position.distance_to(player.position)
            if distance < (orb.radius + player.radius):  # ✅ Visual collision!
                collected_xp += orb.xp_value
                xp_orbs.remove(orb)

        return collected_xp

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

    def create_xp_orb(self, x, y, xp_value):
        """
        Create an XP orb at the given position

        Args:
            x: X position
            y: Y position
            xp_value: Amount of XP this orb gives

        Returns:
            XPOrb: The created XP orb
        """
        return XPOrb(x, y, xp_value)

    def get_xp_progress(self):
        """
        Get XP progress as a percentage

        Returns:
            float: Progress from 0.0 to 1.0
        """
        return self.current_xp / self.xp_to_next_level
