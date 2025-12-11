"""
Chain Laser Projectile
A continuous beam that locks onto enemies, deals damage over time, and can chain to nearby enemies
"""

import pygame
from src.config.weapons.chain_laser import ChainLaserConfig


class ChainLaserProjectile:
    """
    Continuous beam weapon that locks onto enemies
    Not a sprite - managed directly by the weapon
    """

    def __init__(self, origin_pos, primary_target, weapon_level=1):
        """
        Initialize chain laser beam

        Args:
            origin_pos: Vector2 starting position (weapon tip)
            primary_target: Initial enemy to lock onto
            weapon_level: Current weapon level (affects chains and damage)
        """
        self.origin_pos = origin_pos.copy()
        self.primary_target = primary_target
        self.weapon_level = weapon_level

        # Chain targets
        self.chain_targets = []  # List of chained enemies
        self.max_chains = ChainLaserConfig.get_max_chains(weapon_level)

        # Damage tracking
        self.damage_per_second = ChainLaserConfig.get_damage_per_second(weapon_level)
        self.damage_accumulated = 0.0  # Track fractional damage

        # Visual
        self.beam_segments = []  # List of (start, end) tuples for rendering

    def update(self, dt, origin_pos, enemies):
        """
        Update beam state

        Args:
            dt: Delta time
            origin_pos: Current weapon tip position
            enemies: Sprite group of enemies

        Returns:
            bool: True if beam is still active, False if should be removed
        """
        self.origin_pos = origin_pos.copy()

        # Check if primary target is still alive and in range
        if not self._is_valid_target(self.primary_target):
            return False  # Beam expires

        # Update chain targets if enabled
        if ChainLaserConfig.can_chain(self.weapon_level):
            self._update_chain_targets(enemies)

        # Deal damage to all targets
        self._deal_damage(dt)

        # Update beam segments for rendering
        self._update_beam_segments()

        return True

    def _is_valid_target(self, enemy):
        """Check if enemy is alive and in range"""
        if enemy is None or not enemy.alive():
            return False

        distance = self.origin_pos.distance_to(enemy.position)
        return distance <= ChainLaserConfig.RANGE

    def _update_chain_targets(self, enemies):
        """Find and update chain targets"""
        self.chain_targets = []

        if self.max_chains == 0:
            return

        # Start from primary target
        current_target = self.primary_target
        checked_enemies = {self.primary_target}

        for _ in range(self.max_chains):
            # Find nearest enemy to current target
            next_target = self._find_nearest_unchained_enemy(
                current_target, enemies, checked_enemies
            )

            if next_target is None:
                break

            self.chain_targets.append(next_target)
            checked_enemies.add(next_target)
            current_target = next_target

    def _find_nearest_unchained_enemy(self, from_enemy, enemies, exclude_set):
        """Find nearest enemy within chain range"""
        closest_enemy = None
        closest_distance = ChainLaserConfig.CHAIN_RANGE

        for enemy in enemies:
            if enemy in exclude_set or not enemy.alive():
                continue

            distance = from_enemy.position.distance_to(enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def _deal_damage(self, dt):
        """Deal damage over time to all locked targets"""
        # Calculate damage for this frame
        frame_damage = self.damage_per_second * dt
        self.damage_accumulated += frame_damage

        # Deal integer damage when accumulated >= 1
        damage_to_deal = int(self.damage_accumulated)
        if damage_to_deal > 0:
            self.damage_accumulated -= damage_to_deal

            # Damage primary target
            if self.primary_target.alive():
                self.primary_target.take_damage(damage_to_deal)

            # Damage chain targets (50% damage for chains)
            chain_damage = max(1, damage_to_deal // 2)
            for target in self.chain_targets:
                if target.alive():
                    target.take_damage(chain_damage)

    def _update_beam_segments(self):
        """Update beam segments for rendering"""
        self.beam_segments = []

        # Primary beam: origin -> primary target
        if self.primary_target.alive():
            self.beam_segments.append((self.origin_pos, self.primary_target.position))

        # Chain beams: target -> target
        prev_target = self.primary_target
        for target in self.chain_targets:
            if target.alive():
                self.beam_segments.append((prev_target.position, target.position))
                prev_target = target

    def render(self, screen, camera):
        """Render all beam segments"""
        for start_pos, end_pos in self.beam_segments:
            screen_start = camera.apply(start_pos)
            screen_end = camera.apply(end_pos)

            # Draw glow
            pygame.draw.line(
                screen,
                ChainLaserConfig.BEAM_GLOW_COLOR,
                (int(screen_start.x), int(screen_start.y)),
                (int(screen_end.x), int(screen_end.y)),
                ChainLaserConfig.BEAM_GLOW_WIDTH,
            )

            # Draw core beam
            pygame.draw.line(
                screen,
                ChainLaserConfig.BEAM_COLOR,
                (int(screen_start.x), int(screen_start.y)),
                (int(screen_end.x), int(screen_end.y)),
                ChainLaserConfig.BEAM_WIDTH,
            )
