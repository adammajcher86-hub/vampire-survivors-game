"""
Main Game Engine
Manages game state, entities, and systems
"""

import pygame
import math
from src.config import WindowConfig, FastEnemyConfig
from src.entities import Player
from src.camera import Camera
from src.logger import logger
from src.systems import EnemySpawner, XPSystem, UpgradeSystem, PickupManager, WaveSystem
from src.ui import UpgradeMenu
from src.entities.projectiles import LaserProjectile
from src.config.enemies.tank_laser import TankLaserConfig
from src.config.enemies.fast_laser import FastLaserConfig
from src.rendering import GameRenderer
from src.systems.effects import EffectManager
from src.systems.input import InputHandler
from src.systems.collision import CollisionManager
from src.game_event_handler import GameEventHandler
from src.systems.events import get_event_bus, GameEvent
from src.weapon_registry import register_all_weapons
from src.factories import create_starter_weapon


class Game:
    """Main game controller"""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = True
        self.game_over = False

        # Game time tracking
        self.game_time = 0.0

        # Initialize renderer EARLY
        self.renderer = GameRenderer(screen)

        # Initialize effect manager
        self.effect_manager = EffectManager()

        self.input_handler = InputHandler()
        # Initialize camera
        self.camera = Camera(WindowConfig.WIDTH, WindowConfig.HEIGHT)
        # Initialize collision manager
        self.collision_manager = CollisionManager(cell_size=100)
        # Initialize event bus
        self.event_bus = get_event_bus()
        self.event_bus.reset()

        register_all_weapons()
        # Initialize player at center of screen
        self.player = Player(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2)
        starter_weapon = create_starter_weapon("basic")
        self.player.add_weapon(starter_weapon)
        # Entity groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Enemy management
        self.enemies = pygame.sprite.Group()
        self.enemy_spawner = EnemySpawner()

        # Weapon system - POLYMORPHIC LIST!
        # self.weapons = [BasicWeapon()]  # Start with basic weapon
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
        self.event_handler = GameEventHandler(self)

    def handle_event(self, event):
        """Handle game events"""

        # Pause toggle (keep in event loop for immediate response)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.game_over and not self.upgrade_menu.active:
                    self.paused = not self.paused
                    logger.info(f"Game {'paused' if self.paused else 'resumed'}")
                    return

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

    def update(self, dt):
        """Update game state"""
        if self.paused or self.game_over:
            return

        self.game_time += dt

        # UPDATE INPUT FIRST
        self.input_handler.update(self.camera.offset)

        # Get input from handler
        self.mouse_screen_pos = self.input_handler.get_mouse_screen_pos()
        self.mouse_world_pos = self.input_handler.get_mouse_world_pos()
        dx, dy = self.input_handler.get_movement_vector()

        # HANDLE ACTIONS (before player update)

        # Dash action
        if self.input_handler.dash_pressed():
            self.player.try_dash(dx, dy)

        # Bomb action
        if self.input_handler.bomb_pressed():
            self.player.place_bomb(self.bombs)

        # Debug toggle
        if self.input_handler.debug_toggle_pressed():
            self.debug_mode = not self.debug_mode
            logger.info(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

        # Update player
        self.player.update(dt, dx, dy, self.mouse_world_pos)

        # Update all weapon slots
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

        # Update effects (particles, screen shake)
        self.effect_manager.update(dt)

        # Update camera with screen shake
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
        self._handle_collisions()

        # Remove expired projectiles
        for projectile in list(self.projectiles):
            if projectile.is_expired():
                self.projectiles.remove(projectile)

        for projectile in list(self.enemy_projectiles):
            if projectile.is_expired():
                self.enemy_projectiles.remove(projectile)

        # Handle pickup collection
        collected_xp = self.pickup_manager.collect_pickups(self.player, self.pickups)
        if collected_xp > 0:
            # EMIT XP GAINED EVENT
            self.event_bus.emit(
                GameEvent.XP_GAINED,
                amount=collected_xp,
                total_collected=self.xp_collected + collected_xp,
            )

            if self.xp_system.update(dt, collected_xp):
                # EMIT LEVEL UP EVENT
                self.event_bus.emit(
                    GameEvent.LEVEL_UP,
                    new_level=self.xp_system.current_level,
                    xp_required=self.xp_system.xp_to_next_level,
                    player=self.player,
                )

        # OPTIONAL: Debug logging
        current_time = pygame.time.get_ticks()
        if current_time - self.last_debug_time >= self.DEBUG_INTERVAL:
            logger.debug(
                f"Entities - Enemies: {len(self.enemies)}, "
                f"Projectiles: {len(self.projectiles)}, "
                f"Enemy Projectiles: {len(self.enemy_projectiles)}, "
                f"Pickups: {len(self.pickups)}"
            )
            self.last_debug_time = current_time

        # Check game over
        if self.player.health <= 0:
            self.game_over = True
            logger.info("💀 GAME OVER!")

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

    def _handle_collisions(self):
        """Handle all collision detection and responses"""

        # Run all collision checks at once
        self.collision_manager.check_all(
            self.player,
            self.enemies,
            self.projectiles,
            self.enemy_projectiles,
            self.bombs,
            self.pickups,
        )

        # ==================== PROJECTILE HITS ====================
        for projectile, enemy in self.collision_manager.get_projectile_hits():
            # Apply damage
            enemy.take_damage(projectile.damage)

            # EMIT EVENT
            self.event_bus.emit(
                GameEvent.PROJECTILE_HIT,
                projectile=projectile,
                enemy=enemy,
                position=enemy.position.copy(),
                damage=projectile.damage,
            )

            # Remove projectile directly
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)

            # Check if enemy died
            if enemy.health <= 0:
                self._handle_enemy_death(enemy)
                self.wave_system.on_enemy_killed()

        # ==================== ENEMY PROJECTILE HITS ====================
        for projectile in self.collision_manager.get_enemy_projectile_hits():
            # Apply damage to player
            damage = getattr(projectile, "damage", 10)
            self.player.take_damage(damage)

            # EMIT EVENT
            self.event_bus.emit(
                GameEvent.PLAYER_DAMAGED,
                damage=damage,
                source=projectile,
                position=self.player.position.copy(),
            )

            # Remove enemy projectile directly
            if projectile in self.enemy_projectiles:
                self.enemy_projectiles.remove(projectile)

        # ==================== PLAYER-ENEMY COLLISIONS ====================
        if not hasattr(self.player, "last_hit_time"):
            self.player.last_hit_time = 0
        if not hasattr(self.player, "hit_cooldown"):
            self.player.hit_cooldown = 500

        for enemy in self.collision_manager.get_player_enemy_collisions():
            # Check if player can take contact damage (cooldown)
            current_time = pygame.time.get_ticks()
            if current_time - self.player.last_hit_time >= self.player.hit_cooldown:
                # Apply contact damage
                damage = getattr(enemy, "damage", 10)
                self.player.take_damage(damage)
                self.player.last_hit_time = current_time

                # EMIT EVENT
                self.event_bus.emit(
                    GameEvent.PLAYER_DAMAGED,
                    damage=damage,
                    source=enemy,
                    position=self.player.position.copy(),
                )

        # ==================== BOMB EXPLOSIONS ====================
        for bomb, hit_enemies in self.collision_manager.get_bomb_hits():
            # Remove bomb
            if bomb in self.bombs:
                self.bombs.remove(bomb)

            # EMIT EVENT
            self.event_bus.emit(
                GameEvent.BOMB_EXPLODED,
                position=bomb.position.copy(),
                enemies_hit=len(hit_enemies),
                damage=bomb.damage,
            )

            # Damage all enemies in range
            for enemy in hit_enemies:
                enemy.take_damage(bomb.damage)

                if enemy.health <= 0:
                    self._handle_enemy_death(enemy)
                    self.wave_system.on_enemy_killed()

    def _check_fast_enemy_explosions(self):
        """Check for FastEnemy explosions and spawn radial lasers"""
        for enemy in list(self.enemies):
            # Check if FastEnemy should explode
            if hasattr(enemy, "should_explode") and enemy.should_explode():
                explosion_pos = enemy.get_explosion_position()

                # Explosion effect (smaller than bomb)
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
        Handle enemy death - emit event and spawn drops

        Args:
            enemy: Enemy that died
        """
        # let systems react
        self.event_bus.emit(
            GameEvent.ENEMY_KILLED,
            enemy=enemy,
            enemy_type=enemy.__class__.__name__,
            position=enemy.position.copy(),
        )

        # Spawn pickups
        self.pickup_manager.spawn_from_enemy(enemy, self.pickups)

        # Remove enemy from game
        enemy.kill()

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
