"""
Game Renderer
Handles all rendering for the game
Separates rendering logic from game logic
"""

import pygame

from src.config.weapons.spread_weapon import SpreadWeaponConfig


class GameRenderer:
    """Handles rendering game objects and UI"""

    def __init__(self, screen):
        """
        Initialize renderer

        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Background color
        self.bg_color = (50, 50, 50)

        # UI colors
        self.ui_bg_color = (40, 40, 40, 200)
        self.ui_text_color = (255, 255, 255)
        self.health_color = (255, 0, 0)
        self.stamina_color = (0, 150, 255)
        self.xp_color = (255, 215, 0)

        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        self.font_huge = pygame.font.Font(None, 64)

    def render_game(self, game_state, camera, mouse_screen_pos):
        """
        Main render method for gameplay

        Args:
            game_state: Game object with all entities
            camera: Camera for world-to-screen conversion
            mouse_screen_pos: current mouse position
        """
        # Clear screen
        self.screen.fill(self.bg_color)

        # Render in layers (bottom to top)
        self.render_background(game_state, camera)
        self.render_pickups(game_state.pickups, camera)
        self.render_enemies(game_state.enemies, camera, game_state.player.position)
        self.render_player(game_state.player, camera)
        self.render_projectiles(game_state.projectiles, camera)
        self.render_enemy_projectiles(game_state.enemy_projectiles, camera)
        self.render_bombs(game_state.bombs, camera)
        self.render_effects(game_state, camera)
        self._render_crosshair(mouse_screen_pos)
        self.render_ui(game_state)
        # if game_state.debug_mode:
        self.render_debug_collision_grid(game_state.collision_manager)
        # Flip display
        # pygame.display.flip()

    def render_background(self, game_state, camera):
        """
        Render background elements (grid, tiles, etc.)

        Args:
            game_state: Game object
            camera: Camera
        """
        # Optional: Draw grid for debugging
        # if hasattr(game_state, 'debug_mode') and game_state.debug_mode:
        self._render_debug_grid(camera)

    def _render_debug_grid(self, camera):
        """Render debug grid"""
        grid_size = 50
        grid_color = (70, 70, 70)

        # Calculate visible grid range
        start_x = int(camera.offset.x // grid_size) * grid_size
        start_y = int(camera.offset.y // grid_size) * grid_size
        end_x = start_x + self.screen_width + grid_size
        end_y = start_y + self.screen_height + grid_size

        # Draw vertical lines
        for x in range(start_x, end_x, grid_size):
            screen_pos = camera.apply(pygame.math.Vector2(x, start_y))
            pygame.draw.line(
                self.screen,
                grid_color,
                (int(screen_pos.x), 0),
                (int(screen_pos.x), self.screen_height),
            )

        # Draw horizontal lines
        for y in range(start_y, end_y, grid_size):
            screen_pos = camera.apply(pygame.math.Vector2(start_x, y))
            pygame.draw.line(
                self.screen,
                grid_color,
                (0, int(screen_pos.y)),
                (self.screen_width, int(screen_pos.y)),
            )

    def render_pickups(self, pickups, camera):
        """Render all pickups"""
        for pickup in pickups:

            pickup.render(self.screen, camera)

    def render_enemies(self, enemies, camera, player_position):
        """Render all enemies"""
        for enemy in enemies:
            enemy.render(self.screen, camera, player_position)

    def render_player(self, player, camera):
        """Render player"""
        player.render(self.screen, camera)

    def render_projectiles(self, projectiles, camera):
        """Render all projectiles"""
        for projectile in projectiles:
            projectile.render(self.screen, camera)

    def render_bombs(self, bombs, camera):
        """Render all bombs"""
        for bomb in bombs:
            bomb.render(self.screen, camera)

    def render_effects(self, game_state, camera):
        """
        Render visual effects (beams, particles, etc.)

        Args:
            game_state: Game object
            camera: Camera
        """
        # Render laser beams
        if hasattr(game_state, "player"):
            for slot in game_state.player.weapon_slots:
                if not slot.is_empty() and hasattr(slot.weapon, "render_beams"):
                    slot.weapon.render_beams(self.screen, camera)

        # Render particle effects
        if hasattr(game_state, "effect_manager"):
            game_state.effect_manager.render(self.screen, camera)

    def render_ui(self, game_state):
        """
        Render UI elements (health, XP, wave info, etc.)

        Args:
            game_state: Game object
        """
        # Top-left UI
        ui_x = 10
        ui_y = 10

        # Health bar
        self._render_health_bar(game_state.player, ui_x, ui_y)
        ui_y += 30

        # Stamina bar
        self._render_stamina_bar(game_state.player, ui_x, ui_y)
        ui_y += 30

        # XP bar and level
        if hasattr(game_state, "xp_system"):
            self._render_xp_bar(game_state.xp_system, ui_x, ui_y)
            ui_y += 30

        # Wave info
        if hasattr(game_state, "wave_system"):
            self._render_wave_info(game_state.wave_system, ui_x, ui_y)
            ui_y += 30

        # Bomb count
        self._render_bomb_count(game_state.player, ui_x, ui_y)

        # Top-right stats
        self._render_game_stats(game_state)

        # Debug info
        if hasattr(game_state, "debug_mode") and game_state.debug_mode:
            self._render_debug_info(game_state)

    def _render_health_bar(self, player, x, y):
        """Render player health bar"""
        bar_width = 200
        bar_height = 20

        # Background
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y, bar_width, bar_height))

        # Health fill
        health_percent = max(0, player.health / player.max_health)
        fill_width = int(bar_width * health_percent)
        pygame.draw.rect(self.screen, self.health_color, (x, y, fill_width, bar_height))

        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        # Text
        text = self.font.render(
            f"HP: {int(player.health)}/{player.max_health}", True, (255, 255, 255)
        )
        self.screen.blit(text, (x + 5, y + 2))

    def _render_stamina_bar(self, player, x, y):
        """Render player stamina bar"""
        bar_width = 200
        bar_height = 20

        # Background
        pygame.draw.rect(self.screen, (0, 50, 100), (x, y, bar_width, bar_height))

        # Stamina fill
        stamina_percent = max(0, player.stamina / player.max_stamina)
        fill_width = int(bar_width * stamina_percent)
        pygame.draw.rect(
            self.screen, self.stamina_color, (x, y, fill_width, bar_height)
        )

        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        # Text
        text = self.font.render(
            f"SP: {int(player.stamina)}/{int(player.max_stamina)}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(text, (x + 5, y + 2))

    def _render_xp_bar(self, xp_system, x, y):
        """Render XP bar"""
        bar_width = 200
        bar_height = 20

        # Background
        pygame.draw.rect(self.screen, (100, 86, 0), (x, y, bar_width, bar_height))

        # ✅ FIXED: Use correct attributes
        xp_percent = min(1.0, xp_system.current_xp / xp_system.xp_to_next_level)
        fill_width = int(bar_width * xp_percent)
        pygame.draw.rect(self.screen, self.xp_color, (x, y, fill_width, bar_height))

        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        # Text
        text = self.font.render(
            f"Level {xp_system.current_level}: {xp_system.current_xp}/{xp_system.xp_to_next_level} XP",
            True,
            (255, 255, 255),
        )
        self.screen.blit(text, (x + 5, y + 2))

    def _render_wave_info(self, wave_system, x, y):
        """Render wave information"""
        wave_text = f"Wave {wave_system.current_wave}"
        text = self.font_large.render(wave_text, True, (255, 200, 0))
        self.screen.blit(text, (x, y))

    def _render_bomb_count(self, player, x, y):
        """Render bomb count"""
        bomb_text = f"Bombs x{player.bomb_count}"
        text = self.font.render(bomb_text, True, (255, 150, 0))
        self.screen.blit(text, (x, y))

    def _render_game_stats(self, game_state):
        """Render game stats in top-right"""
        x = self.screen_width - 220
        y = 10

        stats = []

        # Game time
        if hasattr(game_state, "game_time"):
            minutes = int(game_state.game_time // 60)
            seconds = int(game_state.game_time % 60)
            stats.append(f"Time: {minutes:02d}:{seconds:02d}")

        # Enemies
        if hasattr(game_state, "enemies"):
            stats.append(f"Enemies: {len(game_state.enemies)}")

        # Kills
        if hasattr(game_state, "enemies_killed"):
            stats.append(f"Killed: {game_state.enemies_killed}")

        # XP collected
        if hasattr(game_state, "xp_collected"):
            stats.append(f"XP: {game_state.xp_collected}")

        # Weapons
        if hasattr(game_state, "player"):
            weapon_count = sum(
                1 for slot in game_state.player.weapon_slots if not slot.is_empty()
            )
            stats.append(f"Weapons: {weapon_count}")

        # Render stats
        for stat in stats:
            text = self.font.render(stat, True, (255, 255, 255))
            self.screen.blit(text, (x, y))
            y += 25

    def _render_debug_info(self, game_state):
        """Render debug information"""
        x = 10
        y = self.screen_height - 150

        debug_lines = [
            f"FPS: {int(game_state.clock.get_fps())}",
            f"Pos: ({int(game_state.player.position.x)}, {int(game_state.player.position.y)})",
        ]

        if hasattr(game_state, "projectiles"):
            debug_lines.append(f"Projectiles: {len(game_state.projectiles)}")

        if hasattr(game_state, "pickups"):
            debug_lines.append(f"Pickups: {len(game_state.pickups)}")

        if hasattr(game_state, "effect_manager"):
            particle_count = (
                game_state.effect_manager.particle_system.get_particle_count()
            )
            debug_lines.append(f"Particles: {particle_count}")

        # Render debug text with background
        for i, line in enumerate(debug_lines):
            text = self.font_small.render(line, True, (0, 255, 0))

            # Semi-transparent background
            bg_rect = pygame.Rect(x - 2, y + i * 22 - 2, text.get_width() + 4, 22)
            bg_surface = pygame.Surface(
                (bg_rect.width, bg_rect.height), pygame.SRCALPHA
            )
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, bg_rect)

            # Text
            self.screen.blit(text, (x, y + i * 22))

    def render_paused(self, game_state, camera):
        """
        Render game with pause overlay

        Args:
            game_state: Game object
            camera: Camera
        """
        # Render game in background
        # self.render_game(game_state, camera)

        # Dark overlay
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        text = self.font_huge.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 50)
        )
        self.screen.blit(text, rect)

        # Instructions
        instruction = self.font.render("Press ESC to resume", True, (200, 200, 200))
        inst_rect = instruction.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 20)
        )
        self.screen.blit(instruction, inst_rect)

        # pygame.display.flip()

    def render_game_over(self, game_state):
        """
        Render game over screen

        Args:
            game_state: Game object
        """
        # Clear screen
        self.screen.fill((20, 20, 20))

        # Game Over text
        game_over_text = self.font_huge.render("GAME OVER", True, (255, 50, 50))
        rect = game_over_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 100)
        )
        self.screen.blit(game_over_text, rect)

        # Stats
        y_offset = 0
        stats = []

        if hasattr(game_state, "game_time"):
            minutes = int(game_state.game_time // 60)
            seconds = int(game_state.game_time % 60)
            stats.append(f"Survived: {minutes:02d}:{seconds:02d}")

        if hasattr(game_state, "enemies_killed"):
            stats.append(f"Enemies Killed: {game_state.enemies_killed}")

        if hasattr(game_state, "wave_system"):
            stats.append(f"Reached Wave: {game_state.wave_system.current_wave}")

        if hasattr(game_state, "xp_system"):
            stats.append(f"Level Reached: {game_state.xp_system.current_level}")

        for stat in stats:
            text = self.font_large.render(stat, True, (255, 255, 255))
            stat_rect = text.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + y_offset)
            )
            self.screen.blit(text, stat_rect)
            y_offset += 50

        # Restart instruction
        restart_text = self.font.render(
            "Press R to restart or ESC to quit", True, (200, 200, 200)
        )
        restart_rect = restart_text.get_rect(
            center=(self.screen_width // 2, self.screen_height - 100)
        )
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def render_upgrade_menu(self, upgrade_menu):
        """
        Render upgrade menu overlay

        Args:
            upgrade_menu: UpgradeMenu object
        """
        upgrade_menu.render(self.screen)

    def _render_crosshair(self, mouse_screen_pos):
        """Render mouse crosshair for aiming"""
        # Get mouse position (screen space)
        mouse_x, mouse_y = int(mouse_screen_pos.x), int(mouse_screen_pos.y)

        size = SpreadWeaponConfig.CROSSHAIR_SIZE
        color = SpreadWeaponConfig.CROSSHAIR_COLOR
        thickness = SpreadWeaponConfig.CROSSHAIR_THICKNESS

        # Draw crosshair (circle + cross)
        # Outer circle
        pygame.draw.circle(self.screen, color, (mouse_x, mouse_y), size, thickness)

        # Horizontal line
        pygame.draw.line(
            self.screen,
            color,
            (mouse_x - size - 5, mouse_y),
            (mouse_x - size // 2, mouse_y),
            thickness,
        )
        pygame.draw.line(
            self.screen,
            color,
            (mouse_x + size // 2, mouse_y),
            (mouse_x + size + 5, mouse_y),
            thickness,
        )

        # Vertical line
        pygame.draw.line(
            self.screen,
            color,
            (mouse_x, mouse_y - size - 5),
            (mouse_x, mouse_y - size // 2),
            thickness,
        )
        pygame.draw.line(
            self.screen,
            color,
            (mouse_x, mouse_y + size // 2),
            (mouse_x, mouse_y + size + 5),
            thickness,
        )

    def render_enemy_projectiles(self, enemy_projectiles, camera):
        """Render all enemy projectiles with different color"""
        for projectile in enemy_projectiles:
            # Render with warning color (red/orange)
            projectile.render(self.screen, camera)

            # Optional: Add glow effect
            if hasattr(projectile, "position"):
                screen_pos = camera.apply(projectile.position)
                pygame.draw.circle(
                    self.screen,
                    (255, 100, 100, 100),  # Red glow
                    (int(screen_pos.x), int(screen_pos.y)),
                    8,
                    2,
                )

    def render_debug_collision_grid(self, collision_manager):
        """Render collision grid for debugging"""

        info = collision_manager.get_debug_info()

        # Draw info on screen
        debug_text = [
            f"Grid Cells: {info['grid_cells']}",
            f"Entities: {info['entities_in_grid']}",
            f"Avg/Cell: {info['avg_per_cell']:.1f}",
            f"Projectile Hits: {info['projectile_hits']}",
            f"Enemy Projectile Hits: {info['enemy_projectile_hits']}",
            f"Player Collisions: {info['player_collisions']}",
        ]

        y_offset = 200
        for line in debug_text:
            text_surface = self.font.render(line, True, (255, 255, 0))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 20
