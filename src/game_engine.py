"""
Main Game Engine
Manages game state, entities, and systems
"""

import pygame
import math
from src.config import WindowConfig, FastEnemyConfig
from src.entities import Player, BasicWeapon
from src.camera import Camera
from src.logger import logger
from src.systems import EnemySpawner, XPSystem, UpgradeSystem, PickupManager, WaveSystem
from src.ui import UpgradeMenu
from src.entities.projectiles import BombProjectile, LaserProjectile
from src.config.enemies.tank_laser import TankLaserConfig
from src.config.enemies.fast_laser import FastLaserConfig
from src.rendering import GameRenderer
from src.systems.effects import EffectManager


class Game:
    """Main game controller"""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = True
        self.game_over = False

        # Game time tracking
        self.game_time = 0.0

        # ✅ Initialize renderer EARLY
        self.renderer = GameRenderer(screen)

        # ✅ Initialize effect manager
        self.effect_manager = EffectManager()

        # Initialize camera
        self.camera = Camera(WindowConfig.WIDTH, WindowConfig.HEIGHT)

        # Initialize player at center of screen
        self.player = Player(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2)

        # Entity groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Enemy management
        self.enemies = pygame.sprite.Group()
        self.enemy_spawner = EnemySpawner()

        # Weapon system - POLYMORPHIC LIST!
        self.weapons = [BasicWeapon()]  # Start with basic weapon
        self.projectiles = pygame.sprite.Group()

        # XP system
        self.xp_system = XPSystem()
        self.pickups = pygame.sprite.Group()
        self.pickup_manager = PickupManager()

        # Upgrade system
        self.upgrade_system = UpgradeSystem()
        self.upgrade_menu = UpgradeMenu()
        self.wave_system = WaveSystem()

        # Game stats
        self.enemies_killed = 0
        self.xp_collected = 0  # Track total XP collected

        # Sprite groups
        self.enemy_projectiles = pygame.sprite.Group()  # Enemy projectiles
        self.bombs = pygame.sprite.Group()  # Bomb entities

        # Mouse tracking
        self.mouse_screen_pos = pygame.math.Vector2(0, 0)
        self.mouse_world_pos = pygame.math.Vector2(0, 0)

        # Debug
        self.last_debug_time = 0
        self.DEBUG_INTERVAL = 1000
        self.debug_mode = False
        self.logID = 0

        # Clock for FPS
        self.clock = pygame.time.Clock()

        print("Game initialized!")
        print(f"Window: {WindowConfig.WIDTH}x{WindowConfig.HEIGHT}")
        print(f"FPS: {WindowConfig.FPS}")
        print("Controls: WASD or Arrow Keys to move, ESC to pause")
        print("Starting weapon: Basic Weapon (auto-aim)")
        print("Collect XP to level up!")
        self.last_debug_time = 0

    def handle_event(self, event):
        """Handle game events"""

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right click
                self.player.place_bomb(self.bombs)

        # Handle game over input
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()
                    return
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

        # Handle upgrade menu input
        if self.upgrade_menu.active:
            selected_index = self.upgrade_menu.handle_input(event)
            if selected_index is not None:
                self._apply_upgrade(selected_index)
                return

        # Normal game input
        if event.type == pygame.KEYDOWN:
            # Dash with Spacebar
            if event.key == pygame.K_SPACE:
                keys = pygame.key.get_pressed()
                dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (
                    keys[pygame.K_a] or keys[pygame.K_LEFT]
                )
                dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (
                    keys[pygame.K_w] or keys[pygame.K_UP]
                )
                self.player.try_dash(dx, dy)

            # Pause
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                logger.info(f"Game {'paused' if self.paused else 'resumed'}")

            # Debug mode toggle
            if event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
                logger.info(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

        # Debug logging
        current_time = pygame.time.get_ticks()
        if current_time - self.last_debug_time >= self.DEBUG_INTERVAL:
            logger.debug(
                f"Entities - Enemies: {len(self.enemies)}, "
                f"Projectiles: {len(self.projectiles)}, "
                f"Enemy Projectiles: {len(self.enemy_projectiles)}, "
                f"Pickups: {len(self.pickups)}"
            )
            self.last_debug_time = current_time

    def update(self, dt):
        """Update game state"""
        if self.paused or self.game_over:
            return

        self.game_time += dt

        # Update mouse positions
        self.mouse_screen_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mouse_world_pos = pygame.math.Vector2(
            self.mouse_screen_pos.x + self.camera.offset.x,
            self.mouse_screen_pos.y + self.camera.offset.y,
        )

        # Get player input
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (
            keys[pygame.K_w] or keys[pygame.K_UP]
        )

        # Update player
        self.player.update(dt, dx, dy, self.mouse_world_pos)

        # ✅ Update all weapon slots with CUMULATIVE tracking
        for slot_index, slot in enumerate(self.player.weapon_slots):
            if not slot.is_empty():
                # Update weapon
                slot.update(
                    dt,
                    self.player,
                    self.enemies,
                    self.projectiles,
                    self.mouse_world_pos,
                )

                # Update beams
                if hasattr(slot.weapon, "update_beams"):
                    slot.weapon.update_beams(dt)

                # Apply laser damage
                if hasattr(slot.weapon, "get_pending_damage"):
                    damage_events = slot.weapon.get_pending_damage()

                    for damage_event in damage_events:
                        self._apply_laser_damage(damage_event)

        # ✅ Update effects (particles, screen shake)
        self.effect_manager.update(dt)

        # ✅ Update camera with screen shake
        shake_offset = self.effect_manager.get_shake_offset()
        self.camera.update(self.player, shake_offset)

        # Update enemy spawner
        enemy_type_to_spawn = self.wave_system.update(dt, self.enemies)
        if enemy_type_to_spawn:
            self.enemy_spawner.spawn_enemy_by_type(
                enemy_type_to_spawn, self.player.position, self.enemies
            )

        # Update all enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player.position)

        # Check enemy shooting
        self._check_enemy_shooting()

        # Check FastEnemy explosions
        self._check_fast_enemy_explosions()

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
        for projectile in self.enemy_projectiles:
            projectile.update(dt)

        # Update bombs
        for bomb in self.bombs:
            bomb.update(dt)

        # Update all pickups (magnetic pull, animations)
        for pickup in self.pickups:
            pickup.update(dt, self.player)

        # Check bomb explosions
        self._check_bomb_explosions()

        # Check collisions
        self._check_projectile_collisions()
        self._check_enemy_projectile_collisions()

        # Remove expired projectiles
        for projectile in list(self.projectiles):
            if projectile.is_expired():
                self.projectiles.remove(projectile)

        for projectile in list(self.enemy_projectiles):
            if projectile.is_expired():
                self.enemy_projectiles.remove(projectile)

        # Check player-enemy collisions
        self._check_player_enemy_collisions()

        # Handle pickup collection
        collected_xp = self.pickup_manager.collect_pickups(self.player, self.pickups)
        if collected_xp > 0:
            self.xp_collected += collected_xp
            if self.xp_system.update(dt, collected_xp):
                # Level up effect
                self.effect_manager.level_up(self.player.position)
                self._show_upgrade_menu()

        # Check game over
        if self.player.health <= 0:
            self.game_over = True
            logger.info("💀 GAME OVER!")

    def _check_projectile_collisions(self):
        """Check player projectile-enemy collisions"""
        for projectile in list(self.projectiles):
            # Special handling for bombs (area damage)
            if isinstance(projectile, BombProjectile):
                continue

            hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies, False)

            for enemy in hit_enemies:
                # ✅ Hit effect
                direction = (
                    projectile.velocity.normalize()
                    if projectile.velocity.length() > 0
                    else pygame.math.Vector2(1, 0)
                )
                self.effect_manager.projectile_hit(enemy.position, direction)

                # Apply damage
                enemy.take_damage(projectile.damage)
                self.projectiles.remove(projectile)

                # Check if enemy died
                if enemy.health <= 0:
                    self._handle_enemy_death(enemy)
                    self.wave_system.on_enemy_killed()

                break  # Projectile hits only one enemy

    def _check_enemy_shooting(self):
        """Check for enemies ready to shoot and spawn projectiles"""
        for enemy in self.enemies:
            # Check if tank is ready to shoot
            if hasattr(enemy, "should_shoot") and enemy.should_shoot():
                # Get shot data
                shot_data = enemy.get_shot_data()

                # Create laser projectile
                laser = LaserProjectile(
                    shot_data["position"].x,
                    shot_data["position"].y,
                    shot_data["target"],
                    TankLaserConfig,
                )

                # Add to enemy projectiles group
                self.enemy_projectiles.add(laser)

                # Reset enemy shoot state
                enemy.reset_shoot_state()

                logger.debug("💥 Tank fired laser!")

    def _check_enemy_projectile_collisions(self):
        """Check collisions between enemy projectiles and player"""
        for projectile in list(self.enemy_projectiles):
            # Check if laser hits player
            if projectile.collides_with(self.player):
                # Use projectile damage method (has immunity)
                if self.player.take_projectile_damage(projectile.damage):
                    # ✅ Player damage effect
                    self.effect_manager.player_damage()
                    logger.info(f"⚡ Player hit by laser! -{projectile.damage} HP")

                # Remove projectile
                self.enemy_projectiles.remove(projectile)

    def _check_fast_enemy_explosions(self):
        """Check for FastEnemy explosions and spawn radial lasers"""
        for enemy in list(self.enemies):
            # Check if FastEnemy should explode
            if hasattr(enemy, "should_explode") and enemy.should_explode():
                explosion_pos = enemy.get_explosion_position()

                # ✅ Explosion effect (smaller than bomb)
                self.effect_manager.particle_system.emit_explosion(
                    explosion_pos.x,
                    explosion_pos.y,
                    count=30,
                    color=(50, 200, 50),  # Green
                    speed=250,
                    size=4,
                    lifetime=0.8,
                )
                self.effect_manager.screen_shake.add_trauma(0.3)

                # Spawn 8 lasers in all directions
                laser_count = FastEnemyConfig.EXPLOSION_LASER_COUNT

                for i in range(laser_count):
                    angle = (i / laser_count) * 2 * math.pi

                    # Calculate direction for this laser
                    target_offset = pygame.math.Vector2(
                        math.cos(angle) * 100,
                        math.sin(angle) * 100,
                    )
                    target_pos = explosion_pos + target_offset

                    # Create laser
                    laser = LaserProjectile(
                        explosion_pos.x, explosion_pos.y, target_pos, FastLaserConfig
                    )

                    self.enemy_projectiles.add(laser)

                # Handle enemy death
                self._handle_enemy_death(enemy)
                self.wave_system.on_enemy_killed()

                logger.info("💥 FastEnemy EXPLODED! 8 lasers fired!")

    def _check_bomb_explosions(self):
        """Check for bomb explosions and apply area damage"""
        for bomb in list(self.bombs):
            if bomb.is_expired():
                # ✅ Bomb explosion effect
                self.effect_manager.bomb_explosion(bomb.position)

                # Apply area damage
                for enemy in self.enemies:
                    distance = enemy.position.distance_to(bomb.position)
                    if distance <= bomb.explosion_radius:
                        enemy.take_damage(bomb.damage)

                        if enemy.health <= 0:
                            self._handle_enemy_death(enemy)
                            self.wave_system.on_enemy_killed()

                # Remove bomb
                self.bombs.remove(bomb)
                logger.info(f"💣 Bomb exploded! Radius: {bomb.explosion_radius}")

    def _apply_laser_damage(self, damage_event):
        """Apply damage from laser to all targets"""
        targets = damage_event.get("targets", [])
        damage = damage_event["damage"]

        enemies_hit = 0
        for i, target_pos in enumerate(targets):
            # Laser hit effect
            self.effect_manager.laser_hit(target_pos)

            for enemy in list(self.enemies):
                if enemy.position.distance_to(target_pos) < 30:
                    enemy.take_damage(damage)
                    enemies_hit += 1

                    if enemy.health <= 0:
                        logger.debug("      💀 Enemy killed!")
                        self._handle_enemy_death(enemy)
                        self.wave_system.on_enemy_killed()

                    break  # Only hit one enemy per target position

    def _handle_enemy_death(self, enemy):
        """
        Handle enemy death - spawn drops and effects

        Args:
            enemy: Enemy that died
        """
        # ✅ Death effects (particles + screen shake)
        self.effect_manager.enemy_death(enemy.position, enemy.__class__.__name__)

        # Spawn pickups
        self.pickup_manager.spawn_from_enemy(enemy, self.pickups)

        # Remove enemy from game
        enemy.kill()

        # Increment kill counter
        self.enemies_killed += 1

    def _check_player_enemy_collisions(self):
        """Check player-enemy collisions"""
        if self.player.is_dashing:
            return  # No damage during dash

        for enemy in self.enemies:
            distance = self.player.position.distance_to(enemy.position)
            collision_distance = self.player.radius + enemy.radius

            if distance < collision_distance:
                if self.player.take_damage(enemy.contact_damage):
                    # ✅ Player damage effect
                    self.effect_manager.player_damage()
                    logger.info(
                        f"💥 Player hit by {enemy.__class__.__name__}! "
                        f"-{enemy.contact_damage} HP"
                    )

    def _show_upgrade_menu(self):
        """Show upgrade menu with choices"""
        choices = self.upgrade_system.generate_choices(self.player, num_choices=3)

        if choices:
            self.upgrade_menu.show(choices)
            self.paused = True
            logger.info("📈 Level up! Choose an upgrade!")

    def _apply_upgrade(self, choice_index):
        """Apply selected upgrade"""
        if choice_index < len(self.upgrade_menu.choices):
            upgrade = self.upgrade_menu.choices[choice_index]
            message = self.upgrade_system.apply_upgrade(upgrade, self.player)

            logger.info(f"Upgrade applied: {message}")

        # Hide menu and resume game
        self.upgrade_menu.hide()
        self.paused = False

    def render(self):
        """Render game (delegates to renderer)"""
        if self.game_over:
            self.renderer.render_game_over(self)
            return

        # Always render game first
        self.renderer.render_game(self, self.camera, self.mouse_screen_pos)

        # Add overlays if needed
        if self.paused:
            if self.upgrade_menu.active:
                self.upgrade_menu.render(self.screen)
            else:
                self.renderer.render_paused(self, self.camera)

        # Single flip at the end
        pygame.display.flip()

    def restart(self):
        """Restart the game"""
        self.__init__(self.screen)
        self.paused = False
        logger.info("🔄 Game restarted!")
