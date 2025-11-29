"""
Pickup Manager
Manages all pickups (XP orbs, health, powerups, etc.)
"""

import random
from src.entities.pickups import XPOrb, HealthPickup
from .drop_tables import DROP_TABLES, DEFAULT_DROP_TABLE


class PickupManager:
    """Manages pickup spawning and collection"""

    def __init__(self):
        """Initialize pickup manager"""
        pass

    def spawn_from_enemy(self, enemy, pickups):
        """
        Spawn a pickup based on enemy's drop table

        Args:
            enemy: Enemy that died
            pickups: Sprite group to add pickup to
        """
        # Get enemy type name
        enemy_type = enemy.__class__.__name__

        # Get drop table for this enemy type
        drop_table = DROP_TABLES.get(enemy_type, DEFAULT_DROP_TABLE)

        # Select pickup based on weighted probabilities
        pickup_type, params = self._weighted_choice(drop_table)

        # Spawn the selected pickup
        if pickup_type == "xp_orb":
            self.spawn_xp_orb(
                enemy.position.x, enemy.position.y, params["xp_value"], pickups
            )
        elif pickup_type == "health_pickup":
            self.spawn_health_pickup(
                enemy.position.x, enemy.position.y, params["heal_amount"], pickups
            )
        # Future pickup types go here

    def _weighted_choice(self, drop_table):
        """
        Choose a pickup from drop table using weighted probability

        Args:
            drop_table: List of (weight, pickup_type, params) tuples

        Returns:
            tuple: (pickup_type, params)
        """
        # Calculate total weight
        total_weight = sum(weight for weight, _, _ in drop_table)

        # Random value between 0 and total_weight
        rand = random.uniform(0, total_weight)

        # Find which pickup this falls into
        current = 0
        for weight, pickup_type, params in drop_table:
            current += weight
            if rand <= current:
                return (pickup_type, params)

        # Fallback (shouldn't happen)
        return drop_table[0][1], drop_table[0][2]

    def spawn_xp_orb(self, x, y, xp_value, pickups):
        """
        Spawn an XP orb at position

        Args:
            x: X position
            y: Y position
            xp_value: Amount of XP this orb gives
            pickups: Sprite group to add orb to
        """
        xp_orb = XPOrb(x, y, xp_value)
        pickups.add(xp_orb)

    def spawn_health_pickup(self, x, y, heal_amount, pickups):
        """
        Spawn a health pickup at position

        Args:
            x: X position
            y: Y position
            heal_amount: Amount of HP restored
            pickups: Sprite group to add pickup to
        """
        health_pickup = HealthPickup(x, y, heal_amount)
        pickups.add(health_pickup)

    def collect_pickups(self, player, pickups):
        """
        Collect all pickups within player range (polymorphic!)

        Args:
            player: Player entity
            pickups: Sprite group of all pickups

        Returns:
            int: Total XP collected (for XP system)
        """
        collected_xp = 0

        for pickup in list(pickups):
            # Use actual visual collision (pickup radius + player radius)
            distance = pickup.position.distance_to(player.position)
            if distance < (pickup.radius + player.radius):
                # Polymorphic collection! Each pickup type handles itself
                value = pickup.on_collect(player)

                # Only count XP from XP orbs
                if hasattr(pickup, "xp_value"):
                    collected_xp += value

                # Remove pickup
                pickups.remove(pickup)

        return collected_xp
