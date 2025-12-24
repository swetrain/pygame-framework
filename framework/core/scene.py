"""
Scene system module.

This module provides the Scene base class and SceneManager for handling
different game states and transitions.
"""

from typing import Dict, List, Optional
import pygame


class Scene:
    """
    Base class for all game scenes.
    
    A scene represents a distinct game state (e.g., menu, gameplay, game over).
    Subclasses should override the methods to implement specific behavior.
    
    Attributes:
        name: Unique identifier for this scene
        game: Reference to the main game instance
    """
    
    def __init__(self, name: str, game: Optional['Game'] = None):
        """
        Initialize the scene.
        
        Args:
            name: Unique scene identifier
            game: Reference to the main Game instance
        """
        self.name = name
        self.game = game
    
    def on_enter(self) -> None:
        """
        Called when entering this scene.
        
        Override this to initialize scene-specific resources,
        reset state, or start background music.
        """
        pass
    
    def on_exit(self) -> None:
        """
        Called when exiting this scene.
        
        Override this to clean up resources or save state.
        """
        pass
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Handle pygame events for this scene.
        
        Args:
            events: List of pygame events to process
        """
        pass
    
    def update(self, dt: float) -> None:
        """
        Update scene logic.
        
        Args:
            dt: Delta time in seconds since last frame
        """
        pass
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the scene to the screen.
        
        Args:
            screen: Pygame surface to render to
        """
        pass


class SceneManager:
    """
    Manager for scene transitions and scene stack.
    
    The SceneManager handles switching between scenes and maintains
    a stack for push/pop scene operations (e.g., pause menus).
    
    Attributes:
        scenes: Dictionary mapping scene names to Scene instances
        scene_stack: Stack of active scenes
        current_scene: Currently active scene (top of stack)
    """
    
    def __init__(self):
        """Initialize the scene manager."""
        self.scenes: Dict[str, Scene] = {}
        self.scene_stack: List[Scene] = []
        self.current_scene: Optional[Scene] = None
    
    def add_scene(self, scene: Scene) -> None:
        """
        Register a scene with the manager.
        
        Args:
            scene: Scene instance to register
        """
        self.scenes[scene.name] = scene
    
    def remove_scene(self, scene_name: str) -> None:
        """
        Remove a scene from the manager.
        
        Args:
            scene_name: Name of the scene to remove
        """
        if scene_name in self.scenes:
            del self.scenes[scene_name]
    
    def change_scene(self, scene_name: str) -> None:
        """
        Switch to a different scene, replacing the current one.
        
        Args:
            scene_name: Name of the scene to switch to
            
        Raises:
            KeyError: If the scene name is not registered
        """
        if scene_name not in self.scenes:
            raise KeyError(f"Scene '{scene_name}' not found")
        
        # Exit current scene
        if self.current_scene:
            self.current_scene.on_exit()
        
        # Clear stack and set new scene
        self.scene_stack.clear()
        self.current_scene = self.scenes[scene_name]
        self.scene_stack.append(self.current_scene)
        
        # Enter new scene
        self.current_scene.on_enter()
    
    def push_scene(self, scene_name: str) -> None:
        """
        Push a scene onto the stack without exiting the current one.
        
        Useful for overlays like pause menus.
        
        Args:
            scene_name: Name of the scene to push
            
        Raises:
            KeyError: If the scene name is not registered
        """
        if scene_name not in self.scenes:
            raise KeyError(f"Scene '{scene_name}' not found")
        
        scene = self.scenes[scene_name]
        self.scene_stack.append(scene)
        self.current_scene = scene
        self.current_scene.on_enter()
    
    def pop_scene(self) -> None:
        """
        Pop the current scene from the stack and return to the previous one.
        
        Raises:
            IndexError: If there's only one scene in the stack
        """
        if len(self.scene_stack) <= 1:
            raise IndexError("Cannot pop the last scene")
        
        # Exit current scene
        if self.current_scene:
            self.current_scene.on_exit()
        
        # Pop and set previous scene as current
        self.scene_stack.pop()
        self.current_scene = self.scene_stack[-1]
    
    def get_scene(self, scene_name: str) -> Optional[Scene]:
        """
        Get a registered scene by name.
        
        Args:
            scene_name: Name of the scene to retrieve
            
        Returns:
            Scene instance or None if not found
        """
        return self.scenes.get(scene_name)
