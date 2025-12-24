"""
헬퍼 유틸리티 모듈

이 모듈은 게임 개발을 위한 공통 유틸리티 함수와 클래스를 제공합니다.
"""

import math
from typing import Tuple
import pygame


# 색상 상수
class Colors:
    """공통 색상 상수"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    DARK_GRAY = (64, 64, 64)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    BROWN = (165, 42, 42)
    PINK = (255, 192, 203)


# 거리와 기하학 함수
def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    두 점 사이의 유클리드 거리를 계산합니다.
    
    Args:
        x1: 첫 번째 점의 x 좌표
        y1: 첫 번째 점의 y 좌표
        x2: 두 번째 점의 x 좌표
        y2: 두 번째 점의 y 좌표
        
    Returns:
        점 사이의 거리
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    제곱 거리를 계산합니다 (더 빠르고 비교에 유용함).
    
    Args:
        x1: 첫 번째 점의 x 좌표
        y1: 첫 번째 점의 y 좌표
        x2: 두 번째 점의 x 좌표
        y2: 두 번째 점의 y 좌표
        
    Returns:
        점 사이의 제곱 거리
    """
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def angle_to(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    점 1에서 점 2로의 각도를 라디안으로 계산합니다.
    
    Args:
        x1: 첫 번째 점의 x 좌표
        y1: 첫 번째 점의 y 좌표
        x2: 두 번째 점의 x 좌표
        y2: 두 번째 점의 y 좌표
        
    Returns:
        라디안 단위 각도
    """
    return math.atan2(y2 - y1, x2 - x1)


def angle_to_degrees(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    점 1에서 점 2로의 각도를 도 단위로 계산합니다.
    
    Args:
        x1: 첫 번째 점의 x 좌표
        y1: 첫 번째 점의 y 좌표
        x2: 두 번째 점의 x 좌표
        y2: 두 번째 점의 y 좌표
        
    Returns:
        도 단위 각도
    """
    return math.degrees(angle_to(x1, y1, x2, y2))


def normalize_vector(x: float, y: float) -> Tuple[float, float]:
    """
    벡터를 단위 길이로 정규화합니다.
    
    Args:
        x: 벡터 x 컴포넌트
        y: 벡터 y 컴포넌트
        
    Returns:
        정규화된 벡터 (x, y)
    """
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def lerp(start: float, end: float, t: float) -> float:
    """
    두 값 사이의 선형 보간.
    
    Args:
        start: 시작 값
        end: 끝 값
        t: 보간 계수 (0-1)
        
    Returns:
        보간된 값
    """
    return start + (end - start) * t


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    값을 최소값과 최대값 사이로 제한합니다.
    
    Args:
        value: 제한할 값
        min_value: 최소값
        max_value: 최대값
        
    Returns:
        제한된 값
    """
    return max(min_value, min(value, max_value))


def map_range(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float,
    out_max: float
) -> float:
    """
    값을 한 범위에서 다른 범위로 매핑합니다.
    
    Args:
        value: 입력 값
        in_min: 입력 범위 최소값
        in_max: 입력 범위 최대값
        out_min: 출력 범위 최소값
        out_max: 출력 범위 최대값
        
    Returns:
        매핑된 값
    """
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)


class Timer:
    """
    쿨다운과 지연 액션을 위한 간단한 타이머 클래스
    
    Attributes:
        duration: 타이머 지속 시간 (초)
        time_left: 남은 시간 (초)
        running: 타이머가 활성화되었는지 여부
        loop: 자동으로 재시작할지 여부
    """
    
    def __init__(self, duration: float, autostart: bool = False, loop: bool = False):
        """
        타이머를 초기화합니다.
        
        Args:
            duration: 타이머 지속 시간 (초)
            autostart: 즉시 타이머 시작
            loop: 완료 시 자동으로 재시작
        """
        self.duration = duration
        self.time_left = duration if autostart else 0
        self.running = autostart
        self.loop = loop
    
    def start(self) -> None:
        """타이머를 시작하거나 재시작합니다."""
        self.time_left = self.duration
        self.running = True
    
    def stop(self) -> None:
        """타이머를 중지합니다."""
        self.running = False
        self.time_left = 0
    
    def pause(self) -> None:
        """타이머를 일시정지합니다."""
        self.running = False
    
    def resume(self) -> None:
        """타이머를 재개합니다."""
        if self.time_left > 0:
            self.running = True
    
    def update(self, dt: float) -> bool:
        """
        타이머를 업데이트합니다.
        
        Args:
            dt: 델타 타임 (초)
            
        Returns:
            이번 프레임에 타이머가 방금 완료되었으면 True
        """
        if not self.running:
            return False
        
        self.time_left -= dt
        
        if self.time_left <= 0:
            if self.loop:
                self.time_left = self.duration
                return True
            else:
                self.running = False
                self.time_left = 0
                return True
        
        return False
    
    def is_finished(self) -> bool:
        """
        타이머가 완료되었는지 확인합니다.
        
        Returns:
            타이머가 실행 중이지 않고 시간이 0이면 True
        """
        return not self.running and self.time_left == 0
    
    def is_running(self) -> bool:
        """
        타이머가 실행 중인지 확인합니다.
        
        Returns:
            타이머가 활성화되어 있으면 True
        """
        return self.running
    
    def get_progress(self) -> float:
        """
        타이머 진행도를 반환합니다 (0-1).
        
        Returns:
            진행도 값 (0 = 방금 시작, 1 = 완료)
        """
        if self.duration == 0:
            return 1.0
        return 1.0 - (self.time_left / self.duration)
    
    def get_time_left(self) -> float:
        """
        남은 시간을 초 단위로 반환합니다.
        
        Returns:
            남은 시간 (초)
        """
        return self.time_left


def point_in_rect(x: float, y: float, rect: pygame.Rect) -> bool:
    """
    점이 사각형 내부에 있는지 확인합니다.
    
    Args:
        x: 점의 x 좌표
        y: 점의 y 좌표
        rect: Pygame Rect
        
    Returns:
        점이 사각형 내부에 있으면 True
    """
    return rect.collidepoint(x, y)


def rects_overlap(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    두 사각형이 겹치는지 확인합니다.
    
    Args:
        rect1: 첫 번째 사각형
        rect2: 두 번째 사각형
        
    Returns:
        사각형이 겹치면 True
    """
    return rect1.colliderect(rect2)


# 모든 공개 함수와 클래스 내보내기
__all__ = [
    'Colors',
    'distance',
    'distance_squared',
    'angle_to',
    'angle_to_degrees',
    'normalize_vector',
    'lerp',
    'clamp',
    'map_range',
    'Timer',
    'point_in_rect',
    'rects_overlap',
]
