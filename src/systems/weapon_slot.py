"""
Weapon Slot System
Manages individual weapon slots with mount positions
"""

import pygame
import math
from src.logger import logger


class WeaponSlot:
    """Represents a weapon slot with mount position"""

    def __init__(self, mount_offset):
        """
        Initialize weapon slot

        Args:
            mount_offset: Tuple (x, y) offset from player center
        """
        self.mount_offset = pygame.math.Vector2(mount_offset)
        self.weapon = None  # Weapon instance (None = empty)
        self.weapon_sprite = None  # Visual weapon sprite
        self.weapon_angle = 0  # Current weapon rotation
        self.rendered_weapon = None  # Rotated weapon sprite
        self.weapon_animation = None

    def is_empty(self):
        """Check if slot is empty"""
        return self.weapon is None

    def equip_weapon(self, weapon, weapon_sprite):
        """Equip weapon to this slot"""
        from src.systems.weapon_animation import WeaponFireAnimation

        self.weapon = weapon
        self.weapon_sprite = weapon_sprite
        self.rendered_weapon = weapon_sprite

        # ✅ Load animation based on weapon type (polymorphism!)
        animation_path = weapon.get_animation_sprite_path()

        if animation_path:
            try:
                config = weapon.get_animation_config()
                self.weapon_animation = WeaponFireAnimation(
                    animation_path,
                    frame_width=config["frame_width"],
                    frame_height=config["frame_height"],
                    frame_count=config["frame_count"],
                )
            except Exception:
                logger.warning("⚠️ Failed to load weapon animation: {e}")
                self.weapon_animation = None
        else:
            self.weapon_animation = None

        # Set callback
        if self.weapon:
            self.weapon.set_fire_callback(self.trigger_fire_animation)

    def unequip_weapon(self):
        """Remove weapon from slot"""
        self.weapon = None
        self.weapon_sprite = None
        self.rendered_weapon = None

    def get_world_position(self, player):
        """
        Calculate world position of this weapon mount

        Args:
            player: Player entity

        Returns:
            Vector2: World position of weapon mount
        """
        angle_rad = math.radians(player.angle)

        rotated_x = self.mount_offset.x * math.cos(
            angle_rad
        ) - self.mount_offset.y * math.sin(angle_rad)
        rotated_y = self.mount_offset.x * math.sin(
            angle_rad
        ) + self.mount_offset.y * math.cos(angle_rad)

        return pygame.math.Vector2(
            player.position.x + rotated_x, player.position.y + rotated_y
        )

    def get_weapon_tip_position(self, player, barrel_length=22):
        """
        Calculate weapon tip position (where projectiles spawn)

        Args:
            player: Player entity
            barrel_length: Length of weapon barrel

        Returns:
            Vector2: World position of weapon tip
        """
        mount_pos = self.get_world_position(player)

        weapon_angle_rad = math.radians(self.weapon_angle)

        tip_offset_x = barrel_length * math.cos(weapon_angle_rad)
        tip_offset_y = barrel_length * math.sin(weapon_angle_rad)

        return pygame.math.Vector2(
            mount_pos.x + tip_offset_x, mount_pos.y + tip_offset_y
        )

    def update(self, dt, player, enemies, projectiles, mouse_world_pos):
        """Update weapon in this slot"""
        if not self.weapon:
            return

        # Update fire animation ✅
        if self.weapon_animation:
            self.weapon_animation.update(dt)

        # Get this weapon's mount position
        mount_pos = self.get_world_position(player)

        # Find nearest enemy FROM THIS WEAPON'S POSITION
        nearest_enemy_pos = None
        if enemies and hasattr(self.weapon, "auto_aim") and self.weapon.auto_aim:
            nearest_enemy_pos = self._find_nearest_enemy(mount_pos, enemies)

        # Update weapon rotation
        if hasattr(self.weapon, "auto_aim") and self.weapon.auto_aim:
            if nearest_enemy_pos:
                delta_x = nearest_enemy_pos.x - mount_pos.x
                delta_y = nearest_enemy_pos.y - mount_pos.y
                angle_rad = math.atan2(delta_y, delta_x)
                self.weapon_angle = math.degrees(angle_rad)
        else:
            if mouse_world_pos:
                delta_x = mouse_world_pos.x - mount_pos.x
                delta_y = mouse_world_pos.y - mount_pos.y
                angle_rad = math.atan2(delta_y, delta_x)
                self.weapon_angle = math.degrees(angle_rad)

        # Choose sprite: animation frame or base sprite ✅
        current_sprite = self.weapon_sprite
        if self.weapon_animation and self.weapon_animation.is_animating():
            current_sprite = self.weapon_animation.get_current_frame()

            # ✅ Choose sprite: animation or base
            current_sprite = self.weapon_sprite
            if self.weapon_animation and self.weapon_animation.is_animating():
                current_sprite = self.weapon_animation.get_current_frame()

        # Rotate weapon sprite
        self.rendered_weapon = pygame.transform.rotate(
            current_sprite, -self.weapon_angle
        )

        # Update weapon with slot-specific weapon tip position
        weapon_tip = self.get_weapon_tip_position(player)

        # Track if weapon fired this frame
        # was_ready = self.weapon.cooldown_timer <= 0

        # Call weapon's update
        self.weapon.update_from_slot(
            dt, player, enemies, projectiles, mouse_world_pos, weapon_tip
        )
        # ✅ Trigger animation if fired
        """if was_ready and self.weapon.cooldown_timer > 0:
            if self.weapon_animation:
                self.weapon_animation.start()
        # If weapon just fired, trigger animation ✅
        is_ready_now = self.weapon.cooldown_timer > 0
        if was_ready and is_ready_now:
            self.trigger_fire_animation()"""

    def render(self, screen, camera):
        """
        Render weapon sprite at mount position

        Args:
            screen: Pygame surface
            camera: Camera for world-to-screen conversion
        """
        if not self.rendered_weapon:
            return

        # This is handled by Player.render() to maintain draw order
        pass

    def _find_nearest_enemy(self, position, enemies):
        """
        Find nearest enemy to this weapon's position

        Args:
            position: Vector2 position to measure from (weapon mount)
            enemies: Enemy sprite group

        Returns:
            Vector2: Position of nearest enemy, or None
        """
        if not enemies:
            return None

        nearest_enemy = None
        nearest_distance = float("inf")

        for enemy in enemies:
            distance = position.distance_to(enemy.position)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        return nearest_enemy.position if nearest_enemy else None

    def trigger_fire_animation(self):
        """Start fire animation"""
        if self.weapon_animation:
            self.weapon_animation.start()
