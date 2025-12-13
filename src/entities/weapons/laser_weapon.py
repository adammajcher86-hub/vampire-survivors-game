"""
Laser Weapon
Instant beam weapon with bouncing mechanic
"""

import pygame
from src.entities.weapons.base_weapon import BaseWeapon
from src.entities.beams.laser_beam import LaserBeam
from src.config.weapons.laser_weapon import LaserWeaponConfig


class LaserWeapon(BaseWeapon):
    """Laser weapon - instant beam with bouncing"""

    def __init__(self):
        super().__init__(
            cooldown=LaserWeaponConfig.FIRE_COOLDOWN,
            damage=LaserWeaponConfig.DAMAGE,
            projectile_speed=0,  # Instant (no travel)
            range=LaserWeaponConfig.RANGE,
            level=1,
            auto_aim=True,
        )

        self.beam_color = LaserWeaponConfig.BEAM_COLOR
        self.beam_width = LaserWeaponConfig.BEAM_WIDTH
        self.bounce_count = LaserWeaponConfig.BASE_BOUNCES  # Upgradeable!
        self.bounce_range = LaserWeaponConfig.BOUNCE_RANGE
        self.active_beams = []  # Store active beam visuals
        self.pending_damage = []  # ✅ CRITICAL - stores damage info
        self.all_enemies = None  # Reference to enemy group

    def update_from_slot(
        self, dt, player, enemies, projectiles, mouse_world_pos, weapon_tip
    ):
        """Override to store enemy reference"""
        self.all_enemies = enemies
        super().update_from_slot(
            dt, player, enemies, projectiles, mouse_world_pos, weapon_tip
        )

    def fire_from_position(self, weapon_tip, target_pos, projectiles):
        """Fire laser beam with bouncing mechanic"""
        if not self.all_enemies:
            return

        # Find chain of targets
        chain = self._find_bounce_chain(weapon_tip, target_pos)

        if not chain:
            return

        # Create visual beams for each segment
        for i in range(len(chain) - 1):
            beam = LaserBeam(
                chain[i],
                chain[i + 1],
                damage_per_second=self.damage,
                color=self.beam_color,
                width=self.beam_width,
            )
            self.active_beams.append(beam)

        # ✅ CRITICAL - Store damage info for game_engine
        self.pending_damage.append(
            {
                "targets": [pos for pos in chain[1:]],  # Skip weapon tip
                "damage": self.damage,
            }
        )

    def _find_bounce_chain(self, weapon_tip, first_target_pos):
        """Find chain of enemies for laser to bounce through"""
        chain = [pygame.math.Vector2(weapon_tip)]
        hit_enemies = set()

        # Find first enemy
        first_enemy = self._find_enemy_at_position(first_target_pos)
        if not first_enemy:
            return []

        chain.append(pygame.math.Vector2(first_enemy.position))
        hit_enemies.add(id(first_enemy))

        # Find bounce targets
        current_pos = first_enemy.position
        for _ in range(self.bounce_count):
            next_enemy = self._find_nearest_enemy_from_position(
                current_pos, hit_enemies, max_range=self.bounce_range
            )

            if not next_enemy:
                break

            chain.append(pygame.math.Vector2(next_enemy.position))
            hit_enemies.add(id(next_enemy))
            current_pos = next_enemy.position

        return chain

    def _find_enemy_at_position(self, position):
        """Find enemy at given position"""
        if not self.all_enemies:
            return None

        for enemy in self.all_enemies:
            if enemy.position.distance_to(position) < 30:
                return enemy
        return None

    def _find_nearest_enemy_from_position(self, position, exclude_ids, max_range):
        """Find nearest enemy from position (for bouncing)"""
        if not self.all_enemies:
            return None

        nearest_enemy = None
        nearest_distance = max_range

        for enemy in self.all_enemies:
            if id(enemy) in exclude_ids:
                continue

            distance = position.distance_to(enemy.position)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        return nearest_enemy

    def update_beams(self, dt):
        """Update and clean up beams"""
        self.active_beams = [beam for beam in self.active_beams if beam.update(dt)]

    def render_beams(self, screen, camera):
        """Render all active beams"""
        for beam in self.active_beams:
            beam.render(screen, camera)

    def get_pending_damage(self):
        """✅ CRITICAL - Get and clear pending damage"""
        damage = self.pending_damage.copy()
        self.pending_damage.clear()
        return damage

    def _apply_level_up_bonus(self):
        """Apply level up bonuses - increase bounces!"""
        self.damage = int(self.damage * 1.1)

        # Every 2 levels, add a bounce
        if self.level % 2 == 0:
            self.bounce_count += 1
            from src.logger import logger

            logger.info(
                f"⚡ Laser bounces increased to {self.bounce_count + 1} targets!"
            )

    def get_animation_sprite_path(self):
        """Use same animation as basic weapon for now"""
        return "src/assets/sprites/weapon_basic_firing.png"

    def get_animation_config(self):
        """Use 3-frame animation"""
        return {"frame_width": 32, "frame_height": 16, "frame_count": 3}

    def get_name(self):
        return "Laser Weapon"
