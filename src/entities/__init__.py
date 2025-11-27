"""
Game Entities
All game entities (player, enemies, projectiles, weapons, etc.)
"""

from .player import Player
from .xp_orb import XPOrb

# Import all enemies from enemies subdirectory
from .enemies import (
    Enemy,
    BasicEnemy,
    FastEnemy,
    TankEnemy,
    EliteEnemy,
)

# Import all weapons/projectiles from weapons subdirectory
from .weapons import (
    Projectile,
    BaseWeapon,
    BasicWeapon,
)

__all__ = [
    # Core entities
    "Player",
    "XPOrb",
    # Enemies
    "Enemy",
    "BasicEnemy",
    "FastEnemy",
    "TankEnemy",
    "EliteEnemy",
    # Weapons
    "Projectile",
    "BaseWeapon",
    "BasicWeapon",
]
