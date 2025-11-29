"""
Drop Tables
Defines what pickups each enemy type can drop
"""

# Drop table format: (weight, pickup_type, params)
# weight: relative probability (doesn't need to add to 1.0)
# pickup_type: 'xp_orb', 'health_pickup', etc.
# params: dict of parameters for that pickup type

DROP_TABLES = {
    "BasicEnemy": [
        (95, "xp_orb", {"xp_value": 1}),
        (5, "health_pickup", {"heal_amount": 10}),
    ],
    "FastEnemy": [
        (90, "xp_orb", {"xp_value": 2}),
        (10, "health_pickup", {"heal_amount": 15}),
    ],
    "TankEnemy": [
        (70, "xp_orb", {"xp_value": 3}),
        (25, "health_pickup", {"heal_amount": 25}),
        (5, "health_pickup", {"heal_amount": 50}),  # Rare big health!
    ],
    "EliteEnemy": [
        (60, "xp_orb", {"xp_value": 5}),
        (25, "health_pickup", {"heal_amount": 30}),
        (10, "xp_orb", {"xp_value": 10}),  # Rare bonus XP!
        (5, "health_pickup", {"heal_amount": 100}),  # Super rare full heal!
    ],
}

# Default drop table for unknown enemy types
DEFAULT_DROP_TABLE = [
    (90, "xp_orb", {"xp_value": 1}),
    (10, "health_pickup", {"heal_amount": 10}),
]
