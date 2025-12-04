"""
Bomb Configuration
Parameters for bomb weapon
"""


class BombConfig:
    """Bomb weapon configuration"""

    # Explosion parameters
    EXPLOSION_RADIUS = 120  # pixels
    EXPLOSION_DAMAGE = 120  # damage to enemies
    EXPLOSION_DELAY = 2.5  # seconds before explosion

    # Player damage
    PLAYER_DAMAGE = 40  # damage to player if caught in blast

    # Starting inventory
    STARTING_BOMBS = 3  # bombs player starts with
    MAX_BOMBS = 10  # maximum bombs player can carry

    # Visual
    BOMB_SIZE = 8  # bomb sprite radius
    BOMB_COLOR = (50, 50, 50)  # dark gray
    WARNING_COLOR = (255, 0, 0)  # red
    PULSE_SPEED = 8.0  # warning circle pulse speed

    # Placement cooldown
    PLACEMENT_COOLDOWN = 2.0
