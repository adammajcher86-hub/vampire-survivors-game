"""
Weapon Registry
Register all weapons with the factory
"""

from src.factories import WeaponFactory
from src.entities.weapons import BasicWeapon, LaserWeapon, SpreadWeapon
from src.logger import logger


def register_all_weapons():
    """Register all game weapons with factory"""

    # Register weapons
    WeaponFactory.register_weapon("basic", BasicWeapon)
    WeaponFactory.register_weapon("laser", LaserWeapon)
    WeaponFactory.register_weapon("spread", SpreadWeapon)

    # Add more weapons here as you create them:
    # WeaponFactory.register_weapon('chain_laser', ChainLaserWeapon)

    logger.debug(f"Registered weapons: {WeaponFactory.get_available_weapons()}")
