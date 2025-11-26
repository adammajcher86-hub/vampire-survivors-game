"""
Main Game Engine
Manages game state, entities, and systems
"""

import pygame
from src.config import WindowConfig, Colors
from src.entities import Player
from src.camera import Camera
from src.systems.enemy_spawner import EnemySpawner


class Game:
    """Main game controller"""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = False

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

        # Game stats
        self.enemies_killed = 0

        print("Game initialized!")
        print(f"Window: {WindowConfig.WIDTH}x{WindowConfig.HEIGHT}")
        print(f"FPS: {WindowConfig.FPS}")
        print("Controls: WASD or Arrow Keys to move, ESC to pause")

    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                print(f"Game {'paused' if self.paused else 'resumed'}")

    def update(self, dt):
        """Update game state"""
        if self.paused:
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

        # Check enemy-player collision
        self._check_enemy_collision(dt)

        # Remove dead enemies
        self._remove_dead_enemies()

        # Check game over
        if not self.player.is_alive():
            print(
                f"Game Over! Survived: {self.game_time:.1f}s, Killed: {self.enemies_killed}"
            )
            self.paused = True

    def _check_enemy_collision(self, dt):
        """Check and handle enemy collision with player"""
        for enemy in self.enemies:
            if enemy.collides_with(self.player):
                # Enemy deals damage to player
                self.player.take_damage(enemy.damage * dt)

    def _remove_dead_enemies(self):
        """Remove dead enemies and track kills"""
        for enemy in list(self.enemies):
            if enemy.is_dead:
                self.enemies_killed += 1
                self.enemies.remove(enemy)

    def render(self):
        """Render the game"""
        # Clear screen with background color
        self.screen.fill(Colors.BACKGROUND)

        # Draw grid for reference
        self._draw_grid()

        # Draw all enemies
        for enemy in self.enemies:
            enemy.render(self.screen, self.camera)

        # Draw player with camera offset
        self.player.render(self.screen, self.camera)

        # Draw debug info
        self._draw_debug_info()

        # Draw pause screen if paused
        if self.paused:
            self._draw_pause_screen()

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

    def _draw_debug_info(self):
        """Draw debug information"""
        font = pygame.font.Font(None, 24)

        debug_info = [
            f"Time: {self.game_time:.1f}s",
            f"Pos: ({int(self.player.position.x)}, {int(self.player.position.y)})",
            f"HP: {int(self.player.health)}/{self.player.max_health}",
            f"Enemies: {len(self.enemies)}",
            f"Killed: {self.enemies_killed}",
        ]

        y_offset = 10
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
        ]

        y_offset = WindowConfig.HEIGHT // 2 + 20
        for stat in stats:
            stat_text = small_font.render(stat, True, Colors.WHITE)
            stat_rect = stat_text.get_rect(center=(WindowConfig.WIDTH // 2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 40
