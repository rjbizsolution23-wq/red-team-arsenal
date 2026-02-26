"""
🔴💀 Hive Mind — Real-time shared blackboard for autonomous agent collaboration
"""
import threading
from typing import Dict, List, Any, Callable
from loguru import logger

class HiveMind:
    """
    A thread-safe shared state for all agents.
    Allows agents to post events and subscribe to findings.
    """
    def __init__(self):
        self._state: Dict[str, Any] = {
            "findings": [],
            "credentials": [],
            "targets": [],
            "exploits": []
        }
        self._subscriptions: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()

    def post(self, event_type: str, data: Any):
        """Post a new finding or event to the blackboard."""
        with self._lock:
            logger.info(f"[HiveMind] 📥 New Event: {event_type}")
            if event_type in self._state:
                if isinstance(self._state[event_type], list):
                    self._state[event_type].append(data)
                else:
                    self._state[event_type] = data
            else:
                self._state[event_type] = [data]

            # Trigger subscribers
            self._notify(event_type, data)

    def subscribe(self, event_type: str, callback: Callable):
        """Register a callback for a specific event type."""
        with self._lock:
            if event_type not in self._subscriptions:
                self._subscriptions[event_type] = []
            self._subscriptions[event_type].append(callback)
            logger.debug(f"[HiveMind] Agent subscribed to {event_type}")

    def _notify(self, event_type: str, data: Any):
        """Notify all subscribers of an event."""
        if event_type in self._subscriptions:
            for callback in self._subscriptions[event_type]:
                try:
                    # In a real system, this would be an async task or thread
                    callback(data)
                except Exception as e:
                    logger.error(f"[HiveMind] Notification failed: {e}")

    def get_snapshot(self) -> Dict[str, Any]:
        """Get the current global state."""
        with self._lock:
            return self._state.copy()
