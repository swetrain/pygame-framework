"""
Animation component module.

This module provides frame-based sprite animation support.
"""

from typing import List, Optional
import pygame


class Animation:
    """
    Component for frame-based sprite animation.
    
    Supports:
    - Multiple animation frames
    - Adjustable playback speed
    - Loop and one-shot modes
    - Animation state tracking
    
    Attributes:
        entity: Reference to parent entity
        frames: List of pygame Surfaces for animation frames
        frame_duration: Duration of each frame in seconds
        loop: Whether to loop the animation
        current_frame: Current frame index
        playing: Whether animation is currently playing
        finished: Whether one-shot animation has finished
    """
    
    def __init__(
        self,
        frames: List[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True,
        autoplay: bool = True
    ):
        """
        Initialize the animation component.
        
        Args:
            frames: List of pygame Surfaces (animation frames)
            frame_duration: Duration of each frame in seconds
            loop: Whether to loop the animation
            autoplay: Start playing automatically
        """
        self.entity: Optional['Entity'] = None
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.playing = autoplay
        self.finished = False
        
        if not frames:
            raise ValueError("Animation must have at least one frame")
    
    def play(self) -> None:
        """Start or resume animation playback."""
        self.playing = True
        self.finished = False
    
    def stop(self) -> None:
        """Stop animation playback."""
        self.playing = False
    
    def reset(self) -> None:
        """Reset animation to first frame."""
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.finished = False
    
    def restart(self) -> None:
        """Reset and start playing animation."""
        self.reset()
        self.play()
    
    def update(self, dt: float) -> None:
        """
        Update animation state.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.playing or self.finished:
            return
        
        self.time_accumulator += dt
        
        # Check if we should advance to next frame
        while self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame += 1
            
            # Handle end of animation
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    self.playing = False
    
    def get_current_frame(self) -> pygame.Surface:
        """
        Get the current animation frame.
        
        Returns:
            Current frame as pygame Surface
        """
        return self.frames[self.current_frame]
    
    def set_frame(self, frame_index: int) -> None:
        """
        Set the current frame index.
        
        Args:
            frame_index: Frame index to set
        """
        self.current_frame = max(0, min(frame_index, len(self.frames) - 1))
    
    def is_finished(self) -> bool:
        """
        Check if animation has finished (for one-shot animations).
        
        Returns:
            True if animation has finished
        """
        return self.finished
    
    def is_playing(self) -> bool:
        """
        Check if animation is currently playing.
        
        Returns:
            True if animation is playing
        """
        return self.playing
    
    def set_frame_duration(self, duration: float) -> None:
        """
        Change the frame duration (animation speed).
        
        Args:
            duration: New frame duration in seconds
        """
        self.frame_duration = max(0.001, duration)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the current animation frame.
        
        Args:
            screen: Pygame surface to render to
        """
        if not self.entity or not self.frames:
            return
        
        current_image = self.get_current_frame()
        
        # Calculate position to center the frame on entity position
        rect = current_image.get_rect()
        rect.center = (
            self.entity.position[0] + self.entity.size[0] / 2,
            self.entity.position[1] + self.entity.size[1] / 2
        )
        
        screen.blit(current_image, rect)


class AnimationController:
    """
    Controller for managing multiple named animations.
    
    Allows switching between different animation states (e.g., idle, walk, jump).
    """
    
    def __init__(self):
        """Initialize the animation controller."""
        self.animations: dict = {}
        self.current_animation: Optional[str] = None
    
    def add_animation(self, name: str, animation: Animation) -> None:
        """
        Add a named animation.
        
        Args:
            name: Unique animation name
            animation: Animation instance
        """
        self.animations[name] = animation
    
    def play_animation(self, name: str, restart: bool = False) -> None:
        """
        Play a named animation.
        
        Args:
            name: Name of animation to play
            restart: Whether to restart if already playing this animation
        """
        if name not in self.animations:
            return
        
        # Stop current animation if different
        if self.current_animation and self.current_animation != name:
            self.animations[self.current_animation].stop()
        
        # Play new animation
        if restart or self.current_animation != name:
            self.animations[name].restart()
        else:
            self.animations[name].play()
        
        self.current_animation = name
    
    def update(self, dt: float) -> None:
        """
        Update the current animation.
        
        Args:
            dt: Delta time in seconds
        """
        if self.current_animation:
            self.animations[self.current_animation].update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the current animation.
        
        Args:
            screen: Pygame surface to render to
        """
        if self.current_animation:
            self.animations[self.current_animation].render(screen)
    
    def get_current_animation(self) -> Optional[Animation]:
        """
        Get the currently playing animation.
        
        Returns:
            Current Animation instance or None
        """
        if self.current_animation:
            return self.animations.get(self.current_animation)
        return None
