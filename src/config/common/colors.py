"""
Color Palette Configuration
Centralized color definitions for the entire game
"""


class Colors:
    """Color palette - RGB tuples"""

    # Basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Primary colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Secondary colors
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    # Game colors
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)

    # UI colors
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)

    # Semantic colors (for clarity in code)
    BACKGROUND = DARK_GRAY
    UI_TEXT = WHITE
    UI_ACCENT = YELLOW
    HEALTH_BAR = GREEN
    DAMAGE_INDICATOR = RED