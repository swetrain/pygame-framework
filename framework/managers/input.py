"""
Input management module.

This module provides centralized input handling for keyboard and mouse
with state tracking and input mapping support.
"""

from typing import Dict, Set, Tuple, Optional
import pygame


class InputManager:
    """
    Manager for keyboard and mouse input handling.
    
    This manager tracks:
    - Key states (pressed, held, released)
    - Mouse position and button states
    - Input action mapping (e.g., "jump" -> SPACE key)
    
    Attributes:
        keys_pressed: Set of keys pressed this frame
        keys_held: Set of keys currently held down
        keys_released: Set of keys released this frame
        mouse_pos: Current mouse position (x, y)
        mouse_buttons: Dictionary of mouse button states
        action_map: Dictionary mapping action names to keys
    """
    
    def __init__(self):
        """Initialize the input manager."""
        self.keys_pressed: Set[int] = set()
        self.keys_held: Set[int] = set()
        self.keys_released: Set[int] = set()
        
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_buttons: Dict[int, bool] = {}
        self.mouse_pressed: Set[int] = set()
        self.mouse_released: Set[int] = set()
        
        self.action_map: Dict[str, int] = {}
    
    def update(self, events: list) -> None:
        """
        Update input states based on pygame events.
        
        Should be called once per frame with the event list.
        
        Args:
            events: List of pygame events from pygame.event.get()
        """
        # Clear frame-specific states
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_pressed.clear()
        self.mouse_released.clear()
        
        # Process events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_held.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_released.add(event.key)
                self.keys_held.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed.add(event.button)
                self.mouse_buttons[event.button] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_released.add(event.button)
                self.mouse_buttons[event.button] = False
        
        # Update mouse position
        self.mouse_pos = pygame.mouse.get_pos()
    
    def is_key_pressed(self, key: int) -> bool:
        """
        Check if a key was just pressed this frame.
        
        Args:
            key: Pygame key constant (e.g., pygame.K_SPACE)
            
        Returns:
            True if key was pressed this frame
        """
        return key in self.keys_pressed
    
    def is_key_held(self, key: int) -> bool:
        """
        Check if a key is currently held down.
        
        Args:
            key: Pygame key constant
            
        Returns:
            True if key is currently held
        """
        return key in self.keys_held
    
    def is_key_released(self, key: int) -> bool:
        """
        Check if a key was just released this frame.
        
        Args:
            key: Pygame key constant
            
        Returns:
            True if key was released this frame
        """
        return key in self.keys_released
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """
        Check if a mouse button was just pressed this frame.
        
        Args:
            button: Mouse button number (1=left, 2=middle, 3=right)
            
        Returns:
            True if button was pressed this frame
        """
        return button in self.mouse_pressed
    
    def is_mouse_button_held(self, button: int) -> bool:
        """
        Check if a mouse button is currently held down.
        
        Args:
            button: Mouse button number
            
        Returns:
            True if button is currently held
        """
        return self.mouse_buttons.get(button, False)
    
    def is_mouse_button_released(self, button: int) -> bool:
        """
        Check if a mouse button was just released this frame.
        
        Args:
            button: Mouse button number
            
        Returns:
            True if button was released this frame
        """
        return button in self.mouse_released
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """
        Get current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return self.mouse_pos
    
    def map_action(self, action_name: str, key: int) -> None:
        """
        Map an action name to a key.
        
        This allows using semantic action names instead of key codes.
        
        Args:
            action_name: Name of the action (e.g., "jump", "fire")
            key: Pygame key constant to map to this action
        """
        self.action_map[action_name] = key
    
    def is_action_pressed(self, action_name: str) -> bool:
        """
        Check if a mapped action was pressed this frame.
        
        Args:
            action_name: Name of the action
            
        Returns:
            True if the action's key was pressed this frame
        """
        key = self.action_map.get(action_name)
        if key is None:
            return False
        return self.is_key_pressed(key)
    
    def is_action_held(self, action_name: str) -> bool:
        """
        Check if a mapped action is currently held.
        
        Args:
            action_name: Name of the action
            
        Returns:
            True if the action's key is currently held
        """
        key = self.action_map.get(action_name)
        if key is None:
            return False
        return self.is_key_held(key)
    
    def is_action_released(self, action_name: str) -> bool:
        """
        Check if a mapped action was released this frame.
        
        Args:
            action_name: Name of the action
            
        Returns:
            True if the action's key was released this frame
        """
        key = self.action_map.get(action_name)
        if key is None:
            return False
        return self.is_key_released(key)
    
    def clear_action_map(self) -> None:
        """Clear all action mappings."""
        self.action_map.clear()
    
    def get_axis(self, negative_key: int, positive_key: int) -> float:
        """
        Get axis value from two keys (e.g., for movement).
        
        Args:
            negative_key: Key for negative direction (-1)
            positive_key: Key for positive direction (+1)
            
        Returns:
            Value between -1 and 1
        """
        value = 0.0
        if self.is_key_held(negative_key):
            value -= 1.0
        if self.is_key_held(positive_key):
            value += 1.0
        return value
