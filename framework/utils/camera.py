"""
Camera/viewport system module.

This module provides camera functionality for scrolling, following entities,
and screen shake effects.
"""

from typing import Optional, Tuple
import pygame
import random
import math


class Camera:
    """
    Camera/viewport system for 2D games.
    
    Supports:
    - Camera position and movement
    - Following entities (follow camera)
    - Zoom in/out
    - Screen shake effects
    - Bounds limiting
    
    Attributes:
        position: Camera position in world space [x, y]
        viewport_size: Size of the viewport (width, height)
        zoom: Zoom level (1.0 = normal)
        shake_intensity: Current shake intensity
        shake_duration: Remaining shake duration
    """
    
    def __init__(
        self,
        viewport_size: Tuple[int, int],
        world_size: Optional[Tuple[int, int]] = None
    ):
        """
        Initialize the camera.
        
        Args:
            viewport_size: Size of the visible viewport (width, height)
            world_size: Optional world bounds (width, height)
        """
        self.position = [0.0, 0.0]
        self.viewport_size = viewport_size
        self.world_size = world_size
        self.zoom = 1.0
        
        # Follow target
        self.follow_target: Optional['Entity'] = None
        self.follow_speed = 1.0
        self.follow_offset = [0, 0]
        
        # Screen shake
        self.shake_intensity = 0.0
        self.shake_duration = 0.0
        self.shake_offset = [0, 0]
    
    def update(self, dt: float) -> None:
        """
        Update camera state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update follow target
        if self.follow_target:
            target_x = self.follow_target.position[0] + self.follow_offset[0] - self.viewport_size[0] / 2
            target_y = self.follow_target.position[1] + self.follow_offset[1] - self.viewport_size[1] / 2
            
            # Smooth following
            self.position[0] += (target_x - self.position[0]) * self.follow_speed * dt * 10
            self.position[1] += (target_y - self.position[1]) * self.follow_speed * dt * 10
        
        # Update screen shake
        if self.shake_duration > 0:
            self.shake_duration -= dt
            angle = random.uniform(0, 2 * math.pi)
            self.shake_offset[0] = math.cos(angle) * self.shake_intensity
            self.shake_offset[1] = math.sin(angle) * self.shake_intensity
        else:
            self.shake_offset = [0, 0]
        
        # Apply world bounds
        if self.world_size:
            self.position[0] = max(0, min(self.position[0], self.world_size[0] - self.viewport_size[0]))
            self.position[1] = max(0, min(self.position[1], self.world_size[1] - self.viewport_size[1]))
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set camera position in world space.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.position[0] = x
        self.position[1] = y
    
    def move(self, dx: float, dy: float) -> None:
        """
        Move camera by a delta.
        
        Args:
            dx: Change in x
            dy: Change in y
        """
        self.position[0] += dx
        self.position[1] += dy
    
    def follow(
        self,
        entity: 'Entity',
        speed: float = 1.0,
        offset: Tuple[float, float] = (0, 0)
    ) -> None:
        """
        Make camera follow an entity.
        
        Args:
            entity: Entity to follow
            speed: Follow speed (0-1, 1 = instant)
            offset: Offset from entity position
        """
        self.follow_target = entity
        self.follow_speed = speed
        self.follow_offset = list(offset)
    
    def unfollow(self) -> None:
        """Stop following the current target."""
        self.follow_target = None
    
    def shake(self, intensity: float, duration: float) -> None:
        """
        Apply screen shake effect.
        
        Args:
            intensity: Shake intensity in pixels
            duration: Shake duration in seconds
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def set_zoom(self, zoom: float) -> None:
        """
        Set camera zoom level.
        
        Args:
            zoom: Zoom level (1.0 = normal, >1 = zoomed in, <1 = zoomed out)
        """
        self.zoom = max(0.1, zoom)
    
    def get_zoom(self) -> float:
        """
        Get current zoom level.
        
        Returns:
            Current zoom level
        """
        return self.zoom
    
    def world_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert world coordinates to screen coordinates.
        
        Args:
            x: World x coordinate
            y: World y coordinate
            
        Returns:
            Tuple of (screen_x, screen_y)
        """
        screen_x = (x - self.position[0]) * self.zoom + self.shake_offset[0]
        screen_y = (y - self.position[1]) * self.zoom + self.shake_offset[1]
        return (screen_x, screen_y)
    
    def screen_to_world(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.
        
        Args:
            x: Screen x coordinate
            y: Screen y coordinate
            
        Returns:
            Tuple of (world_x, world_y)
        """
        world_x = (x - self.shake_offset[0]) / self.zoom + self.position[0]
        world_y = (y - self.shake_offset[1]) / self.zoom + self.position[1]
        return (world_x, world_y)
    
    def apply(self, entity_pos: Tuple[float, float]) -> Tuple[float, float]:
        """
        Apply camera transformation to a position.
        
        Args:
            entity_pos: Position in world space (x, y)
            
        Returns:
            Position in screen space (x, y)
        """
        return self.world_to_screen(entity_pos[0], entity_pos[1])
    
    def get_rect(self) -> pygame.Rect:
        """
        Get camera viewport rectangle in world space.
        
        Returns:
            Pygame Rect representing visible area
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.viewport_size[0] / self.zoom,
            self.viewport_size[1] / self.zoom
        )
    
    def is_visible(self, rect: pygame.Rect) -> bool:
        """
        Check if a rectangle is visible in the camera view.
        
        Args:
            rect: Rectangle in world space
            
        Returns:
            True if rectangle intersects camera viewport
        """
        camera_rect = self.get_rect()
        return camera_rect.colliderect(rect)
