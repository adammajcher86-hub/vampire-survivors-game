"""
Main Game Class
Manages game state, entities, and systems
"""
import pygame
from src.config import WindowConfig, Colors


class Game:
    """Main game controller"""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.paused = False

        # Game time tracking
        self.game_time = 0.0

        print("Game initialized!")
        print(f"Window: {WindowConfig.WIDTH}x{WindowConfig.HEIGHT}")
        print(f"FPS: {WindowConfig.FPS}")

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

    def render(self):
        """Render the game"""
        # Clear screen with background color
        self.screen.fill(Colors.BACKGROUND)

        # Draw test message
        self._draw_test_message()

    def _draw_test_message(self):
        """Draw test message to verify rendering"""
        font = pygame.font.Font(None, 48)

        # Title
        title = font.render("Vampire Survivors Clone", True, Colors.UI_TEXT)
        title_rect = title.get_rect(center=(WindowConfig.WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Instructions
        small_font = pygame.font.Font(None, 32)
        instructions = [
            "Press ESC to pause",
            f"Game Time: {self.game_time:.1f}s",
            "Ready for player movement!" if not self.paused else "PAUSED"
        ]

        for i, text in enumerate(instructions):
            color = Colors.UI_ACCENT if i == 2 else Colors.UI_TEXT
            surface = small_font.render(text, True, color)
            rect = surface.get_rect(center=(WindowConfig.WIDTH // 2, 250 + i * 50))
            self.screen.blit(surface, rect)