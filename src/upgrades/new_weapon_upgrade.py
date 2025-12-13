"""
New Weapon Upgrade
Adds new weapon to player's weapon slots
"""

from src.upgrades.base_upgrade import BaseUpgrade
from src.factories import WeaponFactory
from src.logger import logger


class NewWeaponUpgrade(BaseUpgrade):
    """Add new weapon to player"""

    def __init__(self, weapon_type, weapon_name):
        """
        Initialize new weapon upgrade

        Args:
            weapon_type: Type of weapon to add (e.g., 'basic', 'laser', 'spread')
            weapon_name: Display name
        """
        super().__init__(
            name=f"New Weapon: {weapon_name}",
            description=f"Add {weapon_name} to weapon slot",
            icon_text="⚔️",
        )
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name

    def can_apply(self, player):
        """Check if player has empty weapon slot"""
        return player.get_empty_slot_count() > 0

    def apply(self, player):
        """Add weapon to empty slot using factory"""

        # Create level 1 weapon (clear and explicit)
        weapon = WeaponFactory.create(self.weapon_type, level=1)

        if player.add_weapon(weapon):
            logger.info(f"⚔️ Added {self.weapon_name} to weapon slot!")
            return True

        return False
