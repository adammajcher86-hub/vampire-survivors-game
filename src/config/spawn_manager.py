"""
Spawn Manager Configuration
Enemy spawning and difficulty scaling
"""


class SpawnManagerConfig:
    """Enemy spawning and difficulty settings"""

    # Spawn rates
    INITIAL_SPAWN_RATE = 0.5
    MIN_SPAWN_RATE = 0.3
    SPAWN_RATE_DECREASE = 0.95
    MAX_ENEMIES = 500

    # Spawn positioning
    MIN_SPAWN_DISTANCE = 400
    MAX_SPAWN_DISTANCE = 600

    # Difficulty scaling
    DIFFICULTY_INTERVAL = 60  # Seconds
    ENEMY_HEALTH_SCALE = 1.01
    ENEMY_SPEED_SCALE = 1.005
    MAX_SPEED_SCALE = 1.5

    # Enemy type distribution (percentage chances)
    BASIC_ENEMY_CHANCE = 0.70  # 70%
    FAST_ENEMY_CHANCE = 0.15  # 15%
    TANK_ENEMY_CHANCE = 0.10  # 10%
    ELITE_ENEMY_CHANCE = 0.05  # 5%
