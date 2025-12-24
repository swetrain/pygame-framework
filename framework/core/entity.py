"""
Entity system module.

This module provides the base Entity class for game objects with
component-based architecture.
"""

from typing import Dict, List, Optional, Tuple, Any
import pygame


class Entity:
    """
    Base class for all game entities/objects.
    
    An entity represents any game object (player, enemy, item, etc.)
    and supports a component-based architecture for flexible behavior.
    
    Attributes:
        position: (x, y) position in world space
        size: (width, height) dimensions
        active: Whether the entity should update and render
        components: Dictionary of attached components
        tags: Set of string tags for identification
    """
    
    def __init__(
        self,
        position: Tuple[float, float] = (0, 0),
        size: Tuple[float, float] = (32, 32)
    ):
        """
        Initialize the entity.
        
        Args:
            position: Initial (x, y) position
            size: Initial (width, height) dimensions
        """
        self.position = list(position)  # [x, y]
        self.size = list(size)  # [width, height]
        self.active = True
        self.components: Dict[str, Any] = {}
        self.tags: set = set()
    
    def add_component(self, name: str, component: Any) -> None:
        """
        Add a component to this entity.
        
        Args:
            name: Unique identifier for the component
            component: Component instance to attach
        """
        self.components[name] = component
        
        # Set entity reference on component if it has the attribute
        if hasattr(component, 'entity'):
            component.entity = self
    
    def get_component(self, name: str) -> Optional[Any]:
        """
        Retrieve a component by name.
        
        Args:
            name: Component identifier
            
        Returns:
            Component instance or None if not found
        """
        return self.components.get(name)
    
    def remove_component(self, name: str) -> None:
        """
        Remove a component from this entity.
        
        Args:
            name: Component identifier to remove
        """
        if name in self.components:
            del self.components[name]
    
    def has_component(self, name: str) -> bool:
        """
        Check if entity has a specific component.
        
        Args:
            name: Component identifier
            
        Returns:
            True if component exists, False otherwise
        """
        return name in self.components
    
    def add_tag(self, tag: str) -> None:
        """
        Add a tag to this entity for identification.
        
        Args:
            tag: Tag string to add
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from this entity.
        
        Args:
            tag: Tag string to remove
        """
        self.tags.discard(tag)
    
    def has_tag(self, tag: str) -> bool:
        """
        Check if entity has a specific tag.
        
        Args:
            tag: Tag string to check
            
        Returns:
            True if entity has the tag, False otherwise
        """
        return tag in self.tags
    
    def update(self, dt: float) -> None:
        """
        Update entity logic and all components.
        
        Args:
            dt: Delta time in seconds since last frame
        """
        if not self.active:
            return
        
        # Update all components that have an update method
        for component in self.components.values():
            if hasattr(component, 'update'):
                component.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render entity and all components.
        
        Args:
            screen: Pygame surface to render to
        """
        if not self.active:
            return
        
        # Render all components that have a render method
        for component in self.components.values():
            if hasattr(component, 'render'):
                component.render(screen)
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the bounding rectangle for this entity.
        
        Returns:
            Pygame Rect representing entity bounds
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1]
        )
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set entity position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.position[0] = x
        self.position[1] = y
    
    def get_position(self) -> Tuple[float, float]:
        """
        Get entity position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return tuple(self.position)
    
    def set_size(self, width: float, height: float) -> None:
        """
        Set entity size.
        
        Args:
            width: Entity width
            height: Entity height
        """
        self.size[0] = width
        self.size[1] = height
    
    def get_size(self) -> Tuple[float, float]:
        """
        Get entity size.
        
        Returns:
            Tuple of (width, height)
        """
        return tuple(self.size)
    
    def set_active(self, active: bool) -> None:
        """
        Set entity active state.
        
        Args:
            active: True to activate, False to deactivate
        """
        self.active = active
    
    def is_active(self) -> bool:
        """
        Check if entity is active.
        
        Returns:
            True if active, False otherwise
        """
        return self.active
