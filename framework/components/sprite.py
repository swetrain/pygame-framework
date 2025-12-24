"""
Sprite component module.

This module provides a sprite rendering component with transform support.
"""

from typing import Optional, Tuple
import pygame


class Sprite:
    """
    Component for rendering images/sprites.
    
    Supports:
    - Image rendering
    - Scaling and rotation
    - Flipping (horizontal/vertical)
    - Alpha transparency
    
    Attributes:
        entity: Reference to parent entity
        image: Original image surface
        transformed_image: Cached transformed image
        scale: Scale multiplier (1.0 = original size)
        rotation: Rotation angle in degrees
        flip_x: Whether to flip horizontally
        flip_y: Whether to flip vertically
        alpha: Alpha transparency (0-255)
    """
    
    def __init__(
        self,
        image: pygame.Surface,
        scale: float = 1.0,
        rotation: float = 0.0,
        flip_x: bool = False,
        flip_y: bool = False,
        alpha: int = 255
    ):
        """
        Initialize the sprite component.
        
        Args:
            image: Pygame Surface to render
            scale: Scale multiplier
            rotation: Initial rotation in degrees
            flip_x: Flip horizontally
            flip_y: Flip vertically
            alpha: Alpha transparency (0-255)
        """
        self.entity: Optional['Entity'] = None
        self.image = image
        self.original_image = image
        self.transformed_image = image
        self._scale = scale
        self._rotation = rotation
        self._flip_x = flip_x
        self._flip_y = flip_y
        self._alpha = alpha
        self._needs_update = True
        
        self._update_transform()
    
    def _update_transform(self) -> None:
        """Update the transformed image based on current properties."""
        if not self._needs_update:
            return
        
        image = self.original_image
        
        # Apply flip
        if self._flip_x or self._flip_y:
            image = pygame.transform.flip(image, self._flip_x, self._flip_y)
        
        # Apply scale
        if self._scale != 1.0:
            new_size = (
                int(image.get_width() * self._scale),
                int(image.get_height() * self._scale)
            )
            image = pygame.transform.scale(image, new_size)
        
        # Apply rotation
        if self._rotation != 0:
            image = pygame.transform.rotate(image, self._rotation)
        
        # Apply alpha
        if self._alpha != 255:
            image.set_alpha(self._alpha)
        
        self.transformed_image = image
        self._needs_update = False
    
    @property
    def scale(self) -> float:
        """Get scale multiplier."""
        return self._scale
    
    @scale.setter
    def scale(self, value: float) -> None:
        """Set scale multiplier."""
        if self._scale != value:
            self._scale = value
            self._needs_update = True
    
    @property
    def rotation(self) -> float:
        """Get rotation in degrees."""
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float) -> None:
        """Set rotation in degrees."""
        if self._rotation != value:
            self._rotation = value % 360
            self._needs_update = True
    
    @property
    def flip_x(self) -> bool:
        """Get horizontal flip state."""
        return self._flip_x
    
    @flip_x.setter
    def flip_x(self, value: bool) -> None:
        """Set horizontal flip state."""
        if self._flip_x != value:
            self._flip_x = value
            self._needs_update = True
    
    @property
    def flip_y(self) -> bool:
        """Get vertical flip state."""
        return self._flip_y
    
    @flip_y.setter
    def flip_y(self, value: bool) -> None:
        """Set vertical flip state."""
        if self._flip_y != value:
            self._flip_y = value
            self._needs_update = True
    
    @property
    def alpha(self) -> int:
        """Get alpha transparency."""
        return self._alpha
    
    @alpha.setter
    def alpha(self, value: int) -> None:
        """Set alpha transparency (0-255)."""
        value = max(0, min(255, value))
        if self._alpha != value:
            self._alpha = value
            self._needs_update = True
    
    def set_image(self, image: pygame.Surface) -> None:
        """
        Change the sprite image.
        
        Args:
            image: New pygame Surface
        """
        self.original_image = image
        self.image = image
        self._needs_update = True
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the sprite.
        
        Args:
            screen: Pygame surface to render to
        """
        if not self.entity:
            return
        
        self._update_transform()
        
        # Calculate position to center the sprite on entity position
        rect = self.transformed_image.get_rect()
        rect.center = (
            self.entity.position[0] + self.entity.size[0] / 2,
            self.entity.position[1] + self.entity.size[1] / 2
        )
        
        screen.blit(self.transformed_image, rect)
    
    def get_size(self) -> Tuple[int, int]:
        """
        Get the current size of the transformed sprite.
        
        Returns:
            Tuple of (width, height)
        """
        self._update_transform()
        return self.transformed_image.get_size()
