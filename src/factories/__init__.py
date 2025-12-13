"""
Factories
Factory classes for creating game entities
"""

from .weapon_factory import (
    WeaponFactory,
    create_starter_weapon,
    create_upgraded_weapon,
)

__all__ = ["WeaponFactory", "create_starter_weapon", "create_upgraded_weapon"]
