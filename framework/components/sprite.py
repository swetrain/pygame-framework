"""
스프라이트 컴포넌트 모듈

이 모듈은 변환 지원을 포함한 스프라이트 렌더링 컴포넌트를 제공합니다.
"""

from typing import Optional, Tuple
import pygame


class Sprite:
    """
    이미지/스프라이트 렌더링을 위한 컴포넌트
    
    지원 기능:
    - 이미지 렌더링
    - 크기 조정과 회전
    - 뒤집기 (가로/세로)
    - 알파 투명도
    
    Attributes:
        entity: 부모 엔티티에 대한 참조
        image: 원본 이미지 표면
        transformed_image: 캐시된 변환 이미지
        scale: 크기 배율 (1.0 = 원본 크기)
        rotation: 회전 각도 (도 단위)
        flip_x: 가로로 뒤집을지 여부
        flip_y: 세로로 뒤집을지 여부
        alpha: 알파 투명도 (0-255)
    """
    
    def __init__(
        self,
        image: pygame.Surface,
        scale: float = 1.0,
        rotation: float = 0.0,
        flip_x: bool = False,
        flip_y: bool = False,
        alpha: int = 255
    ):
        """
        스프라이트 컴포넌트를 초기화합니다.
        
        Args:
            image: 렌더링할 Pygame Surface
            scale: 크기 배율
            rotation: 초기 회전 각도 (도 단위)
            flip_x: 가로로 뒤집기
            flip_y: 세로로 뒤집기
            alpha: 알파 투명도 (0-255)
        """
        self.entity: Optional['Entity'] = None
        self.image = image
        self.original_image = image
        self.transformed_image = image
        self._scale = scale
        self._rotation = rotation
        self._flip_x = flip_x
        self._flip_y = flip_y
        self._alpha = alpha
        self._needs_update = True
        
        self._update_transform()
    
    def _update_transform(self) -> None:
        """현재 속성을 기반으로 변환된 이미지를 업데이트합니다."""
        if not self._needs_update:
            return
        
        image = self.original_image
        
        # 뒤집기 적용
        if self._flip_x or self._flip_y:
            image = pygame.transform.flip(image, self._flip_x, self._flip_y)
        
        # 크기 조정 적용
        if self._scale != 1.0:
            new_size = (
                int(image.get_width() * self._scale),
                int(image.get_height() * self._scale)
            )
            image = pygame.transform.scale(image, new_size)
        
        # 회전 적용
        if self._rotation != 0:
            image = pygame.transform.rotate(image, self._rotation)
        
        # 알파 적용
        if self._alpha != 255:
            image.set_alpha(self._alpha)
        
        self.transformed_image = image
        self._needs_update = False
    
    @property
    def scale(self) -> float:
        """크기 배율을 반환합니다."""
        return self._scale
    
    @scale.setter
    def scale(self, value: float) -> None:
        """크기 배율을 설정합니다."""
        if self._scale != value:
            self._scale = value
            self._needs_update = True
    
    @property
    def rotation(self) -> float:
        """회전 각도를 반환합니다 (도 단위)."""
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float) -> None:
        """회전 각도를 설정합니다 (도 단위)."""
        if self._rotation != value:
            self._rotation = value % 360
            self._needs_update = True
    
    @property
    def flip_x(self) -> bool:
        """가로 뒤집기 상태를 반환합니다."""
        return self._flip_x
    
    @flip_x.setter
    def flip_x(self, value: bool) -> None:
        """가로 뒤집기 상태를 설정합니다."""
        if self._flip_x != value:
            self._flip_x = value
            self._needs_update = True
    
    @property
    def flip_y(self) -> bool:
        """세로 뒤집기 상태를 반환합니다."""
        return self._flip_y
    
    @flip_y.setter
    def flip_y(self, value: bool) -> None:
        """세로 뒤집기 상태를 설정합니다."""
        if self._flip_y != value:
            self._flip_y = value
            self._needs_update = True
    
    @property
    def alpha(self) -> int:
        """알파 투명도를 반환합니다."""
        return self._alpha
    
    @alpha.setter
    def alpha(self, value: int) -> None:
        """알파 투명도를 설정합니다 (0-255)."""
        value = max(0, min(255, value))
        if self._alpha != value:
            self._alpha = value
            self._needs_update = True
    
    def set_image(self, image: pygame.Surface) -> None:
        """
        스프라이트 이미지를 변경합니다.
        
        Args:
            image: 새로운 pygame Surface
        """
        self.original_image = image
        self.image = image
        self._needs_update = True
    
    def render(self, screen: pygame.Surface) -> None:
        """
        스프라이트를 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        if not self.entity:
            return
        
        self._update_transform()
        
        # 엔티티 위치에 스프라이트를 중앙 배치하기 위한 위치 계산
        rect = self.transformed_image.get_rect()
        rect.center = (
            self.entity.position[0] + self.entity.size[0] / 2,
            self.entity.position[1] + self.entity.size[1] / 2
        )
        
        screen.blit(self.transformed_image, rect)
    
    def get_size(self) -> Tuple[int, int]:
        """
        변환된 스프라이트의 현재 크기를 반환합니다.
        
        Returns:
            (너비, 높이)의 튜플
        """
        self._update_transform()
        return self.transformed_image.get_size()
