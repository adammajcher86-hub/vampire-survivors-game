"""
New Weapon Upgrade
Adds new weapon to player's weapon slots
"""

from src.upgrades.base_upgrade import BaseUpgrade


class NewWeaponUpgrade(BaseUpgrade):
    """Add new weapon to player"""

    def __init__(self, weapon_class, weapon_name):
        """
        Initialize new weapon upgrade

        Args:
            weapon_class: Class of weapon to add (e.g., BasicWeapon)
            weapon_name: Display name
        """
        super().__init__(
            name=f"New Weapon: {weapon_name}",
            description=f"Add {weapon_name} to weapon slot",
            icon_text="⚔️",
        )
        self.weapon_class = weapon_class
        self.weapon_name = weapon_name

    def can_apply(self, player):
        """Check if player has empty weapon slot"""
        return player.get_empty_slot_count() > 0

    def apply(self, player):
        """Add weapon to empty slot"""
        weapon = self.weapon_class()

        if player.add_weapon(weapon):
            from src.logger import logger

            logger.info(f"⚔️ Added {self.weapon_name} to weapon slot!")
            return True

        return False
