"""
Base Weapon
Abstract base class for all weapons with polymorphism
"""

from abc import ABC, abstractmethod


class BaseWeapon(ABC):
    """Base class for all weapons - handles cooldown and common logic"""

    def __init__(
        self, cooldown, damage, projectile_speed, range, level=1, auto_aim=True
    ):
        """
        Initialize base weapon

        Args:
            cooldown: Time between shots in seconds
            damage: Damage per projectile
            projectile_speed: Speed of projectiles
            range: Maximum targeting range
            level: Current weapon level (1-8)
            auto_aim: If True, weapon aims at enemies; if False, aims at mouse
        """
        self.cooldown = cooldown
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.range = range
        self.level = level
        self.auto_aim = auto_aim  # Determines aiming mode

        # Internal state
        self.cooldown_timer = 0.0

    def update_from_slot(
        self, dt, player, enemies, projectiles, mouse_world_pos, weapon_tip
    ):
        """
        Update weapon from slot (called by WeaponSlot)

        Args:
            dt: Delta time
            player: Player entity
            enemies: Enemy sprite group
            projectiles: Projectile sprite group
            mouse_world_pos: Mouse world position
            weapon_tip: Vector2 position of this slot's weapon tip
        """
        # Update cooldown
        self.cooldown_timer -= dt * player.attack_speed_multiplier

        # Check if ready to fire
        if self.cooldown_timer <= 0:
            if self.auto_aim:
                # Auto-aim at nearest enemy
                if self._try_fire_auto(player, enemies, projectiles, weapon_tip):
                    self.cooldown_timer = self.cooldown
            else:
                # Manual aim (spread weapon, laser, etc.)
                if self._try_fire_manual(
                    player, mouse_world_pos, projectiles, weapon_tip
                ):
                    self.cooldown_timer = self.cooldown

    def _try_fire_auto(self, player, enemies, projectiles, weapon_tip):
        """
        Try to fire at nearest enemy (auto-aim)

        Args:
            player: Player entity
            enemies: Enemy sprite group
            projectiles: Projectile sprite group
            weapon_tip: Weapon tip position for this slot

        Returns:
            bool: True if fired
        """
        # Find target from WEAPON TIP position, not player center! ✅
        target = self._find_target_from_position(weapon_tip, enemies)

        if target:
            self.fire_from_position(weapon_tip, target.position, projectiles)
            return True

        return False

    def _try_fire_manual(self, player, mouse_world_pos, projectiles, weapon_tip):
        """
        Try to fire at mouse position (manual aim)

        Args:
            player: Player entity
            mouse_world_pos: Mouse world position
            projectiles: Projectile sprite group
            weapon_tip: Weapon tip position for this slot

        Returns:
            bool: True if fired
        """
        self.fire_from_position(weapon_tip, mouse_world_pos, projectiles)
        return True

    @abstractmethod
    def fire_from_position(self, weapon_tip, target_pos, projectiles):
        """
        Fire the weapon from specific position - MUST be implemented by subclass

        Args:
            weapon_tip: Vector2 position to fire from
            target_pos: Vector2 position to fire toward
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

    def _find_target_from_position(self, position, enemies):
        """
        Find the closest enemy within range from specific position

        Args:
            position: Vector2 position to measure from (weapon tip)
            enemies: Sprite group of enemies

        Returns:
            Enemy or None: Closest enemy within range
        """
        closest_enemy = None
        closest_distance = self.range

        for enemy in enemies:
            distance = position.distance_to(enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy
