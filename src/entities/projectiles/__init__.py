"""
Projectile Entities
All projectile classes (polymorphic)
"""

from .base_projectile import BaseProjectile
from .basic_projectile import BasicProjectile

__all__ = [
    "BaseProjectile",
    "BasicProjectile",
]
