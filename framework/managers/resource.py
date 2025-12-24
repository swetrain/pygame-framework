"""
리소스 관리 모듈

이 모듈은 이미지, 사운드, 폰트와 같은 게임 리소스를 로딩하고 캐싱하기 위한
싱글톤 ResourceManager를 제공합니다.
"""

from typing import Dict, Optional, Tuple
import pygame
import os


class ResourceManager:
    """
    게임 에셋을 로딩하고 캐싱하기 위한 싱글톤 리소스 매니저
    
    이 매니저는 다음을 처리합니다:
    - 이미지 로딩과 캐싱
    - 사운드 로딩과 캐싱
    - 폰트 로딩과 캐싱
    - 자동 리소스 정리
    
    싱글톤 패턴은 하나의 인스턴스만 존재하도록 보장하여
    중복 리소스 로딩을 방지합니다.
    """
    
    _instance: Optional['ResourceManager'] = None
    
    def __new__(cls):
        """싱글톤 패턴을 구현합니다."""
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """리소스 매니저를 초기화합니다 (한 번만)."""
        if self._initialized:
            return
        
        self._initialized = True
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        self.base_path: str = ""
    
    def set_base_path(self, path: str) -> None:
        """
        리소스 로딩을 위한 기본 경로를 설정합니다.
        
        Args:
            path: 리소스를 위한 기본 디렉토리 경로
        """
        self.base_path = path
    
    def load_image(
        self,
        path: str,
        convert_alpha: bool = True,
        scale: Optional[Tuple[int, int]] = None
    ) -> pygame.Surface:
        """
        파일에서 이미지를 로드하고 캐싱합니다.
        
        Args:
            path: 이미지 파일 경로 (base_path 기준 상대 경로)
            convert_alpha: 알파 투명도를 위해 이미지를 변환할지 여부
            scale: 이미지 크기를 조정할 선택적 (너비, 높이)
            
        Returns:
            이미지를 포함하는 Pygame Surface
            
        Raises:
            FileNotFoundError: 이미지 파일이 존재하지 않는 경우
        """
        cache_key = f"{path}_{scale}"
        
        if cache_key in self.images:
            return self.images[cache_key]
        
        full_path = os.path.join(self.base_path, path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Image not found: {full_path}")
        
        image = pygame.image.load(full_path)
        
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        
        if scale:
            image = pygame.transform.scale(image, scale)
        
        self.images[cache_key] = image
        return image
    
    def create_surface(
        self,
        size: Tuple[int, int],
        color: Tuple[int, int, int],
        alpha: bool = True
    ) -> pygame.Surface:
        """
        색상이 있는 표면을 생성합니다 (플레이스홀더 그래픽에 유용).
        
        Args:
            size: 표면의 (너비, 높이)
            color: RGB 색상 튜플
            alpha: 알파 채널을 활성화할지 여부
            
        Returns:
            지정된 색상으로 채워진 Pygame Surface
        """
        if alpha:
            surface = pygame.Surface(size, pygame.SRCALPHA)
        else:
            surface = pygame.Surface(size)
        surface.fill(color)
        return surface
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """
        파일에서 사운드를 로드하고 캐싱합니다.
        
        Args:
            path: 사운드 파일 경로 (base_path 기준 상대 경로)
            
        Returns:
            Pygame Sound 객체
            
        Raises:
            FileNotFoundError: 사운드 파일이 존재하지 않는 경우
        """
        if path in self.sounds:
            return self.sounds[path]
        
        full_path = os.path.join(self.base_path, path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Sound not found: {full_path}")
        
        sound = pygame.mixer.Sound(full_path)
        self.sounds[path] = sound
        return sound
    
    def load_font(
        self,
        path: Optional[str] = None,
        size: int = 24
    ) -> pygame.font.Font:
        """
        폰트를 로드하고 캐싱합니다.
        
        Args:
            path: 폰트 파일 경로 (기본 폰트는 None)
            size: 포인트 단위 폰트 크기
            
        Returns:
            Pygame Font 객체
            
        Raises:
            FileNotFoundError: 폰트 파일이 존재하지 않는 경우
        """
        cache_key = (path or "", size)
        
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        if path:
            full_path = os.path.join(self.base_path, path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Font not found: {full_path}")
            font = pygame.font.Font(full_path, size)
        else:
            font = pygame.font.Font(None, size)
        
        self.fonts[cache_key] = font
        return font
    
    def clear_images(self) -> None:
        """캐시된 모든 이미지를 지웁니다."""
        self.images.clear()
    
    def clear_sounds(self) -> None:
        """캐시된 모든 사운드를 지웁니다."""
        self.sounds.clear()
    
    def clear_fonts(self) -> None:
        """캐시된 모든 폰트를 지웁니다."""
        self.fonts.clear()
    
    def clear_all(self) -> None:
        """캐시된 모든 리소스를 지웁니다."""
        self.clear_images()
        self.clear_sounds()
        self.clear_fonts()
    
    def get_cached_image(self, path: str) -> Optional[pygame.Surface]:
        """
        로딩 없이 캐시된 이미지를 가져옵니다.
        
        Args:
            path: 이미지 파일 경로
            
        Returns:
            캐시된 이미지 또는 캐시에 없으면 None
        """
        return self.images.get(path)
    
    def get_cached_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        로딩 없이 캐시된 사운드를 가져옵니다.
        
        Args:
            path: 사운드 파일 경로
            
        Returns:
            캐시된 사운드 또는 캐시에 없으면 None
        """
        return self.sounds.get(path)
