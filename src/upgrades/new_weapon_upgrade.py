"""
New Weapon Upgrade
Adds a new weapon to player's arsenal
"""

from src.upgrades.base_upgrade import BaseUpgrade


class NewWeaponUpgrade(BaseUpgrade):
    """Upgrade that adds a new weapon"""

    def __init__(self, weapon_name, weapon_class):
        """
        Initialize new weapon upgrade

        Args:
            weapon_name: Display name of weapon
            weapon_class: Class to instantiate (e.g., BasicWeapon)
        """
        super().__init__(
            name=f"New Weapon: {weapon_name}",
            description=f"Unlock {weapon_name}",
            icon_text="🔫",
        )
        self.weapon_name = weapon_name
        self.weapon_class = weapon_class

    def can_apply(self, player, weapons):
        """
        Check if weapon can be added

        Args:
            player: Player entity
            weapons: List of player weapons

        Returns:
            bool: True if player doesn't already have this weapon
        """
        # Check if player already has this weapon type
        for weapon in weapons:
            if isinstance(weapon, self.weapon_class):
                return False
        return True

    def apply(self, player, weapons):
        """
        Add the new weapon

        Args:
            player: Player entity
            weapons: List of player weapons

        Returns:
            str: Success message
        """
        new_weapon = self.weapon_class()
        weapons.append(new_weapon)
        return f"Unlocked {self.weapon_name}!"
