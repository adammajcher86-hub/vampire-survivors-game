"""
Weapon System
Handles automatic weapon firing and targeting
"""

from src.config import BaseWeaponConfig
from src.entities.projectile import Projectile


class WeaponSystem:
    """Manages weapon firing and projectiles"""

    def __init__(self):
        self.attack_cooldown = BaseWeaponConfig.ATTACK_COOLDOWN
        self.attack_timer = 0.0
        self.range = BaseWeaponConfig.RANGE

        # Projectile properties
        self.projectile_speed = BaseWeaponConfig.PROJECTILE_SPEED
        self.projectile_damage = BaseWeaponConfig.PROJECTILE_DAMAGE
        self.projectile_color = BaseWeaponConfig.PROJECTILE_COLOR
        self.projectile_size = BaseWeaponConfig.PROJECTILE_SIZE

    def update(self, dt, player, enemies, projectiles):
        """
        Update weapon system and fire when ready

        Args:
            dt: Delta time in seconds
            player: Player entity
            enemies: Sprite group of enemies
            projectiles: Sprite group to add new projectiles to
        """
        # Update attack timer
        self.attack_timer += dt

        # Check if ready to attack
        if self.attack_timer >= self.attack_cooldown:
            self._try_attack(player, enemies, projectiles)
            self.attack_timer = 0.0

    def _try_attack(self, player, enemies, projectiles):
        """
        Attempt to attack nearest enemy

        Args:
            player: Player entity
            enemies: Sprite group of enemies
            projectiles: Sprite group to add new projectile to
        """
        # Find closest enemy in range
        target = self._find_closest_enemy(player, enemies)

        if target:
            # Create projectile aimed at target
            projectile = Projectile(
                player.position.x,
                player.position.y,
                target.position,
                damage=self.projectile_damage,
                speed=self.projectile_speed,
                color=self.projectile_color,
                size=self.projectile_size,
            )
            projectiles.add(projectile)

    def _find_closest_enemy(self, player, enemies):
        """
        Find the closest enemy within range

        Args:
            player: Player entity
            enemies: Sprite group of enemies

        Returns:
            Enemy or None: Closest enemy within range, or None if no enemies in range
        """
        closest_enemy = None
        closest_distance = self.range

        for enemy in enemies:
            distance = player.position.distance_to(enemy.position)
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def check_projectile_collisions(self, projectiles, enemies):
        """
        Check and handle projectile-enemy collisions

        Args:
            projectiles: Sprite group of projectiles
            enemies: Sprite group of enemies

        Returns:
            int: Number of enemies killed
        """
        enemies_killed = 0

        # Check each projectile against each enemy
        for projectile in list(projectiles):
            hit_enemy = False

            for enemy in list(enemies):
                if projectile.collides_with(enemy):
                    # Damage enemy
                    if enemy.take_damage(projectile.damage):
                        # Enemy died
                        enemies_killed += 1

                    # Remove projectile (it hit something)
                    projectiles.remove(projectile)
                    hit_enemy = True
                    break

            if hit_enemy:
                continue

        return enemies_killed

    def remove_expired_projectiles(self, projectiles):
        """
        Remove projectiles that have exceeded their lifetime

        Args:
            projectiles: Sprite group of projectiles
        """
        for projectile in list(projectiles):
            if projectile.is_expired():
                projectiles.remove(projectile)
