"""
Pickup Manager
Manages all pickups (XP orbs, health, powerups, etc.)
"""

from src.entities.pickups import XPOrb, HealthPickup


class PickupManager:
    """Manages pickup spawning and collection"""

    def __init__(self):
        """Initialize pickup manager"""
        pass

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
