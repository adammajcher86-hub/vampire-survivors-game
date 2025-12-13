"""
Wave System Configuration
"""


class WaveConfig:
    """Wave system configuration"""

    # Wave timing
    REST_DURATION = 5.0  # seconds between waves

    # Starting difficulty
    BASE_ENEMIES = 11  # Wave 1 enemy count
    ENEMIES_PER_WAVE = 25  # Additional enemies each wave
    MAX_ENEMIES_PER_WAVE = 550  # Cap on enemies

    # Enemy composition (percentages per wave)
    WAVE_COMPOSITION = {
        1: {"BasicEnemy": 1.0},  # 100% basic
        2: {"BasicEnemy": 0.8, "FastEnemy": 0.2},
        3: {"BasicEnemy": 0.6, "FastEnemy": 0.3, "TankEnemy": 0.1},
        5: {"BasicEnemy": 0.4, "FastEnemy": 0.3, "TankEnemy": 0.2, "EliteEnemy": 0.1},
        10: {"BasicEnemy": 0.3, "FastEnemy": 0.3, "TankEnemy": 0.2, "EliteEnemy": 0.2},
    }

    # Use highest defined wave composition for later waves
    DEFAULT_COMPOSITION = {
        "BasicEnemy": 0.3,
        "FastEnemy": 0.3,
        "TankEnemy": 0.2,
        "EliteEnemy": 0.2,
    }

    # Spawn rate (enemies per second)
    BASE_SPAWN_RATE = 2.0  # Wave 1
    SPAWN_RATE_INCREASE = 0.2  # Per wave
    MAX_SPAWN_RATE = 15.0  # Cap
