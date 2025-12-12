"""
Input Configuration
Customizable key bindings for the game
"""

import pygame


class InputConfig:
    """Configuration for input mappings"""

    # Movement keys (multiple keys per direction for flexibility)
    MOVE_UP = [pygame.K_w, pygame.K_UP]
    MOVE_DOWN = [pygame.K_s, pygame.K_DOWN]
    MOVE_LEFT = [pygame.K_a, pygame.K_LEFT]
    MOVE_RIGHT = [pygame.K_d, pygame.K_RIGHT]

    # Action keys
    DASH = pygame.K_SPACE
    PAUSE = pygame.K_ESCAPE
    DEBUG_TOGGLE = pygame.K_F3

    # Mouse buttons
    BOMB_BUTTON = 3  # Right mouse button (1=left, 2=middle, 3=right)

    # Upgrade menu keys (1-3 for selecting upgrades)
    UPGRADE_KEY_1 = pygame.K_1
    UPGRADE_KEY_2 = pygame.K_2
    UPGRADE_KEY_3 = pygame.K_3

    # Game over keys
    RESTART = pygame.K_r
    QUIT = pygame.K_ESCAPE


# ✅ Easy to customize!
# Just change the values above to remap keys
# Example: Change dash to Left Shift
# DASH = pygame.K_LSHIFT
