"""
Base Weapon
Abstract base class for all weapons with polymorphism
"""

from abc import ABC, abstractmethod


class BaseWeapon(ABC):
    """Base class for all weapons - handles cooldown and common logic"""

    def __init__(self, cooldown, damage, projectile_speed, range, level=1):
        """
        Initialize base weapon

        Args:
            cooldown: Time between shots in seconds
            damage: Damage per projectile
            projectile_speed: Speed of projectiles
            range: Maximum targeting range
            level: Current weapon level (1-8)
        """
        self.cooldown = cooldown
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.range = range
        self.level = level

        # Internal state
        self.cooldown_timer = 0.0

    def update(self, dt, player, enemies, projectiles, mouse_world_pos):
        """
        Update weapon and fire if ready

        Args:
            dt: Delta time in seconds
            player: Player entity
            enemies: Sprite group of enemies
            projectiles: Sprite group to add new projectiles to
        """
        # Update cooldown
        self.cooldown_timer -= dt * player.attack_speed_multiplier

        # Check if ready to fire (timer reached 0 or below)
        if self.cooldown_timer <= 0:
            if self._try_fire(player, enemies, projectiles):
                self.cooldown_timer = self.cooldown

    def _try_fire(self, player, enemies, projectiles):
        """Attempt to fire weapon"""
        target = self._find_target(player, enemies)

        if target:
            self.fire(player, target, projectiles)
            return True

        return False

    def _find_target(self, player, enemies):
        """Find the closest enemy within range"""
        closest_enemy = None
        closest_distance = self.range

        for enemy in enemies:
            distance = player.position.distance_to(enemy.position)

            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
        return closest_enemy

    @abstractmethod
    def fire(self, player, target, projectiles):
        """
        Fire the weapon - MUST be implemented by subclass

        Args:
            player: Player entity (source position)
            target: Target enemy
            projectiles: Sprite group to add projectiles to
        """
        pass

    def level_up(self):
        """Level up the weapon - improve stats"""
        if self.level < 8:
            self.level += 1
            self._apply_level_up_bonus()

    def _apply_level_up_bonus(self):
        """Apply level up bonuses - can be overridden by subclasses"""
        # Base: 10% damage increase per level
        self.damage = int(self.damage * 1.1)

    def get_name(self):
        """Get weapon name - should be overridden"""
        return self.__class__.__name__
