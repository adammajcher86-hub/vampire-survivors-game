"""
Event Bus
Central publish/subscribe event system
Allows decoupled communication between game systems
"""

from typing import Callable, Dict, List
from collections import defaultdict
from .event_types import EventData, create_event_data


class EventBus:
    """
    Central event bus for publish/subscribe pattern

    Usage:
        # Subscribe to events
        event_bus.subscribe("enemy_killed", on_enemy_killed)

        # Emit events
        event_bus.emit("enemy_killed", enemy=enemy, position=pos)
    """

    def __init__(self):
        """Initialize event bus"""
        # Store subscribers: {event_type: [callback1, callback2, ...]}
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)

        # Store one-time subscribers
        self._once_subscribers: Dict[str, List[Callable]] = defaultdict(list)

        # Event history (for debugging)
        self._event_history: List[tuple] = []
        self._max_history = 100

        # Statistics
        self._stats = {
            "total_emits": 0,
            "total_subscriptions": 0,
        }

    # ==================== SUBSCRIPTION ====================

    def subscribe(self, event_type: str, callback: Callable) -> Callable:
        """
        Subscribe to an event type

        Args:
            event_type: Event type to listen for
            callback: Function to call when event occurs
                     Signature: callback(event_data) or callback()

        Returns:
            Unsubscribe function

        Example:
            def on_enemy_killed(event):
                print(f"Enemy killed at {event.position}")

            unsubscribe = event_bus.subscribe("enemy_killed", on_enemy_killed)
            # Later: unsubscribe()
        """
        self._subscribers[event_type].append(callback)
        self._stats["total_subscriptions"] += 1

        # Return unsubscribe function
        def unsubscribe():
            self.unsubscribe(event_type, callback)

        return unsubscribe

    def subscribe_once(self, event_type: str, callback: Callable) -> Callable:
        """
        Subscribe to event, but only fire once

        Args:
            event_type: Event type to listen for
            callback: Function to call (once)

        Returns:
            Unsubscribe function
        """
        self._once_subscribers[event_type].append(callback)

        def unsubscribe():
            if callback in self._once_subscribers[event_type]:
                self._once_subscribers[event_type].remove(callback)

        return unsubscribe

    def unsubscribe(self, event_type: str, callback: Callable):
        """
        Unsubscribe from an event

        Args:
            event_type: Event type
            callback: Callback to remove
        """
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    def unsubscribe_all(self, event_type: str = None):
        """
        Unsubscribe all callbacks

        Args:
            event_type: If provided, only clear this event type
                       If None, clear all events
        """
        if event_type:
            self._subscribers[event_type].clear()
            self._once_subscribers[event_type].clear()
        else:
            self._subscribers.clear()
            self._once_subscribers.clear()

    # ==================== EMISSION ====================

    def emit(self, event_type: str, **kwargs):
        """
        Emit an event to all subscribers

        Args:
            event_type: Type of event
            **kwargs: Event data (passed to callbacks)

        Example:
            event_bus.emit("enemy_killed",
                          enemy=enemy,
                          position=enemy.position,
                          killer="laser")
        """
        self._stats["total_emits"] += 1

        # Create event data
        event_data = create_event_data(event_type, **kwargs)

        # Add to history
        self._add_to_history(event_type, event_data)

        # Call regular subscribers
        for callback in self._subscribers[event_type][
            :
        ]:  # Copy list to avoid modification issues
            self._safe_call(callback, event_data)

        # Call one-time subscribers
        for callback in self._once_subscribers[event_type][:]:
            self._safe_call(callback, event_data)

        # Clear one-time subscribers
        self._once_subscribers[event_type].clear()

    def _safe_call(self, callback: Callable, event_data: EventData):
        """
        Safely call callback, handling errors

        Args:
            callback: Function to call
            event_data: Data to pass
        """
        try:
            # Try calling with event data
            callback(event_data)
        except TypeError:
            # If callback doesn't accept arguments, call without
            try:
                callback()
            except Exception as e:
                print(f"⚠️ Event callback error: {e}")
        except Exception as e:
            print(f"⚠️ Event callback error: {e}")

    # ==================== HISTORY & DEBUG ====================

    def _add_to_history(self, event_type: str, event_data: EventData):
        """Add event to history"""
        self._event_history.append((event_type, event_data))

        # Trim history
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history :]

    def get_history(self, event_type: str = None, limit: int = 10) -> List[tuple]:
        """
        Get recent event history

        Args:
            event_type: Filter by event type (None = all events)
            limit: Max number of events to return

        Returns:
            List of (event_type, event_data) tuples
        """
        history = self._event_history

        # Filter by type if specified
        if event_type:
            history = [h for h in history if h[0] == event_type]

        # Return last N events
        return history[-limit:]

    def get_stats(self) -> dict:
        """Get event bus statistics"""
        return {
            **self._stats,
            "active_subscriptions": sum(
                len(subs) for subs in self._subscribers.values()
            ),
            "event_types": len(self._subscribers),
        }

    def get_subscribers(self, event_type: str = None) -> dict:
        """
        Get subscriber information

        Args:
            event_type: If provided, only show this event type

        Returns:
            Dict of event types and subscriber counts
        """
        if event_type:
            return {event_type: len(self._subscribers[event_type])}

        return {
            event_type: len(callbacks)
            for event_type, callbacks in self._subscribers.items()
            if callbacks  # Only show events with subscribers
        }

    # ==================== UTILITY ====================

    def clear_history(self):
        """Clear event history"""
        self._event_history.clear()

    def reset(self):
        """Reset event bus completely"""
        self.unsubscribe_all()
        self.clear_history()
        self._stats = {
            "total_emits": 0,
            "total_subscriptions": 0,
        }


# ==================== GLOBAL EVENT BUS ====================

# Global singleton event bus
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance"""
    return _event_bus


def subscribe(event_type: str, callback: Callable) -> Callable:
    """Convenience function for global event bus subscribe"""
    return _event_bus.subscribe(event_type, callback)


def emit(event_type: str, **kwargs):
    """Convenience function for global event bus emit"""
    _event_bus.emit(event_type, **kwargs)


def unsubscribe(event_type: str, callback: Callable):
    """Convenience function for global event bus unsubscribe"""
    _event_bus.unsubscribe(event_type, callback)
