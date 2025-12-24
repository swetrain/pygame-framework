"""
Text UI component module.

This module provides text rendering with alignment and styling options.
"""

from typing import Tuple, Optional
import pygame


class Text:
    """
    Text rendering component.
    
    Supports:
    - Custom fonts, sizes, and colors
    - Text alignment (left, center, right)
    - Anti-aliasing
    - Background color
    
    Attributes:
        text: Text string to render
        position: Position to render at (x, y)
        font: Pygame font object
        color: Text color
        antialias: Whether to use anti-aliasing
        alignment: Text alignment ("left", "center", "right")
        surface: Cached text surface
    """
    
    def __init__(
        self,
        text: str,
        position: Tuple[float, float],
        font_size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        font_path: Optional[str] = None,
        antialias: bool = True,
        alignment: str = "left",
        bg_color: Optional[Tuple[int, int, int]] = None
    ):
        """
        Initialize the text component.
        
        Args:
            text: Text string to display
            position: Position to render at (x, y)
            font_size: Font size in points
            color: Text color RGB tuple
            font_path: Path to custom font file (None for default)
            antialias: Whether to use anti-aliasing
            alignment: Text alignment ("left", "center", "right")
            bg_color: Optional background color
        """
        self.text = text
        self.position = list(position)
        self.color = color
        self.antialias = antialias
        self.alignment = alignment
        self.bg_color = bg_color
        
        # Load font
        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)
        
        # Render text surface
        self._render_text()
    
    def _render_text(self) -> None:
        """Render the text to a surface."""
        if self.bg_color:
            self.surface = self.font.render(
                self.text,
                self.antialias,
                self.color,
                self.bg_color
            )
        else:
            self.surface = self.font.render(
                self.text,
                self.antialias,
                self.color
            )
    
    def set_text(self, text: str) -> None:
        """
        Change the text string.
        
        Args:
            text: New text to display
        """
        if self.text != text:
            self.text = text
            self._render_text()
    
    def set_color(self, color: Tuple[int, int, int]) -> None:
        """
        Change text color.
        
        Args:
            color: New RGB color tuple
        """
        if self.color != color:
            self.color = color
            self._render_text()
    
    def set_position(self, x: float, y: float) -> None:
        """
        Change text position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.position[0] = x
        self.position[1] = y
    
    def get_position(self) -> Tuple[float, float]:
        """
        Get text position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return tuple(self.position)
    
    def get_size(self) -> Tuple[int, int]:
        """
        Get rendered text size.
        
        Returns:
            Tuple of (width, height)
        """
        return self.surface.get_size()
    
    def get_rect(self) -> pygame.Rect:
        """
        Get text bounding rectangle.
        
        Returns:
            Pygame Rect for the text
        """
        rect = self.surface.get_rect()
        
        # Apply alignment
        if self.alignment == "left":
            rect.topleft = self.position
        elif self.alignment == "center":
            rect.center = self.position
        elif self.alignment == "right":
            rect.topright = self.position
        else:
            rect.topleft = self.position
        
        return rect
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the text to screen.
        
        Args:
            screen: Pygame surface to render to
        """
        rect = self.get_rect()
        screen.blit(self.surface, rect)
    
    def set_alignment(self, alignment: str) -> None:
        """
        Set text alignment.
        
        Args:
            alignment: Alignment mode ("left", "center", "right")
        """
        if alignment in ["left", "center", "right"]:
            self.alignment = alignment


class TextBox:
    """
    Multi-line text box with word wrapping.
    
    Useful for displaying longer text like dialogue or instructions.
    """
    
    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font_size: int = 20,
        color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Optional[Tuple[int, int, int]] = None,
        padding: int = 10,
        line_spacing: int = 5
    ):
        """
        Initialize the text box.
        
        Args:
            text: Text content
            rect: Bounding rectangle for the text box
            font_size: Font size in points
            color: Text color
            bg_color: Optional background color
            padding: Padding from edges
            line_spacing: Space between lines
        """
        self.text = text
        self.rect = rect
        self.color = color
        self.bg_color = bg_color
        self.padding = padding
        self.line_spacing = line_spacing
        
        self.font = pygame.font.Font(None, font_size)
        self.lines = self._wrap_text()
    
    def _wrap_text(self) -> list:
        """
        Wrap text to fit within the box width.
        
        Returns:
            List of text lines
        """
        words = self.text.split(' ')
        lines = []
        current_line = []
        
        max_width = self.rect.width - 2 * self.padding
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, self.color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def set_text(self, text: str) -> None:
        """
        Change text content.
        
        Args:
            text: New text to display
        """
        self.text = text
        self.lines = self._wrap_text()
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the text box.
        
        Args:
            screen: Pygame surface to render to
        """
        # Draw background
        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Draw text lines
        y = self.rect.y + self.padding
        for line in self.lines:
            text_surface = self.font.render(line, True, self.color)
            screen.blit(text_surface, (self.rect.x + self.padding, y))
            y += text_surface.get_height() + self.line_spacing
