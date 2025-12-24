"""
Physics component module.

This module provides physics simulation for entities including velocity,
acceleration, and gravity.
"""

from typing import Optional, Tuple
import pygame


class PhysicsComponent:
    """
    Component for physics simulation.
    
    Handles:
    - Velocity and acceleration
    - Gravity simulation
    - Maximum speed limiting
    - Drag/friction
    
    Attributes:
        entity: Reference to parent entity
        velocity: Current velocity [x, y]
        acceleration: Current acceleration [x, y]
        gravity: Gravity force (positive = downward)
        max_velocity: Maximum velocity limits [x, y]
        drag: Drag coefficient (0-1, 1 = no drag)
        use_gravity: Whether to apply gravity
    """
    
    def __init__(
        self,
        velocity: Tuple[float, float] = (0, 0),
        acceleration: Tuple[float, float] = (0, 0),
        gravity: float = 0,
        max_velocity: Tuple[float, float] = (1000, 1000),
        drag: float = 1.0,
        use_gravity: bool = True
    ):
        """
        Initialize the physics component.
        
        Args:
            velocity: Initial velocity (x, y)
            acceleration: Constant acceleration (x, y)
            gravity: Gravity acceleration (positive = down)
            max_velocity: Maximum velocity limits (x, y)
            drag: Drag coefficient (0-1, 1 = no drag)
            use_gravity: Whether to apply gravity
        """
        self.entity: Optional['Entity'] = None
        self.velocity = list(velocity)
        self.acceleration = list(acceleration)
        self.gravity = gravity
        self.max_velocity = list(max_velocity)
        self.drag = drag
        self.use_gravity = use_gravity
    
    def apply_force(self, force_x: float, force_y: float) -> None:
        """
        Apply an instantaneous force to the velocity.
        
        Args:
            force_x: Force in x direction
            force_y: Force in y direction
        """
        self.velocity[0] += force_x
        self.velocity[1] += force_y
    
    def set_velocity(self, vx: float, vy: float) -> None:
        """
        Set velocity directly.
        
        Args:
            vx: X velocity
            vy: Y velocity
        """
        self.velocity[0] = vx
        self.velocity[1] = vy
    
    def get_velocity(self) -> Tuple[float, float]:
        """
        Get current velocity.
        
        Returns:
            Tuple of (vx, vy)
        """
        return tuple(self.velocity)
    
    def set_acceleration(self, ax: float, ay: float) -> None:
        """
        Set acceleration.
        
        Args:
            ax: X acceleration
            ay: Y acceleration
        """
        self.acceleration[0] = ax
        self.acceleration[1] = ay
    
    def get_acceleration(self) -> Tuple[float, float]:
        """
        Get current acceleration.
        
        Returns:
            Tuple of (ax, ay)
        """
        return tuple(self.acceleration)
    
    def update(self, dt: float) -> None:
        """
        Update physics simulation.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.entity:
            return
        
        # Apply acceleration
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        
        # Apply gravity
        if self.use_gravity:
            self.velocity[1] += self.gravity * dt
        
        # Apply drag
        if self.drag < 1.0:
            self.velocity[0] *= self.drag
            self.velocity[1] *= self.drag
        
        # Clamp to max velocity
        if abs(self.velocity[0]) > self.max_velocity[0]:
            self.velocity[0] = self.max_velocity[0] if self.velocity[0] > 0 else -self.max_velocity[0]
        if abs(self.velocity[1]) > self.max_velocity[1]:
            self.velocity[1] = self.max_velocity[1] if self.velocity[1] > 0 else -self.max_velocity[1]
        
        # Update entity position
        self.entity.position[0] += self.velocity[0] * dt
        self.entity.position[1] += self.velocity[1] * dt
    
    def stop(self) -> None:
        """Stop all movement (set velocity to zero)."""
        self.velocity = [0, 0]
    
    def is_moving(self) -> bool:
        """
        Check if entity is moving.
        
        Returns:
            True if velocity is non-zero
        """
        return self.velocity[0] != 0 or self.velocity[1] != 0
    
    def set_gravity(self, gravity: float) -> None:
        """
        Set gravity force.
        
        Args:
            gravity: Gravity acceleration (positive = down)
        """
        self.gravity = gravity
    
    def enable_gravity(self, enabled: bool = True) -> None:
        """
        Enable or disable gravity.
        
        Args:
            enabled: True to enable gravity
        """
        self.use_gravity = enabled
    
    def set_max_velocity(self, max_x: float, max_y: float) -> None:
        """
        Set maximum velocity limits.
        
        Args:
            max_x: Maximum horizontal velocity
            max_y: Maximum vertical velocity
        """
        self.max_velocity[0] = max_x
        self.max_velocity[1] = max_y
    
    def set_drag(self, drag: float) -> None:
        """
        Set drag coefficient.
        
        Args:
            drag: Drag value (0-1, 1 = no drag)
        """
        self.drag = max(0.0, min(1.0, drag))
