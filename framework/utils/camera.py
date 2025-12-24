"""
카메라/뷰포트 시스템 모듈

이 모듈은 스크롤링, 엔티티 추적, 화면 흔들림 효과를 위한
카메라 기능을 제공합니다.
"""

from typing import Optional, Tuple
import pygame
import random
import math


class Camera:
    """
    2D 게임을 위한 카메라/뷰포트 시스템
    
    지원 기능:
    - 카메라 위치와 이동
    - 엔티티 추적 (팔로우 카메라)
    - 줌 인/아웃
    - 화면 흔들림 효과
    - 경계 제한
    
    Attributes:
        position: 월드 공간에서의 카메라 위치 [x, y]
        viewport_size: 뷰포트의 크기 (너비, 높이)
        zoom: 줌 레벨 (1.0 = 일반)
        shake_intensity: 현재 흔들림 강도
        shake_duration: 남은 흔들림 지속 시간
    """
    
    def __init__(
        self,
        viewport_size: Tuple[int, int],
        world_size: Optional[Tuple[int, int]] = None
    ):
        """
        카메라를 초기화합니다.
        
        Args:
            viewport_size: 가시 뷰포트의 크기 (너비, 높이)
            world_size: 선택적 월드 경계 (너비, 높이)
        """
        self.position = [0.0, 0.0]
        self.viewport_size = viewport_size
        self.world_size = world_size
        self.zoom = 1.0
        
        # 추적 대상
        self.follow_target: Optional['Entity'] = None
        self.follow_speed = 1.0
        self.follow_offset = [0, 0]
        
        # 화면 흔들림
        self.shake_intensity = 0.0
        self.shake_duration = 0.0
        self.shake_offset = [0, 0]
    
    def update(self, dt: float) -> None:
        """
        카메라 상태를 업데이트합니다.
        
        Args:
            dt: 델타 타임 (초 단위)
        """
        # 추적 대상 업데이트
        if self.follow_target:
            target_x = self.follow_target.position[0] + self.follow_offset[0] - self.viewport_size[0] / 2
            target_y = self.follow_target.position[1] + self.follow_offset[1] - self.viewport_size[1] / 2
            
            # 부드러운 추적
            self.position[0] += (target_x - self.position[0]) * self.follow_speed * dt * 10
            self.position[1] += (target_y - self.position[1]) * self.follow_speed * dt * 10
        
        # 화면 흔들림 업데이트
        if self.shake_duration > 0:
            self.shake_duration -= dt
            angle = random.uniform(0, 2 * math.pi)
            self.shake_offset[0] = math.cos(angle) * self.shake_intensity
            self.shake_offset[1] = math.sin(angle) * self.shake_intensity
        else:
            self.shake_offset = [0, 0]
        
        # 월드 경계 적용
        if self.world_size:
            self.position[0] = max(0, min(self.position[0], self.world_size[0] - self.viewport_size[0]))
            self.position[1] = max(0, min(self.position[1], self.world_size[1] - self.viewport_size[1]))
    
    def set_position(self, x: float, y: float) -> None:
        """
        월드 공간에서 카메라 위치를 설정합니다.
        
        Args:
            x: X 좌표
            y: Y 좌표
        """
        self.position[0] = x
        self.position[1] = y
    
    def move(self, dx: float, dy: float) -> None:
        """
        카메라를 델타만큼 이동합니다.
        
        Args:
            dx: x의 변화량
            dy: y의 변화량
        """
        self.position[0] += dx
        self.position[1] += dy
    
    def follow(
        self,
        entity: 'Entity',
        speed: float = 1.0,
        offset: Tuple[float, float] = (0, 0)
    ) -> None:
        """
        카메라가 엔티티를 추적하도록 만듭니다.
        
        Args:
            entity: 추적할 엔티티
            speed: 추적 속도 (0-1, 1 = 즉시)
            offset: 엔티티 위치로부터의 오프셋
        """
        self.follow_target = entity
        self.follow_speed = speed
        self.follow_offset = list(offset)
    
    def unfollow(self) -> None:
        """현재 대상 추적을 중지합니다."""
        self.follow_target = None
    
    def shake(self, intensity: float, duration: float) -> None:
        """
        화면 흔들림 효과를 적용합니다.
        
        Args:
            intensity: 흔들림 강도 (픽셀)
            duration: 흔들림 지속 시간 (초)
        """
        self.shake_intensity = intensity
        self.shake_duration = duration
    
    def set_zoom(self, zoom: float) -> None:
        """
        카메라 줌 레벨을 설정합니다.
        
        Args:
            zoom: 줌 레벨 (1.0 = 일반, >1 = 확대, <1 = 축소)
        """
        self.zoom = max(0.1, zoom)
    
    def get_zoom(self) -> float:
        """
        현재 줌 레벨을 반환합니다.
        
        Returns:
            현재 줌 레벨
        """
        return self.zoom
    
    def world_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """
        월드 좌표를 화면 좌표로 변환합니다.
        
        Args:
            x: 월드 x 좌표
            y: 월드 y 좌표
            
        Returns:
            (screen_x, screen_y)의 튜플
        """
        screen_x = (x - self.position[0]) * self.zoom + self.shake_offset[0]
        screen_y = (y - self.position[1]) * self.zoom + self.shake_offset[1]
        return (screen_x, screen_y)
    
    def screen_to_world(self, x: float, y: float) -> Tuple[float, float]:
        """
        화면 좌표를 월드 좌표로 변환합니다.
        
        Args:
            x: 화면 x 좌표
            y: 화면 y 좌표
            
        Returns:
            (world_x, world_y)의 튜플
        """
        world_x = (x - self.shake_offset[0]) / self.zoom + self.position[0]
        world_y = (y - self.shake_offset[1]) / self.zoom + self.position[1]
        return (world_x, world_y)
    
    def apply(self, entity_pos: Tuple[float, float]) -> Tuple[float, float]:
        """
        위치에 카메라 변환을 적용합니다.
        
        Args:
            entity_pos: 월드 공간에서의 위치 (x, y)
            
        Returns:
            화면 공간에서의 위치 (x, y)
        """
        return self.world_to_screen(entity_pos[0], entity_pos[1])
    
    def get_rect(self) -> pygame.Rect:
        """
        월드 공간에서 카메라 뷰포트 사각형을 반환합니다.
        
        Returns:
            가시 영역을 나타내는 Pygame Rect
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.viewport_size[0] / self.zoom,
            self.viewport_size[1] / self.zoom
        )
    
    def is_visible(self, rect: pygame.Rect) -> bool:
        """
        사각형이 카메라 뷰에 보이는지 확인합니다.
        
        Args:
            rect: 월드 공간의 사각형
            
        Returns:
            사각형이 카메라 뷰포트와 교차하면 True
        """
        camera_rect = self.get_rect()
        return camera_rect.colliderect(rect)
