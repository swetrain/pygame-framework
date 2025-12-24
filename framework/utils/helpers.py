"""
Helper utilities module.

This module provides common utility functions and classes for game development.
"""

import math
from typing import Tuple
import pygame


# Color constants
class Colors:
    """Common color constants."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    BROWN = (165, 42, 42)
    PINK = (255, 192, 203)


# Distance and geometry functions
def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        x1: First point x coordinate
        y1: First point y coordinate
        x2: Second point x coordinate
        y2: Second point y coordinate
        
    Returns:
        Distance between the points
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate squared distance (faster, useful for comparisons).
    
    Args:
        x1: First point x coordinate
        y1: First point y coordinate
        x2: Second point x coordinate
        y2: Second point y coordinate
        
    Returns:
        Squared distance between the points
    """
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def angle_to(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate angle from point 1 to point 2 in radians.
    
    Args:
        x1: First point x coordinate
        y1: First point y coordinate
        x2: Second point x coordinate
        y2: Second point y coordinate
        
    Returns:
        Angle in radians
    """
    return math.atan2(y2 - y1, x2 - x1)


def angle_to_degrees(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate angle from point 1 to point 2 in degrees.
    
    Args:
        x1: First point x coordinate
        y1: First point y coordinate
        x2: Second point x coordinate
        y2: Second point y coordinate
        
    Returns:
        Angle in degrees
    """
    return math.degrees(angle_to(x1, y1, x2, y2))


def normalize_vector(x: float, y: float) -> Tuple[float, float]:
    """
    Normalize a vector to unit length.
    
    Args:
        x: Vector x component
        y: Vector y component
        
    Returns:
        Normalized vector (x, y)
    """
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values.
    
    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated value
    """
    return start + (end - start) * t


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def map_range(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float,
    out_max: float
) -> float:
    """
    Map a value from one range to another.
    
    Args:
        value: Input value
        in_min: Input range minimum
        in_max: Input range maximum
        out_min: Output range minimum
        out_max: Output range maximum
        
    Returns:
        Mapped value
    """
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)


class Timer:
    """
    Simple timer class for cooldowns and delayed actions.
    
    Attributes:
        duration: Timer duration in seconds
        time_left: Time remaining in seconds
        running: Whether timer is active
        loop: Whether to automatically restart
    """
    
    def __init__(self, duration: float, autostart: bool = False, loop: bool = False):
        """
        Initialize the timer.
        
        Args:
            duration: Timer duration in seconds
            autostart: Start timer immediately
            loop: Automatically restart when finished
        """
        self.duration = duration
        self.time_left = duration if autostart else 0
        self.running = autostart
        self.loop = loop
    
    def start(self) -> None:
        """Start or restart the timer."""
        self.time_left = self.duration
        self.running = True
    
    def stop(self) -> None:
        """Stop the timer."""
        self.running = False
        self.time_left = 0
    
    def pause(self) -> None:
        """Pause the timer."""
        self.running = False
    
    def resume(self) -> None:
        """Resume the timer."""
        if self.time_left > 0:
            self.running = True
    
    def update(self, dt: float) -> bool:
        """
        Update the timer.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if timer just finished this frame
        """
        if not self.running:
            return False
        
        self.time_left -= dt
        
        if self.time_left <= 0:
            if self.loop:
                self.time_left = self.duration
                return True
            else:
                self.running = False
                self.time_left = 0
                return True
        
        return False
    
    def is_finished(self) -> bool:
        """
        Check if timer has finished.
        
        Returns:
            True if timer is not running and time is 0
        """
        return not self.running and self.time_left == 0
    
    def is_running(self) -> bool:
        """
        Check if timer is running.
        
        Returns:
            True if timer is active
        """
        return self.running
    
    def get_progress(self) -> float:
        """
        Get timer progress (0-1).
        
        Returns:
            Progress value (0 = just started, 1 = finished)
        """
        if self.duration == 0:
            return 1.0
        return 1.0 - (self.time_left / self.duration)
    
    def get_time_left(self) -> float:
        """
        Get remaining time in seconds.
        
        Returns:
            Time left in seconds
        """
        return self.time_left


def point_in_rect(x: float, y: float, rect: pygame.Rect) -> bool:
    """
    Check if a point is inside a rectangle.
    
    Args:
        x: Point x coordinate
        y: Point y coordinate
        rect: Pygame Rect
        
    Returns:
        True if point is inside rectangle
    """
    return rect.collidepoint(x, y)


def rects_overlap(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Check if two rectangles overlap.
    
    Args:
        rect1: First rectangle
        rect2: Second rectangle
        
    Returns:
        True if rectangles overlap
    """
    return rect1.colliderect(rect2)


# Export all public functions and classes
__all__ = [
    'Colors',
    'distance',
    'distance_squared',
    'angle_to',
    'angle_to_degrees',
    'normalize_vector',
    'lerp',
    'clamp',
    'map_range',
    'Timer',
    'point_in_rect',
    'rects_overlap',
]
