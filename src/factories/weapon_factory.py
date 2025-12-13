"""
Weapon Factory (Adapted for Config-Based Weapons)
Works with weapons that use Config classes instead of parameters
"""

from typing import Dict, Any


class WeaponFactory:
    """
    Factory for creating and upgrading weapons
    Adapted to work with config-based weapon classes
    """

    # Weapon registry - maps weapon types to classes
    _weapon_classes = {}

    @classmethod
    def register_weapon(cls, weapon_type: str, weapon_class):
        """
        Register a weapon class

        Args:
            weapon_type: Weapon type identifier (e.g., 'laser', 'basic')
            weapon_class: Weapon class to register

        Example:
            WeaponFactory.register_weapon('laser', LaserWeapon)
        """
        cls._weapon_classes[weapon_type.lower()] = weapon_class

    @classmethod
    def create(cls, weapon_type: str, level: int = 1) -> Any:
        """
        Create a weapon instance

        Args:
            weapon_type: Type of weapon ('basic', 'laser', 'spread')
            level: Weapon level (1-8, matches your BaseWeapon.level)

        Returns:
            Weapon instance

        Example:
            weapon = WeaponFactory.create('laser', level=2)
        """
        weapon_type = weapon_type.lower()

        # Get weapon class
        if weapon_type not in cls._weapon_classes:
            raise ValueError(
                f"Unknown weapon type: {weapon_type}. Available: {cls.get_available_weapons()}"
            )

        weapon_class = cls._weapon_classes[weapon_type]

        # Create weapon instance (no parameters - uses Config)
        weapon = weapon_class()

        # Apply level if > 1
        if level > 1:
            for _ in range(level - 1):
                weapon.level_up()
        print(weapon)
        return weapon

    @classmethod
    def upgrade(cls, weapon, level_increase: int = 1) -> Any:
        """
        Upgrade existing weapon

        Args:
            weapon: Existing weapon instance
            level_increase: How many levels to increase

        Returns:
            The SAME weapon instance (modified in-place)

        Note: Unlike the standard factory, this modifies the weapon in-place
              because your weapons use level_up() method

        Example:
            weapon = player.get_weapon()
            WeaponFactory.upgrade(weapon)  # Weapon is now level+1
        """
        for _ in range(level_increase):
            weapon.level_up()

        return weapon

    @classmethod
    def create_upgraded(cls, weapon_type: str, level: int) -> Any:
        """
        Create a weapon directly at a specific level

        Args:
            weapon_type: Type of weapon
            level: Desired level (1-8)

        Returns:
            Weapon instance at specified level

        Example:
            weapon = WeaponFactory.create_upgraded('laser', level=5)
        """
        return cls.create(weapon_type, level=level)

    @classmethod
    def get_available_weapons(cls) -> list:
        """
        Get list of available weapon types

        Returns:
            List of weapon type strings
        """
        return list(cls._weapon_classes.keys())

    @classmethod
    def get_weapon_info(cls, weapon_type: str, level: int = 1) -> Dict[str, Any]:
        """
        Get weapon information without creating permanent instance

        Args:
            weapon_type: Weapon type
            level: Weapon level

        Returns:
            Weapon stats dictionary
        """
        # Create temporary weapon to get stats
        temp_weapon = cls.create(weapon_type, level=level)

        info = {
            "type": weapon_type,
            "level": temp_weapon.level,
            "damage": temp_weapon.damage,
            "cooldown": temp_weapon.cooldown,
            "range": temp_weapon.range,
            "name": temp_weapon.get_name(),
        }

        # Add weapon-specific stats
        if hasattr(temp_weapon, "bounce_count"):
            info["bounces"] = temp_weapon.bounce_count

        if hasattr(temp_weapon, "projectile_count"):
            info["projectiles"] = temp_weapon.projectile_count

        return info


# ============================================
# HELPER FUNCTIONS
# ============================================


def create_starter_weapon(weapon_type: str = "basic"):
    """
    Create a level 1 starter weapon

    Args:
        weapon_type: Type of weapon to create

    Returns:
        Level 1 weapon instance
    """
    print(weapon_type)
    return WeaponFactory.create(weapon_type, level=1)


def create_upgraded_weapon(weapon_type: str, level: int):
    """
    Create an upgraded weapon at specific level

    Args:
        weapon_type: Type of weapon
        level: Desired level (1-8)

    Returns:
        Weapon instance at specified level
    """
    return WeaponFactory.create_upgraded(weapon_type, level=level)


def get_upgrade_preview(weapon) -> str:
    """
    Get preview text for upgrading a weapon

    Args:
        weapon: Weapon instance

    Returns:
        Description of what upgrade will do
    """
    current_level = getattr(weapon, "level", 1)

    if current_level >= 8:
        return "⭐ MAX LEVEL REACHED!"

    current_damage = weapon.damage

    # Simulate upgrade to see what changes
    weapon_type = weapon.get_name().replace(" Weapon", "").replace(" ", "_").lower()
    if "basic" in weapon_type:
        weapon_type = "basic"
    elif "laser" in weapon_type:
        weapon_type = "laser"
    elif "spread" in weapon_type:
        weapon_type = "spread"

    try:
        next_level_weapon = WeaponFactory.create(weapon_type, level=current_level + 1)
        next_damage = next_level_weapon.damage

        damage_diff = next_damage - current_damage

        preview = f"Level {current_level} → {current_level + 1}\n"
        preview += f"Damage: {current_damage} → {next_damage} (+{damage_diff})"

        # Add bounce info if laser
        if hasattr(weapon, "bounce_count") and hasattr(
            next_level_weapon, "bounce_count"
        ):
            if next_level_weapon.bounce_count > weapon.bounce_count:
                preview += f"\n💫 Bounces: {weapon.bounce_count} → {next_level_weapon.bounce_count}"

        return preview
    except Exception as e:
        return f"Level {current_level} → {current_level + 1}{e}\nDamage increase!"
