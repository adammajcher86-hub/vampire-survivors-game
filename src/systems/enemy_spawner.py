"""
Enemy Spawner System
Handles spawning of enemies around the player
"""

import random
import math
from src.config import SpawnManagerConfig
from src.entities import BasicEnemy, FastEnemy, TankEnemy, EliteEnemy


class EnemySpawner:
    """Manages enemy spawning"""

    def __init__(self):
        self.spawn_timer = 0.0
        self.spawn_rate = SpawnManagerConfig.INITIAL_SPAWN_RATE
        self.difficulty_timer = 0.0
        self.difficulty_level = 0

    def update(self, dt, player_position, enemies):
        """
        Update spawner and spawn enemies

        Args:
            dt: Delta time in seconds
            player_position: Vector2 of player position
            enemies: Sprite group to add enemies to
        """
        # Update difficulty over time
        self.difficulty_timer += dt
        if self.difficulty_timer >= SpawnManagerConfig.DIFFICULTY_INTERVAL:
            self.difficulty_timer = 0.0
            self.difficulty_level += 1
            self._increase_difficulty()

        # Check if we should spawn
        self.spawn_timer += dt
        if (
            self.spawn_timer >= self.spawn_rate
            and len(enemies) < SpawnManagerConfig.MAX_ENEMIES
        ):
            self.spawn_timer = 0.0
            self._spawn_enemy(player_position, enemies)

    def _increase_difficulty(self):
        """Increase difficulty by reducing spawn rate"""
        self.spawn_rate *= SpawnManagerConfig.SPAWN_RATE_DECREASE
        if self.spawn_rate < SpawnManagerConfig.MIN_SPAWN_RATE:
            self.spawn_rate = SpawnManagerConfig.MIN_SPAWN_RATE

        print(
            f"Difficulty increased! Level {self.difficulty_level}, Spawn rate: {self.spawn_rate:.2f}s"
        )

    def _spawn_enemy(self, player_position, enemies):
        """
        Spawn a random enemy around the player

        Args:
            player_position: Vector2 of player position
            enemies: Sprite group to add enemy to
        """
        # Choose random spawn position around player
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(
            SpawnManagerConfig.MIN_SPAWN_DISTANCE, SpawnManagerConfig.MAX_SPAWN_DISTANCE
        )

        spawn_x = player_position.x + math.cos(angle) * distance
        spawn_y = player_position.y + math.sin(angle) * distance

        # Choose enemy type based on distribution
        enemy = self._create_random_enemy(spawn_x, spawn_y)
        enemies.add(enemy)

    def _create_random_enemy(self, x, y):
        """
        Create a random enemy type based on spawn chances

        Args:
            x: Spawn x position
            y: Spawn y position

        Returns:
            Enemy instance
        """
        roll = random.random()

        if roll < SpawnManagerConfig.BASIC_ENEMY_CHANCE:
            return BasicEnemy(x, y)
        elif (
            roll
            < SpawnManagerConfig.BASIC_ENEMY_CHANCE
            + SpawnManagerConfig.FAST_ENEMY_CHANCE
        ):
            return FastEnemy(x, y)
        elif roll < (
            SpawnManagerConfig.BASIC_ENEMY_CHANCE
            + SpawnManagerConfig.FAST_ENEMY_CHANCE
            + SpawnManagerConfig.TANK_ENEMY_CHANCE
        ):
            return TankEnemy(x, y)
        else:
            return EliteEnemy(x, y)
