"""
Event Types
Defines all event types in the game
"""


class GameEvent:
    """Game event type constants"""

    # ==================== PLAYER EVENTS ====================
    PLAYER_DAMAGED = "player_damaged"
    PLAYER_HEALED = "player_healed"
    PLAYER_DIED = "player_died"
    PLAYER_DASHED = "player_dashed"
    PLAYER_MOVED = "player_moved"

    # ==================== COMBAT EVENTS ====================
    ENEMY_SPAWNED = "enemy_spawned"
    ENEMY_DAMAGED = "enemy_damaged"
    ENEMY_KILLED = "enemy_killed"
    PROJECTILE_FIRED = "projectile_fired"
    PROJECTILE_HIT = "projectile_hit"
    BOMB_PLACED = "bomb_placed"
    BOMB_EXPLODED = "bomb_exploded"

    # ==================== PROGRESSION EVENTS ====================
    XP_GAINED = "xp_gained"
    LEVEL_UP = "level_up"
    UPGRADE_SELECTED = "upgrade_selected"
    WAVE_STARTED = "wave_started"
    WAVE_COMPLETED = "wave_completed"

    # ==================== PICKUP EVENTS ====================
    PICKUP_SPAWNED = "pickup_spawned"
    PICKUP_COLLECTED = "pickup_collected"

    # ==================== WEAPON EVENTS ====================
    WEAPON_ACQUIRED = "weapon_acquired"
    WEAPON_UPGRADED = "weapon_upgraded"
    WEAPON_FIRED = "weapon_fired"

    # ==================== UI EVENTS ====================
    MENU_OPENED = "menu_opened"
    MENU_CLOSED = "menu_closed"
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"

    # ==================== GAME STATE EVENTS ====================
    GAME_STARTED = "game_started"
    GAME_OVER = "game_over"
    GAME_RESTARTED = "game_restarted"

    # ==================== ACHIEVEMENT EVENTS (Future) ====================
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    MILESTONE_REACHED = "milestone_reached"


# ==================== EVENT DATA CLASSES ====================


class EventData:
    """Base class for event data"""

    def __init__(self, **kwargs):
        """Store arbitrary event data as attributes"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class PlayerDamagedEvent(EventData):
    """
    Data for PLAYER_DAMAGED event

    Attributes:
        damage: Amount of damage taken
        source: What caused the damage (enemy, projectile, etc.)
        position: Where damage occurred
    """

    pass


class EnemyKilledEvent(EventData):
    """
    Data for ENEMY_KILLED event

    Attributes:
        enemy: Enemy entity that died
        enemy_type: Type of enemy (e.g., "BasicEnemy")
        position: Where enemy died
        killer: What killed the enemy (weapon, bomb, etc.)
    """

    pass


class LevelUpEvent(EventData):
    """
    Data for LEVEL_UP event

    Attributes:
        new_level: Player's new level
        xp_required: XP needed for next level
        player: Player entity
    """

    pass


class PickupCollectedEvent(EventData):
    """
    Data for PICKUP_COLLECTED event

    Attributes:
        pickup_type: Type of pickup (xp, health, etc.)
        value: Value of pickup
        position: Where pickup was collected
    """

    pass


class WaveStartedEvent(EventData):
    """
    Data for WAVE_STARTED event

    Attributes:
        wave_number: Current wave number
        enemy_count: Number of enemies in this wave
        spawn_rate: Enemies per second
    """

    pass


# ==================== HELPER FUNCTIONS ====================


def create_event_data(event_type, **kwargs):
    """
    Create appropriate EventData instance for event type

    Args:
        event_type: Event type constant
        **kwargs: Event data

    Returns:
        EventData instance
    """
    # Map event types to specific data classes
    event_classes = {
        GameEvent.PLAYER_DAMAGED: PlayerDamagedEvent,
        GameEvent.ENEMY_KILLED: EnemyKilledEvent,
        GameEvent.LEVEL_UP: LevelUpEvent,
        GameEvent.PICKUP_COLLECTED: PickupCollectedEvent,
        GameEvent.WAVE_STARTED: WaveStartedEvent,
    }

    # Use specific class if available, otherwise generic EventData
    event_class = event_classes.get(event_type, EventData)
    return event_class(**kwargs)
