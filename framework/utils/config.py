"""
Configuration management module.

This module provides JSON-based configuration loading and saving.
"""

from typing import Any, Dict, Optional
import json
import os


class Config:
    """
    Configuration manager for game settings.
    
    Handles loading and saving configuration from/to JSON files
    with default values support.
    
    Attributes:
        config_path: Path to configuration file
        data: Dictionary of configuration values
        defaults: Dictionary of default values
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.data: Dict[str, Any] = {}
        self.defaults: Dict[str, Any] = self._get_defaults()
        
        # Load configuration
        self.load()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """
        Get default configuration values.
        
        Returns:
            Dictionary of default configuration
        """
        return {
            # Display settings
            "screen_width": 800,
            "screen_height": 600,
            "fullscreen": False,
            "fps": 60,
            
            # Audio settings
            "music_volume": 1.0,
            "sound_volume": 1.0,
            "mute_music": False,
            "mute_sound": False,
            
            # Game settings
            "difficulty": "normal",
            "language": "en",
            
            # Controls (can be customized)
            "controls": {
                "up": "w",
                "down": "s",
                "left": "a",
                "right": "d",
                "jump": "space",
                "action": "e"
            }
        }
    
    def load(self) -> None:
        """
        Load configuration from file.
        
        If file doesn't exist, uses default values.
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.data = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in self.defaults.items():
                    if key not in self.data:
                        self.data[key] = value
            except json.JSONDecodeError as e:
                print(f"Error loading config: {e}")
                self.data = self.defaults.copy()
        else:
            # Use defaults if file doesn't exist
            self.data = self.defaults.copy()
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.data[key] = value
    
    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """
        Get a nested configuration value.
        
        Example: config.get_nested("controls", "jump")
        
        Args:
            keys: Sequence of keys to traverse
            default: Default value if path doesn't exist
            
        Returns:
            Configuration value or default
        """
        value = self.data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set_nested(self, *keys: str, value: Any) -> None:
        """
        Set a nested configuration value.
        
        Example: config.set_nested("controls", "jump", "space")
        
        Args:
            keys: Sequence of keys to traverse (last key is set)
            value: Value to set
        """
        if len(keys) < 2:
            if keys:
                self.data[keys[0]] = value
            return
        
        # Navigate to parent
        current = self.data
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        # Set final value
        current[keys[-1]] = value
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to default values."""
        self.data = self.defaults.copy()
    
    def reset_key(self, key: str) -> None:
        """
        Reset a specific key to its default value.
        
        Args:
            key: Configuration key to reset
        """
        if key in self.defaults:
            self.data[key] = self.defaults[key]
    
    def has_key(self, key: str) -> bool:
        """
        Check if configuration has a key.
        
        Args:
            key: Configuration key
            
        Returns:
            True if key exists
        """
        return key in self.data
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration data.
        
        Returns:
            Dictionary of all configuration
        """
        return self.data.copy()
    
    def update(self, new_data: Dict[str, Any]) -> None:
        """
        Update configuration with new values.
        
        Args:
            new_data: Dictionary of values to update
        """
        self.data.update(new_data)
