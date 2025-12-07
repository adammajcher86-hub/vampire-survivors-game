"""
Game Logger Configuration
Simple on/off logging system
"""

import logging
import sys


class GameLogger:
    """Simple game logger with debug control"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not GameLogger._initialized:
            self.logger = logging.getLogger("VampireSurvivors")
            self.logger.setLevel(logging.DEBUG)

            # Console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)  # Default to INFO

            # Formatter with emojis preserved
            formatter = logging.Formatter("%(levelname)s: %(message)s")
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)
            self.handler = handler

            GameLogger._initialized = True

    def set_debug_mode(self, enabled):
        """Enable or disable debug logging"""
        if enabled:
            self.handler.setLevel(logging.DEBUG)
            self.logger.info("🔧 Debug mode enabled")
        else:
            self.handler.setLevel(logging.INFO)

    def get_logger(self):
        """Get the logger instance"""
        return self.logger


# Global logger instance
_game_logger = GameLogger()
logger = _game_logger.get_logger()


def set_debug_mode(enabled):
    """Global function to set debug mode"""
    _game_logger.set_debug_mode(enabled)
