"""
Game Entities
All game entities (player, enemies, projectiles, weapons, etc.)
"""

from .player import Player
from .pickups import XPOrb  # ✅ Changed from .xp_orb

# Import all enemies from enemies subdirectory
from .enemies import (
    Enemy,
    BasicEnemy,
    FastEnemy,
    TankEnemy,
    EliteEnemy,
)

# Import all projectiles from projectiles subdirectory
from .projectiles import (
    BaseProjectile,
    BasicProjectile,
)

# Import all weapons from weapons subdirectory
from .weapons import (
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
    # Projectiles
    "BaseProjectile",
    "BasicProjectile",
    # Weapons
    "BaseWeapon",
    "BasicWeapon",
]
