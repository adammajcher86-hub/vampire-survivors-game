"""
Chain Laser Weapon Configuration
A continuous beam weapon that locks onto enemies and does damage over time.
Can chain to nearby enemies when upgraded.
"""


class ChainLaserConfig:
    """Configuration for chain laser weapon"""

    # Weapon properties
    COOLDOWN = 0.1  # How often it can switch targets
    DAMAGE_PER_SECOND = 50  # DOT damage
    RANGE = 300  # Maximum lock-on range
    AUTO_AIM = True  # Automatically targets nearest enemy

    # Beam visual properties
    BEAM_COLOR = (100, 200, 255)  # Light blue beam
    BEAM_GLOW_COLOR = (150, 220, 255)  # Outer glow
    BEAM_WIDTH = 3
    BEAM_GLOW_WIDTH = 6

    # Chain properties (unlocked at level 2+)
    CHAIN_ENABLED_AT_LEVEL = 2  # Enable chaining at level 2
    CHAIN_RANGE = 150  # How far it can jump to next enemy
    MAX_CHAIN_COUNT_BY_LEVEL = {
        1: 0,  # No chaining at level 1
        2: 1,  # Can chain to 1 additional enemy
        3: 1,
        4: 2,  # Can chain to 2 additional enemies
        5: 2,
        6: 3,  # Can chain to 3 additional enemies
        7: 3,
        8: 4,  # Maximum 4 chains
    }

    # Damage scaling per level
    DAMAGE_MULTIPLIER_BY_LEVEL = {
        1: 1.0,
        2: 1.2,
        3: 1.4,
        4: 1.6,
        5: 1.9,
        6: 2.2,
        7: 2.5,
        8: 3.0,
    }

    @classmethod
    def get_max_chains(cls, level):
        """Get maximum chain count for weapon level"""
        return cls.MAX_CHAIN_COUNT_BY_LEVEL.get(level, 0)

    @classmethod
    def get_damage_per_second(cls, level):
        """Get DPS for weapon level"""
        multiplier = cls.DAMAGE_MULTIPLIER_BY_LEVEL.get(level, 1.0)
        return cls.DAMAGE_PER_SECOND * multiplier

    @classmethod
    def can_chain(cls, level):
        """Check if weapon can chain at this level"""
        return level >= cls.CHAIN_ENABLED_AT_LEVEL
