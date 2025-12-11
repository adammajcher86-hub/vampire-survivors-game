"""
Upgrade System
Manages available upgrades and generates choices for level-up
"""

import random
from src.upgrades import WeaponLevelUpgrade, StatUpgrade, NewWeaponUpgrade
from src.entities.weapons import BasicWeapon, SpreadWeapon, LaserWeapon


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
                    10,
                    is_percentage=False,
                    icon="🧲",
                ),
                StatUpgrade(
                    "Max Health", "max_health", 20, is_percentage=False, icon="❤️"
                ),
                StatUpgrade(
                    "Attack Speed",
                    "attack_speed_multiplier",
                    0.30,
                    is_percentage=True,
                    icon="⚡",
                ),
                StatUpgrade("HP Regen", "hp_regen", 1, is_percentage=False, icon="💚"),
            ]
        )

        # Weapon upgrades
        self.available_upgrades.append(
            NewWeaponUpgrade(BasicWeapon, "Basic Weapon")  # Can add multiple!
        )
        self.available_upgrades.append(NewWeaponUpgrade(SpreadWeapon, "Spread Shot"))
        self.available_upgrades.append(NewWeaponUpgrade(LaserWeapon, "Laser Weapon"))

    def generate_choices(self, player, num_choices=3):
        """
        Generate random upgrade choices

        Args:
            player: Player entity
            num_choices: Number of choices to offer (default 3)

        Returns:
            list: List of upgrade instances
        """
        # Filter to only upgrades that can be applied
        valid_upgrades = [
            upgrade
            for upgrade in self.available_upgrades
            if upgrade.can_apply(player)  # ✅ Only pass player
        ]

        # If not enough valid upgrades, return what we have
        if len(valid_upgrades) <= num_choices:
            return valid_upgrades

        # Randomly select num_choices upgrades
        return random.sample(valid_upgrades, num_choices)

    def apply_upgrade(self, upgrade, player):
        """
        Apply selected upgrade

        Args:
            upgrade: Upgrade instance to apply
            player: Player entity

        Returns:
            str: Message describing what was upgraded
        """
        return upgrade.apply(player)  # ✅ Only pass player
