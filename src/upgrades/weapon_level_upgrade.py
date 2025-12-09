"""
Weapon Level Upgrade
Levels up an existing weapon
"""

from src.upgrades.base_upgrade import BaseUpgrade


class WeaponLevelUpgrade(BaseUpgrade):
    """Upgrade that levels up a weapon"""

    def __init__(self, weapon_class=None):
        """
        Initialize weapon level upgrade

        Args:
            weapon_class: Specific weapon class to upgrade (None = any weapon)
        """
        weapon_name = (
            weapon_class.__name__.replace("Weapon", "") if weapon_class else "Any"
        )

        super().__init__(
            name=f"Level Up: {weapon_name} Weapon",
            description="+10% Damage",
            icon_text="⬆️",
        )
        self.weapon_class = weapon_class

    def can_apply(self, player):
        """
        Check if any weapon can be leveled up

        Args:
            player: Player entity

        Returns:
            bool: True if at least one weapon can level up
        """
        # Get weapons from player's weapon slots ✅
        weapons = [slot.weapon for slot in player.weapon_slots if not slot.is_empty()]

        if not weapons:
            return False

        # If specific weapon class, check if player has it and it's not maxed
        if self.weapon_class:
            for weapon in weapons:
                if isinstance(weapon, self.weapon_class) and weapon.level < 8:
                    return True
            return False

        # Otherwise, check if any weapon can level up
        for weapon in weapons:
            if weapon.level < 8:
                return True
        return False

    def apply(self, player):
        """
        Level up a weapon

        Args:
            player: Player entity

        Returns:
            str: Success message
        """
        # Get weapons from player's weapon slots ✅
        weapons = [slot.weapon for slot in player.weapon_slots if not slot.is_empty()]

        # Find weapon to level up
        target_weapon = None

        if self.weapon_class:
            # Level up specific weapon type
            for weapon in weapons:
                if isinstance(weapon, self.weapon_class) and weapon.level < 8:
                    target_weapon = weapon
                    break
        else:
            # Level up lowest level weapon
            for weapon in weapons:
                if weapon.level < 8:
                    if target_weapon is None or weapon.level < target_weapon.level:
                        target_weapon = weapon

        if target_weapon:
            old_level = target_weapon.level
            target_weapon.level_up()
            return f"{target_weapon.get_name()} leveled up! (Lv.{old_level} → Lv.{target_weapon.level})"

        return "No weapon to level up"
