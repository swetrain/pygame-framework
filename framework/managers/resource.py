"""
Resource management module.

This module provides a singleton ResourceManager for loading and caching
game resources like images, sounds, and fonts.
"""

from typing import Dict, Optional, Tuple
import pygame
import os


class ResourceManager:
    """
    Singleton resource manager for loading and caching game assets.
    
    This manager handles:
    - Image loading and caching
    - Sound loading and caching
    - Font loading and caching
    - Automatic resource cleanup
    
    The singleton pattern ensures only one instance exists,
    preventing duplicate resource loading.
    """
    
    _instance: Optional['ResourceManager'] = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the resource manager (only once)."""
        if self._initialized:
            return
        
        self._initialized = True
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        self.base_path: str = ""
    
    def set_base_path(self, path: str) -> None:
        """
        Set the base path for resource loading.
        
        Args:
            path: Base directory path for resources
        """
        self.base_path = path
    
    def load_image(
        self,
        path: str,
        convert_alpha: bool = True,
        scale: Optional[Tuple[int, int]] = None
    ) -> pygame.Surface:
        """
        Load an image from file with caching.
        
        Args:
            path: Path to image file (relative to base_path)
            convert_alpha: Whether to convert image for alpha transparency
            scale: Optional (width, height) to scale the image
            
        Returns:
            Pygame Surface containing the image
            
        Raises:
            FileNotFoundError: If image file doesn't exist
        """
        cache_key = f"{path}_{scale}"
        
        if cache_key in self.images:
            return self.images[cache_key]
        
        full_path = os.path.join(self.base_path, path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Image not found: {full_path}")
        
        image = pygame.image.load(full_path)
        
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        
        if scale:
            image = pygame.transform.scale(image, scale)
        
        self.images[cache_key] = image
        return image
    
    def create_surface(
        self,
        size: Tuple[int, int],
        color: Tuple[int, int, int],
        alpha: bool = True
    ) -> pygame.Surface:
        """
        Create a colored surface (useful for placeholder graphics).
        
        Args:
            size: (width, height) of the surface
            color: RGB color tuple
            alpha: Whether to enable alpha channel
            
        Returns:
            Pygame Surface filled with the specified color
        """
        if alpha:
            surface = pygame.Surface(size, pygame.SRCALPHA)
        else:
            surface = pygame.Surface(size)
        surface.fill(color)
        return surface
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """
        Load a sound from file with caching.
        
        Args:
            path: Path to sound file (relative to base_path)
            
        Returns:
            Pygame Sound object
            
        Raises:
            FileNotFoundError: If sound file doesn't exist
        """
        if path in self.sounds:
            return self.sounds[path]
        
        full_path = os.path.join(self.base_path, path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Sound not found: {full_path}")
        
        sound = pygame.mixer.Sound(full_path)
        self.sounds[path] = sound
        return sound
    
    def load_font(
        self,
        path: Optional[str] = None,
        size: int = 24
    ) -> pygame.font.Font:
        """
        Load a font with caching.
        
        Args:
            path: Path to font file (None for default font)
            size: Font size in points
            
        Returns:
            Pygame Font object
            
        Raises:
            FileNotFoundError: If font file doesn't exist
        """
        cache_key = (path or "", size)
        
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        if path:
            full_path = os.path.join(self.base_path, path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Font not found: {full_path}")
            font = pygame.font.Font(full_path, size)
        else:
            font = pygame.font.Font(None, size)
        
        self.fonts[cache_key] = font
        return font
    
    def clear_images(self) -> None:
        """Clear all cached images."""
        self.images.clear()
    
    def clear_sounds(self) -> None:
        """Clear all cached sounds."""
        self.sounds.clear()
    
    def clear_fonts(self) -> None:
        """Clear all cached fonts."""
        self.fonts.clear()
    
    def clear_all(self) -> None:
        """Clear all cached resources."""
        self.clear_images()
        self.clear_sounds()
        self.clear_fonts()
    
    def get_cached_image(self, path: str) -> Optional[pygame.Surface]:
        """
        Get a cached image without loading.
        
        Args:
            path: Path to image file
            
        Returns:
            Cached image or None if not in cache
        """
        return self.images.get(path)
    
    def get_cached_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Get a cached sound without loading.
        
        Args:
            path: Path to sound file
            
        Returns:
            Cached sound or None if not in cache
        """
        return self.sounds.get(path)
