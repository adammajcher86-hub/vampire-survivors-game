"""
Upgrades Module
All upgrade classes for level-up system
"""

from .base_upgrade import BaseUpgrade
from .new_weapon_upgrade import NewWeaponUpgrade
from .weapon_level_upgrade import WeaponLevelUpgrade
from .stat_upgrade import StatUpgrade

__all__ = [
    "BaseUpgrade",
    "NewWeaponUpgrade",
    "WeaponLevelUpgrade",
    "StatUpgrade",
]
