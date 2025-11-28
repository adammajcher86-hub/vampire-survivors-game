"""
Upgrade Menu
UI for displaying and selecting upgrades on level-up
"""

import pygame
from src.config import Colors, WindowConfig


class UpgradeMenu:
    """Upgrade menu UI"""

    def __init__(self):
        """Initialize upgrade menu"""
        self.active = False
        self.choices = []
        self.selected_index = None

        # UI settings
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        # Card dimensions
        self.card_width = 280
        self.card_height = 320
        self.card_spacing = 40

        # Colors
        self.bg_color = (0, 0, 0, 200)  # Semi-transparent black
        self.card_color = (40, 40, 60)
        self.card_hover_color = (60, 60, 100)
        self.card_border_color = Colors.YELLOW

    def show(self, choices):
        """
        Show upgrade menu with choices

        Args:
            choices: List of upgrade instances
        """
        self.active = True
        self.choices = choices
        self.selected_index = None

    def hide(self):
        """Hide upgrade menu"""
        self.active = False
        self.choices = []
        self.selected_index = None

    def handle_input(self, event):
        """
        Handle keyboard input

        Args:
            event: Pygame event

        Returns:
            int or None: Selected choice index (0, 1, 2) or None
        """
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            # Number keys 1, 2, 3
            if event.key == pygame.K_1 and len(self.choices) >= 1:
                return 0
            elif event.key == pygame.K_2 and len(self.choices) >= 2:
                return 1
            elif event.key == pygame.K_3 and len(self.choices) >= 3:
                return 2

        return None

    def render(self, screen):
        """
        Render upgrade menu

        Args:
            screen: Pygame surface to draw on
        """
        if not self.active:
            return

        screen_width = WindowConfig.WIDTH
        screen_height = WindowConfig.HEIGHT

        # Draw semi-transparent background overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Draw "LEVEL UP!" title
        title_text = self.font_large.render("LEVEL UP!", True, Colors.YELLOW)
        title_rect = title_text.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_text, title_rect)

        # Calculate card positions (centered)
        num_cards = len(self.choices)
        total_width = (self.card_width * num_cards) + (
            self.card_spacing * (num_cards - 1)
        )
        start_x = (screen_width - total_width) // 2
        start_y = 200

        # Draw upgrade cards
        for i, upgrade in enumerate(self.choices):
            card_x = start_x + (i * (self.card_width + self.card_spacing))
            card_y = start_y

            self._draw_upgrade_card(screen, upgrade, card_x, card_y, i + 1)

        # Draw instruction text
        instruction_text = self.font_small.render(
            "Press 1, 2, or 3 to choose", True, Colors.WHITE
        )
        instruction_rect = instruction_text.get_rect(
            center=(screen_width // 2, screen_height - 80)
        )
        screen.blit(instruction_text, instruction_rect)

    def _draw_upgrade_card(self, screen, upgrade, x, y, number):
        """
        Draw individual upgrade card

        Args:
            screen: Pygame surface
            upgrade: Upgrade instance
            x: Card x position
            y: Card y position
            number: Card number (1, 2, 3)
        """
        # Card background
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        pygame.draw.rect(screen, self.card_color, card_rect)
        pygame.draw.rect(screen, self.card_border_color, card_rect, 3)

        # Number badge
        number_text = self.font_medium.render(f"[{number}]", True, Colors.YELLOW)
        number_rect = number_text.get_rect(center=(x + self.card_width // 2, y + 30))
        screen.blit(number_text, number_rect)

        # Icon
        icon_text = self.font_large.render(upgrade.icon_text, True, Colors.WHITE)
        icon_rect = icon_text.get_rect(center=(x + self.card_width // 2, y + 100))
        screen.blit(icon_text, icon_rect)

        # Upgrade name (wrapped)
        name_lines = self._wrap_text(
            upgrade.name, self.card_width - 20, self.font_small
        )
        name_y = y + 160
        for line in name_lines:
            name_text = self.font_small.render(line, True, Colors.WHITE)
            name_rect = name_text.get_rect(center=(x + self.card_width // 2, name_y))
            screen.blit(name_text, name_rect)
            name_y += 30

        # Upgrade description
        desc_lines = self._wrap_text(
            upgrade.description, self.card_width - 20, self.font_small
        )
        desc_y = y + 230
        for line in desc_lines:
            desc_text = self.font_small.render(line, True, Colors.GRAY)
            desc_rect = desc_text.get_rect(center=(x + self.card_width // 2, desc_y))
            screen.blit(desc_text, desc_rect)
            desc_y += 28

    def _wrap_text(self, text, max_width, font):
        """
        Wrap text to fit within width

        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            font: Pygame font

        Returns:
            list: List of text lines
        """
        words = text.split(" ")
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            test_surface = font.render(test_line, True, Colors.WHITE)

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines
