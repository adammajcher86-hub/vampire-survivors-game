"""
Weapon Slot System
Manages individual weapon slots with mount positions
"""

import pygame
import math


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

    def is_empty(self):
        """Check if slot is empty"""
        return self.weapon is None

    def equip_weapon(self, weapon, weapon_sprite):
        """
        Equip weapon to this slot

        Args:
            weapon: Weapon instance
            weapon_sprite: Pygame surface for weapon visual
        """
        self.weapon = weapon
        self.weapon_sprite = weapon_sprite
        self.rendered_weapon = weapon_sprite

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

    def update(
        self, dt, player, enemies, projectiles, mouse_world_pos, nearest_enemy_pos
    ):
        """
        Update weapon in this slot

        Args:
            dt: Delta time
            player: Player entity
            enemies: Enemy sprite group
            projectiles: Projectile sprite group
            mouse_world_pos: Mouse world position
            nearest_enemy_pos: Nearest enemy position (for auto-aim)
        """
        if not self.weapon:
            return

        # Update weapon rotation
        mount_pos = self.get_world_position(player)

        if hasattr(self.weapon, "auto_aim") and self.weapon.auto_aim:
            # Auto-aim: Rotate toward nearest enemy ✅
            if nearest_enemy_pos:
                delta_x = nearest_enemy_pos.x - mount_pos.x
                delta_y = nearest_enemy_pos.y - mount_pos.y

                angle_rad = math.atan2(delta_y, delta_x)
                self.weapon_angle = math.degrees(angle_rad)
        else:
            # Manual aim: Rotate toward mouse
            if mouse_world_pos:
                delta_x = mouse_world_pos.x - mount_pos.x
                delta_y = mouse_world_pos.y - mount_pos.y

                angle_rad = math.atan2(delta_y, delta_x)
                self.weapon_angle = math.degrees(angle_rad)

        # Rotate weapon sprite (for both auto and manual) ✅
        if self.weapon_sprite:
            self.rendered_weapon = pygame.transform.rotate(
                self.weapon_sprite, -self.weapon_angle
            )

        # Update weapon with slot-specific weapon tip position
        weapon_tip = self.get_weapon_tip_position(player)

        # Call weapon's update with weapon tip position
        self.weapon.update_from_slot(
            dt, player, enemies, projectiles, mouse_world_pos, weapon_tip
        )

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
