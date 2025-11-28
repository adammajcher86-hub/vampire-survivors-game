"""
Upgrade System
Manages available upgrades and generates choices for level-up
"""

import random
from src.upgrades import WeaponLevelUpgrade, StatUpgrade


class UpgradeSystem:
    """Manages upgrades and generates level-up choices"""

    def __init__(self):
        """Initialize upgrade system with available upgrades"""
        self.available_upgrades = []
        self._initialize_upgrades()

    def _initialize_upgrades(self):
        """Initialize all available upgrades"""

        # Weapon level-up upgrades (always available if you have weapons)
        self.available_upgrades.append(
            WeaponLevelUpgrade(weapon_class=None)  # Levels up any weapon
        )

        # Stat upgrades
        self.available_upgrades.extend(
            [
                StatUpgrade("Speed", "speed", 20, is_percentage=False, icon="💨"),
                StatUpgrade(
                    "Pickup Range",
                    "xp_pickup_range",
                    20,
                    is_percentage=False,
                    icon="🧲",
                ),
                StatUpgrade(
                    "Max Health", "max_health", 20, is_percentage=False, icon="❤️"
                ),
            ]
        )

        # TODO: Add more weapon upgrades when you create new weapons
        # Example:
        # self.available_upgrades.append(
        #     NewWeaponUpgrade("Spread Weapon", SpreadWeapon)
        # )

    def generate_choices(self, player, weapons, num_choices=3):
        """
        Generate random upgrade choices

        Args:
            player: Player entity
            weapons: List of player weapons
            num_choices: Number of choices to offer (default 3)

        Returns:
            list: List of upgrade instances
        """
        # Filter to only upgrades that can be applied
        valid_upgrades = [
            upgrade
            for upgrade in self.available_upgrades
            if upgrade.can_apply(player, weapons)
        ]

        # If not enough valid upgrades, return what we have
        if len(valid_upgrades) <= num_choices:
            return valid_upgrades

        # Randomly select num_choices upgrades
        return random.sample(valid_upgrades, num_choices)

    def apply_upgrade(self, upgrade, player, weapons):
        """
        Apply selected upgrade

        Args:
            upgrade: Upgrade instance to apply
            player: Player entity
            weapons: List of player weapons

        Returns:
            str: Message describing what was upgraded
        """
        return upgrade.apply(player, weapons)
