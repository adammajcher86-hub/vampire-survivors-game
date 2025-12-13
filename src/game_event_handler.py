"""
Game Event Handler
Centralizes all game event subscriptions and handlers
Keeps game_engine.py clean and focused
"""

from src.systems.events import get_event_bus, GameEvent
from src.logger import logger


class GameEventHandler:
    """
    Manages all game event subscriptions and handlers
    Decouples event logic from game engine
    """

    def __init__(self, game):
        """
        Initialize event handler

        Args:
            game: Reference to Game instance (for accessing systems)
        """
        self.game = game
        self.event_bus = get_event_bus()

        # Setup all event listeners
        self._setup_listeners()

    def _setup_listeners(self):
        """Subscribe to all game events"""

        # ==================== COMBAT EVENTS ====================
        # Enemy killed
        self.event_bus.subscribe(GameEvent.ENEMY_KILLED, self._on_enemy_killed_effects)
        self.event_bus.subscribe(GameEvent.ENEMY_KILLED, self._on_enemy_killed_stats)

        # Projectile hit
        self.event_bus.subscribe(
            GameEvent.PROJECTILE_HIT, self._on_projectile_hit_effects
        )

        # Bomb exploded
        self.event_bus.subscribe(
            GameEvent.BOMB_EXPLODED, self._on_bomb_exploded_effects
        )

        # ==================== PLAYER EVENTS ====================
        # Player damaged
        self.event_bus.subscribe(
            GameEvent.PLAYER_DAMAGED, self._on_player_damaged_effects
        )

        # ==================== PROGRESSION EVENTS ====================
        # XP gained
        self.event_bus.subscribe(GameEvent.XP_GAINED, self._on_xp_gained_stats)

        # Level up
        self.event_bus.subscribe(GameEvent.LEVEL_UP, self._on_level_up_effects)

        # Wave started
        self.event_bus.subscribe(GameEvent.WAVE_STARTED, self._on_wave_started_ui)

        logger.debug("✅ Event handlers registered")

    # ==================== COMBAT EVENT HANDLERS ====================

    def _on_enemy_killed_effects(self, event):
        """Visual effects for enemy death"""
        self.game.effect_manager.enemy_death(event.position, event.enemy_type)

    def _on_enemy_killed_stats(self, event):
        """Track enemy kills"""
        self.game.enemies_killed += 1

    def _on_projectile_hit_effects(self, event):
        """Visual effects for projectile hit"""
        direction = (event.enemy.position - event.projectile.position).normalize()
        self.game.effect_manager.projectile_hit(event.position, direction)

    def _on_bomb_exploded_effects(self, event):
        """Visual effects for bomb explosion"""
        self.game.effect_manager.bomb_explosion(event.position)

    # ==================== PLAYER EVENT HANDLERS ====================

    def _on_player_damaged_effects(self, event):
        """Visual effects for player damage"""
        self.game.effect_manager.player_damage()

    # ==================== PROGRESSION EVENT HANDLERS ====================

    def _on_xp_gained_stats(self, event):
        """Track XP collection"""
        self.game.xp_collected = event.total_collected

    def _on_level_up_effects(self, event):
        """Handle level up"""
        self.game.effect_manager.level_up(self.game.player.position)
        self.game._show_upgrade_menu()

    def _on_wave_started_ui(self, event):
        """Display wave start info"""
        logger.info(f"🌊 WAVE {event.wave_number} START!")
        logger.info(f"Enemies: {event.enemy_count}, Spawn rate: {event.spawn_rate}/s")

    # ==================== UTILITY ====================

    def cleanup(self):
        """Cleanup event subscriptions (call on game exit)"""
        self.event_bus.unsubscribe_all()
        logger.debug("🧹 Event handlers cleaned up")

    def get_stats(self):
        """Get event bus statistics (for debugging)"""
        return self.event_bus.get_stats()

    def get_subscribers(self):
        """Get subscriber counts per event"""
        return self.event_bus.get_subscribers()
