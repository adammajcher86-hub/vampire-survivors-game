"""
Stat Upgrade
Boosts player stats (speed, pickup range, max health, etc.)
"""

from src.upgrades.base_upgrade import BaseUpgrade


class StatUpgrade(BaseUpgrade):
    """Upgrade that boosts player stats"""

    def __init__(
        self, stat_name, stat_attribute, amount, is_percentage=False, icon="⚡"
    ):
        """
        Initialize stat upgrade

        Args:
            stat_name: Display name (e.g., "Speed")
            stat_attribute: Player attribute name (e.g., "speed")
            amount: Amount to increase (e.g., 10 for +10 or 0.1 for +10%)
            is_percentage: If True, amount is percentage (multiply), else absolute (add)
            icon: Icon text for display
        """
        if is_percentage:
            desc = f"+{int(amount * 100)}% {stat_name}"
        else:
            desc = f"+{amount} {stat_name}"

        super().__init__(name=f"Boost: {stat_name}", description=desc, icon_text=icon)

        self.stat_name = stat_name
        self.stat_attribute = stat_attribute
        self.amount = amount
        self.is_percentage = is_percentage

    def can_apply(self, player, weapons):
        """
        Check if stat upgrade can be applied

        Args:
            player: Player entity
            weapons: List of player weapons

        Returns:
            bool: Always True (stats can always be upgraded)
        """
        # Could add max limits here if needed
        return True

    def apply(self, player, weapons):
        """
        Apply stat boost to player

        Args:
            player: Player entity
            weapons: List of player weapons

        Returns:
            str: Success message
        """
        if not hasattr(player, self.stat_attribute):
            return f"Player doesn't have attribute: {self.stat_attribute}"

        old_value = getattr(player, self.stat_attribute)

        if self.is_percentage:
            # Percentage increase (multiply)
            new_value = old_value * (1 + self.amount)
        else:
            # Absolute increase (add)
            new_value = old_value + self.amount

        setattr(player, self.stat_attribute, new_value)

        return f"{self.stat_name} increased! ({old_value:.0f} → {new_value:.0f})"
