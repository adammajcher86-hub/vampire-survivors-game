"""
Vampire Survivors Clone - Main Entry Point
A bullet-heaven style game built with Pygame
"""
import pygame
import sys
from src.game import Game
from src.config import WindowConfig


def main():
    """Initialize and run the game"""
    pygame.init()

    # Create the game window
    screen = pygame.display.set_mode((WindowConfig.WIDTH, WindowConfig.HEIGHT))
    pygame.display.set_caption(WindowConfig.TITLE)

    # Create game instance
    game = Game(screen)

    # Main game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(WindowConfig.FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        # Update game state
        game.update(dt)

        # Render
        game.render()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()