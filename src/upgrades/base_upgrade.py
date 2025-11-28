"""
Base Upgrade
Abstract base class for all upgrades
"""

from abc import ABC, abstractmethod


class BaseUpgrade(ABC):
    """Base class for all upgrades"""

    def __init__(self, name, description, icon_text=None):
        """
        Initialize base upgrade

        Args:
            name: Upgrade name
            description: Upgrade description
            icon_text: Optional icon text (emoji or short text)
        """
        self.name = name
        self.description = description
        self.icon_text = icon_text or "?"

    @abstractmethod
    def can_apply(self, player, weapons):
        """
        Check if upgrade can be applied

        Args:
            player: Player entity
            weapons: List of player weapons

        Returns:
            bool: True if upgrade can be applied
        """
        pass

    @abstractmethod
    def apply(self, player, weapons):
        """
        Apply the upgrade

        Args:
            player: Player entity
            weapons: List of player weapons

        Returns:
            str: Message describing what was upgraded
        """
        pass

    def get_display_info(self):
        """
        Get display information for UI

        Returns:
            dict: Display info with name, description, icon
        """
        return {
            "name": self.name,
            "description": self.description,
            "icon": self.icon_text,
        }
