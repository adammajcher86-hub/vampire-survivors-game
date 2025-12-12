"""
Input Handler
Centralized input management system
Handles keyboard, mouse, and event processing
"""

import pygame
from .input_config import InputConfig


class InputHandler:
    """Handles all player input"""

    def __init__(self):
        """Initialize input handler"""
        # Current frame state
        self.keys_pressed = {}
        self.keys_just_pressed = set()
        self.keys_just_released = set()

        # Mouse state
        self.mouse_buttons_pressed = {}
        self.mouse_buttons_just_pressed = set()
        self.mouse_buttons_just_released = set()
        self.mouse_screen_pos = pygame.math.Vector2(0, 0)
        self.mouse_world_pos = pygame.math.Vector2(0, 0)

        # Previous frame state (for detecting "just pressed")
        self.previous_keys = set()
        self.previous_mouse_buttons = set()

    def update(self, camera_offset):
        """
        Update input state (call once per frame at start of update)

        Args:
            camera_offset: Camera offset for mouse world position
        """
        # Get current keyboard state
        keys = pygame.key.get_pressed()
        current_keys = {i for i in range(len(keys)) if keys[i]}

        # Detect just pressed/released
        self.keys_just_pressed = current_keys - self.previous_keys
        self.keys_just_released = self.previous_keys - current_keys
        self.previous_keys = current_keys

        # Update keys_pressed dict for easy access
        self.keys_pressed = {i: keys[i] for i in range(len(keys))}

        # Get current mouse state
        mouse_buttons = pygame.mouse.get_pressed()
        current_mouse = {i for i in range(len(mouse_buttons)) if mouse_buttons[i]}

        # Detect mouse just pressed/released
        self.mouse_buttons_just_pressed = current_mouse - self.previous_mouse_buttons
        self.mouse_buttons_just_released = self.previous_mouse_buttons - current_mouse
        self.previous_mouse_buttons = current_mouse

        # Update mouse buttons dict
        self.mouse_buttons_pressed = {
            i: mouse_buttons[i] for i in range(len(mouse_buttons))
        }

        # Update mouse positions
        self.mouse_screen_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.mouse_world_pos = pygame.math.Vector2(
            self.mouse_screen_pos.x + camera_offset.x,
            self.mouse_screen_pos.y + camera_offset.y,
        )

    # ==================== MOVEMENT ====================

    def get_movement_vector(self):
        """
        Get movement direction as a vector

        Returns:
            tuple: (dx, dy) where each is -1, 0, or 1
        """
        dx = 0
        dy = 0

        # Check all configured movement keys
        for key in InputConfig.MOVE_RIGHT:
            if self.is_key_pressed(key):
                dx += 1
                break

        for key in InputConfig.MOVE_LEFT:
            if self.is_key_pressed(key):
                dx -= 1
                break

        for key in InputConfig.MOVE_DOWN:
            if self.is_key_pressed(key):
                dy += 1
                break

        for key in InputConfig.MOVE_UP:
            if self.is_key_pressed(key):
                dy -= 1
                break

        return (dx, dy)

    def is_moving(self):
        """Check if player is pressing any movement keys"""
        dx, dy = self.get_movement_vector()
        return dx != 0 or dy != 0

    # ==================== ACTIONS ====================

    def is_key_pressed(self, key):
        """Check if a key is currently held down"""
        return self.keys_pressed.get(key, False)

    def is_key_just_pressed(self, key):
        """Check if a key was just pressed this frame"""
        return key in self.keys_just_pressed

    def is_key_just_released(self, key):
        """Check if a key was just released this frame"""
        return key in self.keys_just_released

    def dash_pressed(self):
        """Check if dash action was just pressed"""
        return self.is_key_just_pressed(InputConfig.DASH)

    def pause_pressed(self):
        """Check if pause action was just pressed"""
        return self.is_key_just_pressed(InputConfig.PAUSE)

    def debug_toggle_pressed(self):
        """Check if debug toggle was just pressed"""
        return self.is_key_just_pressed(InputConfig.DEBUG_TOGGLE)

    def restart_pressed(self):
        """Check if restart action was just pressed"""
        return self.is_key_just_pressed(InputConfig.RESTART)

    def quit_pressed(self):
        """Check if quit action was just pressed"""
        return self.is_key_just_pressed(InputConfig.QUIT)

    # ==================== MOUSE ====================

    def is_mouse_button_pressed(self, button):
        """
        Check if mouse button is currently held down

        Args:
            button: Button number (0=left, 1=middle, 2=right)
        """
        return self.mouse_buttons_pressed.get(button, False)

    def is_mouse_button_just_pressed(self, button):
        """
        Check if mouse button was just pressed this frame

        Args:
            button: Button number (0=left, 1=middle, 2=right)
        """
        return button in self.mouse_buttons_just_pressed

    def is_mouse_button_just_released(self, button):
        """Check if mouse button was just released this frame"""
        return button in self.mouse_buttons_just_released

    def bomb_pressed(self):
        """Check if bomb action (right click) was just pressed"""
        return self.is_mouse_button_just_pressed(
            InputConfig.BOMB_BUTTON - 1
        )  # pygame uses 0-indexed

    def get_mouse_screen_pos(self):
        """Get mouse position in screen space"""
        return self.mouse_screen_pos

    def get_mouse_world_pos(self):
        """Get mouse position in world space"""
        return self.mouse_world_pos

    # ==================== UPGRADE MENU ====================

    def get_upgrade_selection(self):
        """
        Check if player pressed an upgrade selection key

        Returns:
            int or None: 0-2 for upgrade selection, None if no selection
        """
        if self.is_key_just_pressed(InputConfig.UPGRADE_KEY_1):
            return 0
        elif self.is_key_just_pressed(InputConfig.UPGRADE_KEY_2):
            return 1
        elif self.is_key_just_pressed(InputConfig.UPGRADE_KEY_3):
            return 2
        return None

    # ==================== EVENT PROCESSING ====================

    def process_event(self, event):
        """
        Process pygame events (for special cases not covered by polling)
        Call this in your event loop for each event

        Args:
            event: pygame.event.Event

        Returns:
            dict: Information about the event for game to handle
        """
        result = {"type": None, "handled": False}

        # This method is here for extensibility
        # Most input is handled by polling in update()
        # But some things (like text input) need event processing

        return result
