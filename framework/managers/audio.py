"""
Audio management module.

This module provides centralized audio management for background music
and sound effects.
"""

from typing import Optional
import pygame


class AudioManager:
    """
    Manager for game audio (music and sound effects).
    
    This manager handles:
    - Background music playback
    - Sound effect playback
    - Volume control for music and sounds
    
    Attributes:
        music_volume: Current music volume (0.0 to 1.0)
        sound_volume: Current sound effects volume (0.0 to 1.0)
        current_music: Path to currently playing music
    """
    
    def __init__(self):
        """Initialize the audio manager."""
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.music_volume: float = 1.0
        self.sound_volume: float = 1.0
        self.current_music: Optional[str] = None
        
        # Set initial volume
        pygame.mixer.music.set_volume(self.music_volume)
    
    def play_music(
        self,
        path: str,
        loops: int = -1,
        fade_ms: int = 0
    ) -> None:
        """
        Play background music.
        
        Args:
            path: Path to music file
            loops: Number of times to loop (-1 for infinite)
            fade_ms: Fade-in time in milliseconds
        """
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops, fade_ms=fade_ms)
            self.current_music = path
        except pygame.error as e:
            print(f"Error loading music '{path}': {e}")
    
    def stop_music(self, fade_ms: int = 0) -> None:
        """
        Stop the currently playing music.
        
        Args:
            fade_ms: Fade-out time in milliseconds
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self) -> None:
        """Pause the currently playing music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self) -> None:
        """Resume paused music."""
        pygame.mixer.music.unpause()
    
    def is_music_playing(self) -> bool:
        """
        Check if music is currently playing.
        
        Returns:
            True if music is playing
        """
        return pygame.mixer.music.get_busy()
    
    def set_music_volume(self, volume: float) -> None:
        """
        Set the music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def get_music_volume(self) -> float:
        """
        Get the current music volume.
        
        Returns:
            Current music volume (0.0 to 1.0)
        """
        return self.music_volume
    
    def play_sound(self, sound: pygame.mixer.Sound, loops: int = 0) -> None:
        """
        Play a sound effect.
        
        Args:
            sound: Pygame Sound object to play
            loops: Number of additional times to play (0 = once)
        """
        sound.set_volume(self.sound_volume)
        sound.play(loops)
    
    def set_sound_volume(self, volume: float) -> None:
        """
        Set the sound effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def get_sound_volume(self) -> float:
        """
        Get the current sound effects volume.
        
        Returns:
            Current sound volume (0.0 to 1.0)
        """
        return self.sound_volume
    
    def stop_all_sounds(self) -> None:
        """Stop all currently playing sound effects."""
        pygame.mixer.stop()
    
    def get_current_music(self) -> Optional[str]:
        """
        Get the path to the currently playing music.
        
        Returns:
            Path to current music file or None
        """
        return self.current_music
