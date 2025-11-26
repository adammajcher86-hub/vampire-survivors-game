"""
Spawn Manager Configuration
Enemy spawning and difficulty scaling
"""

class SpawnManagerConfig:
    """Enemy spawning and difficulty settings"""

    # Spawn rates
    INITIAL_SPAWN_RATE = 2.0
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
    BASIC_ENEMY_CHANCE = 0.70   # 70%
    FAST_ENEMY_CHANCE = 0.15    # 15%
    TANK_ENEMY_CHANCE = 0.10    # 10%
    ELITE_ENEMY_CHANCE = 0.05   # 5%

    @classmethod
    def calculate_scaled_health(cls, base_health, difficulty_level):
        """Calculate scaled health based on difficulty"""
        return base_health * (cls.ENEMY_HEALTH_SCALE ** difficulty_level)

    @classmethod
    def calculate_scaled_speed(cls, base_speed, difficulty_level):
        """Calculate scaled speed based on difficulty (with cap)"""
        scaled = base_speed * (cls.ENEMY_SPEED_SCALE ** difficulty_level)
        return min(scaled, base_speed * cls.MAX_SPEED_SCALE)