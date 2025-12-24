"""
Main game engine module.

This module provides the core Game class that manages the game loop,
screen initialization, and scene management.
"""

from typing import Optional, Tuple
import pygame
from framework.core.scene import SceneManager


class Game:
    """
    Main game engine class that handles initialization and the game loop.
    
    This class manages:
    - Window initialization
    - Game loop (events, update, render)
    - FPS limiting and delta time calculation
    - Scene management integration
    
    Attributes:
        screen_size: Tuple of (width, height) for the game window
        title: Window title
        fps: Target frames per second
        screen: Pygame display surface
        clock: Pygame clock for FPS management
        scene_manager: SceneManager instance for scene transitions
        running: Flag indicating if the game loop is active
        dt: Delta time in seconds since last frame
    """
    
    def __init__(
        self,
        screen_size: Tuple[int, int] = (800, 600),
        title: str = "Pygame Framework Game",
        fps: int = 60,
        flags: int = 0
    ):
        """
        Initialize the game engine.
        
        Args:
            screen_size: Window dimensions (width, height)
            title: Window title
            fps: Target frames per second
            flags: Pygame display flags (e.g., pygame.FULLSCREEN)
        """
        self.screen_size = screen_size
        self.title = title
        self.fps = fps
        self.flags = flags
        
        # Initialize Pygame
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption(title)
        
        # Create clock for FPS management
        self.clock = pygame.time.Clock()
        
        # Scene management
        self.scene_manager = SceneManager()
        
        # Game state
        self.running = False
        self.dt = 0.0
    
    def run(self) -> None:
        """
        Start the main game loop.
        
        The game loop handles:
        1. Event processing
        2. Scene updates
        3. Scene rendering
        4. FPS limiting and delta time calculation
        """
        self.running = True
        
        while self.running:
            # Calculate delta time (in seconds)
            self.dt = self.clock.tick(self.fps) / 1000.0
            
            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Update current scene
            if self.scene_manager.current_scene:
                self.scene_manager.current_scene.handle_events(events)
                self.scene_manager.current_scene.update(self.dt)
            
            # Render current scene
            self.screen.fill((0, 0, 0))  # Clear screen with black
            if self.scene_manager.current_scene:
                self.scene_manager.current_scene.render(self.screen)
            
            # Update display
            pygame.display.flip()
        
        # Cleanup
        self.quit()
    
    def quit(self) -> None:
        """Clean up resources and quit pygame."""
        pygame.quit()
    
    def set_scene(self, scene_name: str) -> None:
        """
        Change to a different scene.
        
        Args:
            scene_name: Name of the scene to switch to
        """
        self.scene_manager.change_scene(scene_name)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the current screen dimensions.
        
        Returns:
            Tuple of (width, height)
        """
        return self.screen_size
    
    def get_fps(self) -> float:
        """
        Get the current frames per second.
        
        Returns:
            Current FPS as a float
        """
        return self.clock.get_fps()
