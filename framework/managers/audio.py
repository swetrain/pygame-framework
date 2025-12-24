"""
오디오 관리 모듈

이 모듈은 배경 음악과 사운드 효과를 위한
중앙집중식 오디오 관리를 제공합니다.
"""

from typing import Optional
import pygame


class AudioManager:
    """
    게임 오디오(음악과 사운드 효과)를 위한 매니저
    
    이 매니저는 다음을 처리합니다:
    - 배경 음악 재생
    - 사운드 효과 재생
    - 음악과 사운드의 볼륨 제어
    
    Attributes:
        music_volume: 현재 음악 볼륨 (0.0 ~ 1.0)
        sound_volume: 현재 사운드 효과 볼륨 (0.0 ~ 1.0)
        current_music: 현재 재생 중인 음악의 경로
    """
    
    def __init__(self):
        """오디오 매니저를 초기화합니다."""
        # 아직 초기화되지 않았다면 pygame mixer 초기화
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.music_volume: float = 1.0
        self.sound_volume: float = 1.0
        self.current_music: Optional[str] = None
        
        # 초기 볼륨 설정
        pygame.mixer.music.set_volume(self.music_volume)
    
    def play_music(
        self,
        path: str,
        loops: int = -1,
        fade_ms: int = 0
    ) -> None:
        """
        배경 음악을 재생합니다.
        
        Args:
            path: 음악 파일 경로
            loops: 반복 횟수 (무한 반복은 -1)
            fade_ms: 페이드인 시간 (밀리초)
        """
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops, fade_ms=fade_ms)
            self.current_music = path
        except pygame.error as e:
            print(f"Error loading music '{path}': {e}")
    
    def stop_music(self, fade_ms: int = 0) -> None:
        """
        현재 재생 중인 음악을 중지합니다.
        
        Args:
            fade_ms: 페이드아웃 시간 (밀리초)
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self) -> None:
        """현재 재생 중인 음악을 일시정지합니다."""
        pygame.mixer.music.pause()
    
    def unpause_music(self) -> None:
        """일시정지된 음악을 재개합니다."""
        pygame.mixer.music.unpause()
    
    def is_music_playing(self) -> bool:
        """
        음악이 현재 재생 중인지 확인합니다.
        
        Returns:
            음악이 재생 중이면 True
        """
        return pygame.mixer.music.get_busy()
    
    def set_music_volume(self, volume: float) -> None:
        """
        음악 볼륨을 설정합니다.
        
        Args:
            volume: 볼륨 레벨 (0.0 ~ 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def get_music_volume(self) -> float:
        """
        현재 음악 볼륨을 반환합니다.
        
        Returns:
            현재 음악 볼륨 (0.0 ~ 1.0)
        """
        return self.music_volume
    
    def play_sound(self, sound: pygame.mixer.Sound, loops: int = 0) -> None:
        """
        사운드 효과를 재생합니다.
        
        Args:
            sound: 재생할 Pygame Sound 객체
            loops: 추가 재생 횟수 (0 = 한 번)
        """
        sound.set_volume(self.sound_volume)
        sound.play(loops)
    
    def set_sound_volume(self, volume: float) -> None:
        """
        사운드 효과 볼륨을 설정합니다.
        
        Args:
            volume: 볼륨 레벨 (0.0 ~ 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def get_sound_volume(self) -> float:
        """
        현재 사운드 효과 볼륨을 반환합니다.
        
        Returns:
            현재 사운드 볼륨 (0.0 ~ 1.0)
        """
        return self.sound_volume
    
    def stop_all_sounds(self) -> None:
        """현재 재생 중인 모든 사운드 효과를 중지합니다."""
        pygame.mixer.stop()
    
    def get_current_music(self) -> Optional[str]:
        """
        현재 재생 중인 음악의 경로를 반환합니다.
        
        Returns:
            현재 음악 파일의 경로 또는 None
        """
        return self.current_music
