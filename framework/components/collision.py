"""
Collision detection module.

This module provides AABB collision detection with callback support.
"""

from typing import Optional, Callable, List, Set
import pygame


class CollisionComponent:
    """
    Component for AABB (Axis-Aligned Bounding Box) collision detection.
    
    Supports:
    - Rectangle-based collision detection
    - Collision callbacks
    - Collision layers/tags for filtering
    - Offset from entity position
    
    Attributes:
        entity: Reference to parent entity
        offset: Offset from entity position [x, y]
        size: Collision box size [width, height] (None = use entity size)
        on_collision: Callback function for collision events
        layer: Collision layer for filtering
        collision_tags: Set of tags this collider can collide with
    """
    
    def __init__(
        self,
        offset: tuple = (0, 0),
        size: Optional[tuple] = None,
        on_collision: Optional[Callable] = None,
        layer: str = "default",
        collision_tags: Optional[Set[str]] = None
    ):
        """
        Initialize the collision component.
        
        Args:
            offset: Offset from entity position (x, y)
            size: Collision box size (width, height), None to use entity size
            on_collision: Callback function(other_entity) called on collision
            layer: Collision layer name
            collision_tags: Set of tags this collider interacts with
        """
        self.entity: Optional['Entity'] = None
        self.offset = list(offset)
        self.size = list(size) if size else None
        self.on_collision = on_collision
        self.layer = layer
        self.collision_tags = collision_tags or set()
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the collision rectangle in world space.
        
        Returns:
            Pygame Rect for collision detection
        """
        if not self.entity:
            return pygame.Rect(0, 0, 0, 0)
        
        # Use custom size or entity size
        width, height = self.size if self.size else self.entity.size
        
        # Apply offset
        x = self.entity.position[0] + self.offset[0]
        y = self.entity.position[1] + self.offset[1]
        
        return pygame.Rect(x, y, width, height)
    
    def check_collision(self, other: 'CollisionComponent') -> bool:
        """
        Check if this collider intersects with another.
        
        Args:
            other: Other CollisionComponent to check against
            
        Returns:
            True if colliding
        """
        # Check layer/tag filtering
        if self.collision_tags and other.layer not in self.collision_tags:
            return False
        
        # Check rectangle intersection
        rect1 = self.get_rect()
        rect2 = other.get_rect()
        return rect1.colliderect(rect2)
    
    def check_collision_with_rect(self, rect: pygame.Rect) -> bool:
        """
        Check collision with a rectangle.
        
        Args:
            rect: Pygame Rect to check against
            
        Returns:
            True if colliding
        """
        return self.get_rect().colliderect(rect)
    
    def check_collision_with_point(self, x: float, y: float) -> bool:
        """
        Check if a point is inside the collision box.
        
        Args:
            x: Point x coordinate
            y: Point y coordinate
            
        Returns:
            True if point is inside
        """
        return self.get_rect().collidepoint(x, y)
    
    def handle_collision(self, other_entity: 'Entity') -> None:
        """
        Handle collision with another entity.
        
        Calls the on_collision callback if set.
        
        Args:
            other_entity: The entity we collided with
        """
        if self.on_collision:
            self.on_collision(other_entity)
    
    def set_offset(self, x: float, y: float) -> None:
        """
        Set collision box offset.
        
        Args:
            x: X offset
            y: Y offset
        """
        self.offset[0] = x
        self.offset[1] = y
    
    def set_size(self, width: float, height: float) -> None:
        """
        Set collision box size.
        
        Args:
            width: Box width
            height: Box height
        """
        self.size = [width, height]
    
    def add_collision_tag(self, tag: str) -> None:
        """
        Add a tag that this collider can collide with.
        
        Args:
            tag: Tag to add
        """
        self.collision_tags.add(tag)
    
    def remove_collision_tag(self, tag: str) -> None:
        """
        Remove a collision tag.
        
        Args:
            tag: Tag to remove
        """
        self.collision_tags.discard(tag)
    
    def debug_render(self, screen: pygame.Surface, color: tuple = (255, 0, 0)) -> None:
        """
        Render collision box for debugging.
        
        Args:
            screen: Pygame surface to render to
            color: Color to draw the collision box
        """
        rect = self.get_rect()
        pygame.draw.rect(screen, color, rect, 2)


class CollisionSystem:
    """
    System for managing and checking collisions between entities.
    
    Maintains a list of entities with collision components and
    performs collision detection.
    """
    
    def __init__(self):
        """Initialize the collision system."""
        self.entities: List['Entity'] = []
    
    def add_entity(self, entity: 'Entity') -> None:
        """
        Add an entity to collision checking.
        
        Args:
            entity: Entity with CollisionComponent to track
        """
        if entity not in self.entities:
            self.entities.append(entity)
    
    def remove_entity(self, entity: 'Entity') -> None:
        """
        Remove an entity from collision checking.
        
        Args:
            entity: Entity to stop tracking
        """
        if entity in self.entities:
            self.entities.remove(entity)
    
    def check_collisions(self) -> None:
        """Check collisions between all registered entities."""
        # Simple O(n²) collision detection
        # For better performance with many entities, use spatial partitioning
        for i, entity1 in enumerate(self.entities):
            if not entity1.active:
                continue
            
            collision1 = entity1.get_component('collision')
            if not collision1:
                continue
            
            for entity2 in self.entities[i + 1:]:
                if not entity2.active:
                    continue
                
                collision2 = entity2.get_component('collision')
                if not collision2:
                    continue
                
                if collision1.check_collision(collision2):
                    collision1.handle_collision(entity2)
                    collision2.handle_collision(entity1)
    
    def clear(self) -> None:
        """Remove all entities from the system."""
        self.entities.clear()
