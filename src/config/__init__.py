"""
Configuration Package
Centralizes all game configuration settings

Usage:
    from src.config import SCREEN_WIDTH, PLAYER_SPEED, ENEMY_HEALTH
    # or
    from src.config.player import PLAYER_SPEED
"""

# Window and display
from .window import *

# General game settings
from .game import *

# Player configuration
from .player import *

# Enemy configurations
from .enemies import *

# Weapon configurations
from .weapons import *

# Spawn manager
from .spawn_manager import *