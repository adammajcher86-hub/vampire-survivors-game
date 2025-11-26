"""
Base Weapon Configuration
Default stats for basic projectile weapon
"""

# Projectile settings
PROJECTILE_SPEED = 300
PROJECTILE_SIZE = 8
PROJECTILE_DAMAGE = 25
PROJECTILE_LIFETIME = 2.0  # Seconds

# Weapon settings
BASE_ATTACK_COOLDOWN = 1.0  # Seconds between attacks
WEAPON_RANGE = 300  # Attack range

# Projectile appearance
from ..window import YELLOW
PROJECTILE_COLOR = YELLOW
