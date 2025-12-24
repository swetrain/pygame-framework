"""
버튼 UI 컴포넌트 모듈

이 모듈은 텍스트와 이미지 지원을 포함한 대화형 버튼 위젯을 제공합니다.
"""

from typing import Optional, Callable, Tuple
import pygame


class Button:
    """
    대화형 버튼 위젯
    
    지원 기능:
    - 텍스트 또는 이미지 버튼
    - 호버 및 클릭 상태
    - 콜백 함수
    - 사용자 정의 가능한 색상과 스타일
    
    Attributes:
        position: 버튼 위치 (x, y)
        size: 버튼 크기 (너비, 높이)
        text: 버튼 텍스트
        callback: 클릭 시 호출할 함수
        enabled: 버튼이 상호작용 가능한지 여부
        hovered: 마우스가 버튼 위에 있는지 여부
        pressed: 버튼이 현재 눌려있는지 여부
    """
    
    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[float, float],
        text: str = "",
        callback: Optional[Callable] = None,
        font_size: int = 24,
        text_color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        press_color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Optional[Tuple[int, int, int]] = None,
        border_width: int = 0,
        image: Optional[pygame.Surface] = None
    ):
        """
        버튼을 초기화합니다.
        
        Args:
            position: 버튼 위치 (x, y)
            size: 버튼 크기 (너비, 높이)
            text: 버튼 텍스트
            callback: 클릭 시 호출할 함수
            font_size: 텍스트 폰트 크기
            text_color: 버튼 텍스트 색상
            bg_color: 일반 배경 색상
            hover_color: 호버 시 배경 색상
            press_color: 눌렸을 때 배경 색상
            border_color: 테두리 색상 (테두리 없음은 None)
            border_width: 테두리 너비 (픽셀)
            image: 텍스트 대신 표시할 선택적 이미지
        """
        self.position = list(position)
        self.size = list(size)
        self.text = text
        self.callback = callback
        
        # 시각적 속성
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.press_color = press_color
        self.border_color = border_color
        self.border_width = border_width
        self.image = image
        
        # 상태
        self.enabled = True
        self.hovered = False
        self.pressed = False
        
        # 텍스트 사용 시 폰트 생성
        if text and not image:
            self.font = pygame.font.Font(None, font_size)
            self.text_surface = self.font.render(text, True, text_color)
        else:
            self.font = None
            self.text_surface = None
    
    def get_rect(self) -> pygame.Rect:
        """
        버튼 경계 사각형을 반환합니다.
        
        Returns:
            버튼을 위한 Pygame Rect
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1]
        )
    
    def update(self, events: list) -> None:
        """
        이벤트를 기반으로 버튼 상태를 업데이트합니다.
        
        Args:
            events: pygame 이벤트 리스트
        """
        if not self.enabled:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        rect = self.get_rect()
        
        # 호버 상태 확인
        self.hovered = rect.collidepoint(mouse_pos)
        
        # 클릭 확인
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.pressed and self.hovered:
                    # 버튼이 클릭됨
                    if self.callback:
                        self.callback()
                self.pressed = False
    
    def render(self, screen: pygame.Surface) -> None:
        """
        버튼을 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        rect = self.get_rect()
        
        # 상태에 따라 배경 색상 결정
        if not self.enabled:
            bg_color = (80, 80, 80)
        elif self.pressed:
            bg_color = self.press_color
        elif self.hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.bg_color
        
        # 배경 그리기
        pygame.draw.rect(screen, bg_color, rect)
        
        # 테두리 그리기
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, rect, self.border_width)
        
        # 이미지 또는 텍스트 그리기
        if self.image:
            # 버튼에 이미지 중앙 배치
            image_rect = self.image.get_rect()
            image_rect.center = rect.center
            screen.blit(self.image, image_rect)
        elif self.text_surface:
            # 버튼에 텍스트 중앙 배치
            text_rect = self.text_surface.get_rect()
            text_rect.center = rect.center
            screen.blit(self.text_surface, text_rect)
    
    def set_text(self, text: str) -> None:
        """
        버튼 텍스트를 변경합니다.
        
        Args:
            text: 새로운 버튼 텍스트
        """
        self.text = text
        if self.font:
            self.text_surface = self.font.render(text, True, self.text_color)
    
    def set_enabled(self, enabled: bool) -> None:
        """
        버튼을 활성화하거나 비활성화합니다.
        
        Args:
            enabled: 활성화하려면 True, 비활성화하려면 False
        """
        self.enabled = enabled
    
    def set_callback(self, callback: Callable) -> None:
        """
        버튼 클릭 콜백을 설정합니다.
        
        Args:
            callback: 클릭 시 호출할 함수
        """
        self.callback = callback
    
    def set_position(self, x: float, y: float) -> None:
        """
        버튼 위치를 설정합니다.
        
        Args:
            x: X 좌표
            y: Y 좌표
        """
        self.position[0] = x
        self.position[1] = y
    
    def set_size(self, width: float, height: float) -> None:
        """
        버튼 크기를 설정합니다.
        
        Args:
            width: 버튼 너비
            height: 버튼 높이
        """
        self.size[0] = width
        self.size[1] = height
    
    def is_hovered(self) -> bool:
        """
        버튼이 호버 상태인지 확인합니다.
        
        Returns:
            마우스가 버튼 위에 있으면 True
        """
        return self.hovered
    
    def is_pressed(self) -> bool:
        """
        버튼이 눌려있는지 확인합니다.
        
        Returns:
            버튼이 현재 눌려있으면 True
        """
        return self.pressed
