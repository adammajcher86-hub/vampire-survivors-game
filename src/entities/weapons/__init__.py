"""
Weapon Entities
All weapon classes (polymorphic)
"""

from .base_weapon import BaseWeapon
from .basic_weapon import BasicWeapon

__all__ = [
    "BaseWeapon",
    "BasicWeapon",
]
