"""
Drop Tables
Defines what pickups each enemy type can drop
"""

# Drop table format: (weight, pickup_type, params)

DROP_TABLES = {
    "BasicEnemy": [
        (90, "xp_orb", {"xp_value": 1}),
        (1, "health_pickup", {"heal_amount": 10}),  #
        (2, "bomb_pickup", {"bomb_amount": 1}),  # 2% chance
    ],
    "FastEnemy": [
        (85, "xp_orb", {"xp_value": 2}),
        (2, "health_pickup", {"heal_amount": 15}),  #
        (1, "bomb_pickup", {"bomb_amount": 1}),  # 2% chance
    ],
    "TankEnemy": [
        (70, "xp_orb", {"xp_value": 3}),
        (5, "health_pickup", {"heal_amount": 25}),  # ✅ Reduced from 25 to 20
        (2, "health_pickup", {"heal_amount": 50}),  # ✅ Big health same
        (1, "bomb_pickup", {"bomb_amount": 1}),  # ✅ 5% chance, 1 bomb
    ],
    "EliteEnemy": [
        (60, "xp_orb", {"xp_value": 5}),
        (5, "health_pickup", {"heal_amount": 30}),  # ✅ Reduced from 25 to 20
        (10, "xp_orb", {"xp_value": 10}),  # Rare bonus XP
        (2, "health_pickup", {"heal_amount": 100}),  # Super rare full heal
        (2, "bomb_pickup", {"bomb_amount": 1}),  # ✅ 5% chance, 1 bombs
    ],
}

# Default drop table for unknown enemy types
DEFAULT_DROP_TABLE = [
    (90, "xp_orb", {"xp_value": 1}),
    (8, "health_pickup", {"heal_amount": 10}),
    (2, "bomb_pickup", {"bomb_amount": 1}),
]
