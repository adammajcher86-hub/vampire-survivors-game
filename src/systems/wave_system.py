"""
Wave System
Manages wave progression, enemy spawning, and difficulty scaling
"""

import random
from src.config.wave_system import WaveConfig
from src.logger import logger


class WaveSystem:
    """Manages wave-based gameplay"""

    def __init__(self):
        """Initialize wave system"""
        self.current_wave = 0
        self.wave_active = False
        self.wave_complete = False

        # Enemy tracking
        self.enemies_to_spawn = 0
        self.enemies_spawned = 0
        self.enemies_killed_this_wave = 0

        # Rest period
        self.rest_timer = 0.0
        self.in_rest_period = False

        # Spawn timing
        self.spawn_timer = 0.0
        self.spawn_rate = WaveConfig.BASE_SPAWN_RATE

        # Start first wave after brief delay
        self.rest_timer = 3.0
        self.in_rest_period = True

    def start_wave(self):
        """Start a new wave"""
        self.current_wave += 1
        self.wave_active = True
        self.wave_complete = False
        self.in_rest_period = False

        # Calculate enemies for this wave
        self.enemies_to_spawn = min(
            WaveConfig.BASE_ENEMIES
            + (self.current_wave - 1) * WaveConfig.ENEMIES_PER_WAVE,
            WaveConfig.MAX_ENEMIES_PER_WAVE,
        )

        self.enemies_spawned = 0
        self.enemies_killed_this_wave = 0

        # Calculate spawn rate for this wave
        self.spawn_rate = min(
            WaveConfig.BASE_SPAWN_RATE
            + (self.current_wave - 1) * WaveConfig.SPAWN_RATE_INCREASE,
            WaveConfig.MAX_SPAWN_RATE,
        )

        self.spawn_timer = 0.0

        logger.info(f"🌊 WAVE {self.current_wave} START!")
        logger.info(
            f"Enemies: {self.enemies_to_spawn}, Spawn rate: {self.spawn_rate:.1f}/s"
        )

    def update(self, dt, enemies):
        """
        Update wave system

        Args:
            dt: Delta time
            enemies: Enemy sprite group

        Returns:
            str or None: Enemy type to spawn, or None
        """
        # Handle rest period
        if self.in_rest_period:
            self.rest_timer -= dt
            if self.rest_timer <= 0:
                self.start_wave()
            return None

        # Check if wave is complete
        if self.wave_active and not self.wave_complete:
            # All enemies spawned and all killed?
            if self.enemies_spawned >= self.enemies_to_spawn and len(enemies) == 0:
                self._complete_wave()
                return None

        # Spawn enemies if wave active
        if self.wave_active and self.enemies_spawned < self.enemies_to_spawn:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_timer = 1.0 / self.spawn_rate
                self.enemies_spawned += 1

                # Return enemy type to spawn
                return self._get_enemy_type()

        return None

    def on_enemy_killed(self):
        """Call when an enemy is killed"""
        self.enemies_killed_this_wave += 1

    def _complete_wave(self):
        """Complete current wave"""
        self.wave_complete = True
        self.wave_active = False
        self.in_rest_period = True
        self.rest_timer = WaveConfig.REST_DURATION

        logger.info(f"✅ WAVE {self.current_wave} COMPLETE!")
        logger.info(f"Enemies killed: {self.enemies_killed_this_wave}")
        logger.info(f"Next wave in {WaveConfig.REST_DURATION}s...")

    def _get_enemy_type(self):
        """
        Get enemy type to spawn based on wave composition

        Returns:
            str: Enemy class name
        """
        # Get composition for current wave (or closest lower wave)
        composition = None
        for wave_num in sorted(WaveConfig.WAVE_COMPOSITION.keys(), reverse=True):
            if self.current_wave >= wave_num:
                composition = WaveConfig.WAVE_COMPOSITION[wave_num]
                break

        if composition is None:
            composition = WaveConfig.DEFAULT_COMPOSITION

        # Random selection based on weights
        rand = random.random()
        cumulative = 0.0

        for enemy_type, weight in composition.items():
            cumulative += weight
            if rand <= cumulative:
                return enemy_type

        # Fallback
        return "BasicEnemy"

    def get_progress(self):
        """
        Get wave progress

        Returns:
            dict: Wave progress data
        """
        return {
            "wave": self.current_wave,
            "active": self.wave_active,
            "complete": self.wave_complete,
            "in_rest": self.in_rest_period,
            "rest_timer": self.rest_timer,
            "enemies_spawned": self.enemies_spawned,
            "enemies_to_spawn": self.enemies_to_spawn,
            "enemies_remaining": self.enemies_to_spawn - self.enemies_killed_this_wave,
        }
