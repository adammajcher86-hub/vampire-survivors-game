"""
Main Game Engine
Manages game state, entities, and systems
"""

import pygame
from src.config import WindowConfig, Colors
from src.entities import Player, BasicWeapon
from src.camera import Camera
from src.systems import EnemySpawner, XPSystem, UpgradeSystem, PickupManager
from src.ui import UpgradeMenu


class Game:
    """Main game controller"""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = False
        self.game_over = False

        # Game time tracking
        self.game_time = 0.0

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

        # Game stats
        self.enemies_killed = 0

        print("Game initialized!")
        print(f"Window: {WindowConfig.WIDTH}x{WindowConfig.HEIGHT}")
        print(f"FPS: {WindowConfig.FPS}")
        print("Controls: WASD or Arrow Keys to move, ESC to pause")
        print("Starting weapon: Basic Weapon (auto-aim)")
        print("Collect XP to level up!")

    def handle_event(self, event):
        """Handle game events"""

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
                print(f"Game {'paused' if self.paused else 'resumed'}")

    def update(self, dt):
        """Update game state"""
        if self.paused or self.game_over:
            return

        self.game_time += dt

        # Get player input
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (
            keys[pygame.K_w] or keys[pygame.K_UP]
        )

        # Update player
        self.player.update(dt, dx, dy)

        # Update camera to follow player
        self.camera.update(self.player)

        # Update enemy spawner
        self.enemy_spawner.update(dt, self.player.position, self.enemies)

        # Update all enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player.position)

        # Update all weapons (POLYMORPHIC!)
        for weapon in self.weapons:
            weapon.update(dt, self.player, self.enemies, self.projectiles)

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)

        # Check projectile-enemy collisions
        self._check_projectile_collisions()

        # Remove expired projectiles
        self._remove_expired_projectiles()

        # Update all pickups (magnetic pull, animations)
        for pickup in self.pickups:
            pickup.update(dt, self.player)

        # Collect pickups
        collected_xp = self.pickup_manager.collect_pickups(self.player, self.pickups)

        # Update XP system (returns True if leveled up)
        leveled_up = self.xp_system.update(dt, collected_xp)

        # Show upgrade menu on level up
        if leveled_up:
            self._show_upgrade_menu()

        # Check enemy-player collision
        self._check_enemy_collision(dt)

        # Check game over
        if not self.player.is_alive():
            self.game_over = True  # ✅ Set game_over, not paused!
            print("💀 GAME OVER!")
            print(f"Survived: {self.game_time:.1f}s")
            print(f"Enemies Killed: {self.enemies_killed}")
            print(f"Level Reached: {self.xp_system.current_level}")

    def _check_projectile_collisions(self):
        """Check and handle projectile-enemy collisions"""
        for projectile in list(self.projectiles):
            for enemy in list(self.enemies):
                if projectile.collides_with(enemy):
                    # Damage enemy
                    if enemy.take_damage(projectile.damage):
                        # Enemy died
                        self.enemies_killed += 1
                        self.pickup_manager.spawn_from_enemy(enemy, self.pickups)
                        self.enemies.remove(enemy)

                    # Remove projectile
                    self.projectiles.remove(projectile)
                    break

    def _remove_expired_projectiles(self):
        """Remove projectiles that have exceeded their lifetime"""
        for projectile in list(self.projectiles):
            if projectile.is_expired():
                self.projectiles.remove(projectile)

    def _check_enemy_collision(self, dt):
        """Check and handle enemy collision with player"""
        for enemy in self.enemies:
            if enemy.collides_with(self.player):
                # Don't take damage if invulnerable (during dash)
                if not self.player.invulnerable:
                    # Check if it's an Elite doing a dash attack
                    if hasattr(enemy, "is_dashing") and enemy.is_dashing:
                        # Elite dash hit! Apply slow debuff
                        self.player.apply_slow(
                            duration=enemy.dash_slow_duration,
                            strength=enemy.dash_slow_strength,
                        )

                    # Normal contact damage
                    damage = enemy.damage * dt
                    self.player.take_damage(damage)

    def render(self):
        """Render the game"""
        # Clear screen with background color
        self.screen.fill(Colors.BACKGROUND)

        # Draw grid for reference
        self._draw_grid()

        # Draw all pickups (XP orbs, health, etc.)
        for pickup in self.pickups:
            pickup.render(self.screen, self.camera)

        # Draw all projectiles
        for projectile in self.projectiles:
            projectile.render(self.screen, self.camera)

        # Draw all enemies
        for enemy in self.enemies:
            enemy.render(self.screen, self.camera)

        # Draw player with camera offset
        self.player.render(self.screen, self.camera)

        # Draw UI (XP bar, debug info)
        self._draw_xp_bar()
        self._draw_debug_info()
        self._render_resource_bars()

        # Draw level up notification
        if self.xp_system.level_up_flash:
            self._draw_level_up()

            # Draw pause screen (but not if game over)
        if self.paused and not self.game_over:
            self._draw_pause_text()  # Just the pause text

            # Draw game over screen
        if self.game_over:
            self._draw_game_over()

            # Draw upgrade menu (if active)
        self.upgrade_menu.render(self.screen)

    def _draw_grid(self):
        """Draw background grid"""
        grid_size = 64
        cam_x, cam_y = self.camera.offset

        # Calculate visible grid lines
        start_x = int(cam_x // grid_size) * grid_size
        start_y = int(cam_y // grid_size) * grid_size

        # Draw vertical lines
        for x in range(start_x, start_x + WindowConfig.WIDTH + grid_size, grid_size):
            screen_x = x - cam_x
            pygame.draw.line(
                self.screen, Colors.GRAY, (screen_x, 0), (screen_x, WindowConfig.HEIGHT)
            )

        # Draw horizontal lines
        for y in range(start_y, start_y + WindowConfig.HEIGHT + grid_size, grid_size):
            screen_y = y - cam_y
            pygame.draw.line(
                self.screen, Colors.GRAY, (0, screen_y), (WindowConfig.WIDTH, screen_y)
            )

    def _draw_xp_bar(self):
        """Draw XP bar at top of screen"""
        bar_width = 300
        bar_height = 20
        bar_x = (WindowConfig.WIDTH - bar_width) // 2
        bar_y = 10

        # Background (dark gray)
        pygame.draw.rect(
            self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height)
        )

        # XP progress (cyan)
        progress = self.xp_system.get_xp_progress()
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            pygame.draw.rect(
                self.screen, Colors.CYAN, (bar_x, bar_y, progress_width, bar_height)
            )

        # Border
        pygame.draw.rect(
            self.screen, Colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 2
        )

        # Level text
        font = pygame.font.Font(None, 24)
        level_text = font.render(
            f"Level {self.xp_system.current_level}", True, Colors.WHITE
        )
        text_rect = level_text.get_rect(
            center=(bar_x + bar_width // 2, bar_y + bar_height // 2)
        )
        self.screen.blit(level_text, text_rect)

    def _draw_level_up(self):
        """Draw level up notification"""
        # Calculate flash alpha (fades out over time)
        alpha = int(
            255
            * (1.0 - self.xp_system.level_up_timer / self.xp_system.level_up_duration)
        )

        # Large text
        font = pygame.font.Font(None, 100)
        text = font.render("LEVEL UP!", True, Colors.YELLOW)
        text.set_alpha(alpha)

        # Position at center
        text_rect = text.get_rect(
            center=(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2)
        )
        self.screen.blit(text, text_rect)

    def _draw_debug_info(self):
        """Draw debug information"""
        font = pygame.font.Font(None, 24)

        debug_info = [
            f"Time: {self.game_time:.1f}s",
            f"Pos: ({int(self.player.position.x)}, {int(self.player.position.y)})",
            f"HP: {int(self.player.health)}/{self.player.max_health}",
            f"Enemies: {len(self.enemies)}",
            f"Killed: {self.enemies_killed}",
            f"XP: {self.xp_system.current_xp}/{self.xp_system.xp_to_next_level}",
            f"Weapons: {len(self.weapons)}",
        ]

        y_offset = 50  # Start below XP bar
        for text in debug_info:
            surface = font.render(text, True, Colors.WHITE)
            self.screen.blit(surface, (10, y_offset))
            y_offset += 25

    def _draw_pause_screen(self):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WindowConfig.WIDTH, WindowConfig.HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self.screen.blit(overlay, (0, 0))

        # Check if game over
        if not self.player.is_alive():
            self._draw_game_over()
        else:
            self._draw_pause_text()

    def _draw_pause_text(self):
        """Draw paused text"""
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, Colors.WHITE)
        text_rect = text.get_rect(
            center=(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2)
        )
        self.screen.blit(text, text_rect)

        # Hint text
        small_font = pygame.font.Font(None, 36)
        hint = small_font.render("Press ESC to continue", True, Colors.WHITE)
        hint_rect = hint.get_rect(
            center=(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2 + 60)
        )
        self.screen.blit(hint, hint_rect)

    def _draw_game_over(self):
        """Draw game over screen"""
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, Colors.RED)
        text_rect = text.get_rect(
            center=(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2 - 50)
        )
        self.screen.blit(text, text_rect)

        # Stats
        small_font = pygame.font.Font(None, 36)
        stats = [
            f"Survived: {self.game_time:.1f}s",
            f"Enemies Killed: {self.enemies_killed}",
            f"Final Level: {self.xp_system.current_level}",
            "Press r for restart, esc to quit.",
        ]

        y_offset = WindowConfig.HEIGHT // 2 + 20
        for stat in stats:
            stat_text = small_font.render(stat, True, Colors.WHITE)
            stat_rect = stat_text.get_rect(center=(WindowConfig.WIDTH // 2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 40

    def _show_upgrade_menu(self):
        """Show upgrade menu when player levels up"""
        # Generate 3 random upgrade choices
        choices = self.upgrade_system.generate_choices(
            self.player, self.weapons, num_choices=3
        )

        # Show menu and pause game
        self.upgrade_menu.show(choices)
        self.paused = True
        print("Level up! Upgrade menu shown.")

    def _apply_upgrade(self, choice_index):
        """
        Apply selected upgrade

        Args:
            choice_index: Index of selected upgrade (0, 1, 2)
        """
        if choice_index < len(self.upgrade_menu.choices):
            upgrade = self.upgrade_menu.choices[choice_index]
            message = self.upgrade_system.apply_upgrade(
                upgrade, self.player, self.weapons
            )

            print(f"Upgrade applied: {message}")

        # Hide menu and resume game
        self.upgrade_menu.hide()
        self.paused = False

    def _render_resource_bars(self):
        """Render health and stamina bars"""
        bar_width = 300
        bar_height = 25
        bar_x = 490  # Left side of screen
        bar_y = 35
        spacing = 30

        # Health Bar
        pygame.draw.rect(
            self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height)
        )
        health_percent = self.player.health / self.player.max_health
        health_width = int(bar_width * health_percent)
        pygame.draw.rect(
            self.screen, Colors.RED, (bar_x, bar_y, health_width, bar_height)
        )
        pygame.draw.rect(
            self.screen, Colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 2
        )

        # Health text
        health_font = pygame.font.Font(None, 24)
        health_text = health_font.render(
            f"HP: {int(self.player.health)}/{int(self.player.max_health)}",
            True,
            Colors.WHITE,
        )
        self.screen.blit(health_text, (bar_x + 5, bar_y + 3))

        # Stamina Bar
        stamina_y = bar_y + spacing
        pygame.draw.rect(
            self.screen, (50, 50, 50), (bar_x, stamina_y, bar_width, bar_height)
        )
        stamina_percent = self.player.stamina / self.player.max_stamina
        stamina_width = int(bar_width * stamina_percent)
        pygame.draw.rect(
            self.screen,
            Colors.CYAN,  # Blue/cyan for stamina
            (bar_x, stamina_y, stamina_width, bar_height),
        )
        pygame.draw.rect(
            self.screen, Colors.WHITE, (bar_x, stamina_y, bar_width, bar_height), 2
        )

        # Stamina text
        stamina_text = health_font.render(
            f"SP: {int(self.player.stamina)}/{int(self.player.max_stamina)}",
            True,
            Colors.WHITE,
        )
        self.screen.blit(stamina_text, (bar_x + 5, stamina_y + 3))

    def restart(self):
        """Restart the game - reset all state"""
        # Reset game state
        self.game_over = False
        self.paused = False
        self.game_time = 0.0
        self.enemies_killed = 0

        # Reset player
        self.player = Player(WindowConfig.WIDTH // 2, WindowConfig.HEIGHT // 2)

        # Clear all entities
        self.enemies.empty()
        self.projectiles.empty()
        self.pickups.empty()

        # Reset weapons
        self.weapons = [BasicWeapon()]

        # Reset systems
        self.xp_system = XPSystem()
        self.enemy_spawner = EnemySpawner()

        print("🔄 Game Restarted!")
