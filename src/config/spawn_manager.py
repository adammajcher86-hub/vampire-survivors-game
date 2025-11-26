"""
Spawn Manager Configuration
Controls enemy spawning and difficulty scaling
"""

# Spawn settings
INITIAL_SPAWN_RATE = 2.0  # Seconds between spawns
MIN_SPAWN_RATE = 0.3
SPAWN_RATE_DECREASE = 0.95  # Multiplier per difficulty increase
MAX_ENEMIES = 500

# Spawn positioning
MIN_SPAWN_DISTANCE = 400  # Minimum distance from player
MAX_SPAWN_DISTANCE = 600  # Maximum distance from player

# Difficulty scaling
DIFFICULTY_INTERVAL = 60  # Seconds between difficulty increases
ENEMY_HEALTH_SCALE = 1.01  # Health multiplier per difficulty level
ENEMY_SPEED_SCALE = 1.005  # Speed multiplier per difficulty level
MAX_SPEED_SCALE = 1.5  # Cap on speed scaling