"""
Button UI component module.

This module provides interactive button widgets with text and image support.
"""

from typing import Optional, Callable, Tuple
import pygame


class Button:
    """
    Interactive button widget.
    
    Supports:
    - Text or image buttons
    - Hover and click states
    - Callback functions
    - Customizable colors and styling
    
    Attributes:
        position: Button position (x, y)
        size: Button size (width, height)
        text: Button text
        callback: Function to call on click
        enabled: Whether button is interactive
        hovered: Whether mouse is over button
        pressed: Whether button is currently pressed
    """
    
    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[float, float],
        text: str = "",
        callback: Optional[Callable] = None,
        font_size: int = 24,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        press_color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 0,
        image: Optional[pygame.Surface] = None
    ):
        """
        Initialize the button.
        
        Args:
            position: Button position (x, y)
            size: Button size (width, height)
            text: Button text
            callback: Function to call when clicked
            font_size: Font size for text
            text_color: Color of button text
            bg_color: Normal background color
            hover_color: Background color when hovered
            press_color: Background color when pressed
            border_color: Border color (None for no border)
            border_width: Border width in pixels
            image: Optional image to display instead of text
        """
        self.position = list(position)
        self.size = list(size)
        self.text = text
        self.callback = callback
        
        # Visual properties
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.press_color = press_color
        self.border_color = border_color
        self.border_width = border_width
        self.image = image
        
        # State
        self.enabled = True
        self.hovered = False
        self.pressed = False
        
        # Create font if using text
        if text and not image:
            self.font = pygame.font.Font(None, font_size)
            self.text_surface = self.font.render(text, True, text_color)
        else:
            self.font = None
            self.text_surface = None
    
    def get_rect(self) -> pygame.Rect:
        """
        Get button bounding rectangle.
        
        Returns:
            Pygame Rect for the button
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1]
        )
    
    def update(self, events: list) -> None:
        """
        Update button state based on events.
        
        Args:
            events: List of pygame events
        """
        if not self.enabled:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        rect = self.get_rect()
        
        # Check hover state
        self.hovered = rect.collidepoint(mouse_pos)
        
        # Check for clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.pressed and self.hovered:
                    # Button was clicked
                    if self.callback:
                        self.callback()
                self.pressed = False
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the button.
        
        Args:
            screen: Pygame surface to render to
        """
        rect = self.get_rect()
        
        # Determine background color based on state
        if not self.enabled:
            bg_color = (80, 80, 80)
        elif self.pressed:
            bg_color = self.press_color
        elif self.hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.bg_color
        
        # Draw background
        pygame.draw.rect(screen, bg_color, rect)
        
        # Draw border
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, rect, self.border_width)
        
        # Draw image or text
        if self.image:
            # Center image on button
            image_rect = self.image.get_rect()
            image_rect.center = rect.center
            screen.blit(self.image, image_rect)
        elif self.text_surface:
            # Center text on button
            text_rect = self.text_surface.get_rect()
            text_rect.center = rect.center
            screen.blit(self.text_surface, text_rect)
    
    def set_text(self, text: str) -> None:
        """
        Change button text.
        
        Args:
            text: New button text
        """
        self.text = text
        if self.font:
            self.text_surface = self.font.render(text, True, self.text_color)
    
    def set_enabled(self, enabled: bool) -> None:
        """
        Enable or disable the button.
        
        Args:
            enabled: True to enable, False to disable
        """
        self.enabled = enabled
    
    def set_callback(self, callback: Callable) -> None:
        """
        Set button click callback.
        
        Args:
            callback: Function to call when clicked
        """
        self.callback = callback
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set button position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.position[0] = x
        self.position[1] = y
    
    def set_size(self, width: float, height: float) -> None:
        """
        Set button size.
        
        Args:
            width: Button width
            height: Button height
        """
        self.size[0] = width
        self.size[1] = height
    
    def is_hovered(self) -> bool:
        """
        Check if button is hovered.
        
        Returns:
            True if mouse is over button
        """
        return self.hovered
    
    def is_pressed(self) -> bool:
        """
        Check if button is pressed.
        
        Returns:
            True if button is currently pressed
        """
        return self.pressed
