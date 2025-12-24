"""
텍스트 UI 컴포넌트 모듈

이 모듈은 정렬과 스타일링 옵션을 포함한 텍스트 렌더링을 제공합니다.
"""

from typing import Tuple, Optional
import pygame


class Text:
    """
    텍스트 렌더링 컴포넌트
    
    지원 기능:
    - 사용자 정의 폰트, 크기, 색상
    - 텍스트 정렬 (왼쪽, 중앙, 오른쪽)
    - 안티앨리어싱
    - 배경 색상
    
    Attributes:
        text: 렌더링할 텍스트 문자열
        position: 렌더링할 위치 (x, y)
        font: Pygame 폰트 객체
        color: 텍스트 색상
        antialias: 안티앨리어싱 사용 여부
        alignment: 텍스트 정렬 ("left", "center", "right")
        surface: 캐시된 텍스트 표면
    """
    
    def __init__(
        self,
        text: str,
        position: Tuple[float, float],
        font_size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        font_path: Optional[str] = None,
        antialias: bool = True,
        alignment: str = "left",
        bg_color: Optional[Tuple[int, int, int]] = None
    ):
        """
        텍스트 컴포넌트를 초기화합니다.
        
        Args:
            text: 표시할 텍스트 문자열
            position: 렌더링할 위치 (x, y)
            font_size: 포인트 단위 폰트 크기
            color: 텍스트 색상 RGB 튜플
            font_path: 사용자 정의 폰트 파일 경로 (기본값은 None)
            antialias: 안티앨리어싱 사용 여부
            alignment: 텍스트 정렬 ("left", "center", "right")
            bg_color: 선택적 배경 색상
        """
        self.text = text
        self.position = list(position)
        self.color = color
        self.antialias = antialias
        self.alignment = alignment
        self.bg_color = bg_color
        
        # 폰트 로드
        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)
        
        # 텍스트 표면 렌더링
        self._render_text()
    
    def _render_text(self) -> None:
        """텍스트를 표면에 렌더링합니다."""
        if self.bg_color:
            self.surface = self.font.render(
                self.text,
                self.antialias,
                self.color,
                self.bg_color
            )
        else:
            self.surface = self.font.render(
                self.text,
                self.antialias,
                self.color
            )
    
    def set_text(self, text: str) -> None:
        """
        텍스트 문자열을 변경합니다.
        
        Args:
            text: 표시할 새로운 텍스트
        """
        if self.text != text:
            self.text = text
            self._render_text()
    
    def set_color(self, color: Tuple[int, int, int]) -> None:
        """
        텍스트 색상을 변경합니다.
        
        Args:
            color: 새로운 RGB 색상 튜플
        """
        if self.color != color:
            self.color = color
            self._render_text()
    
    def set_position(self, x: float, y: float) -> None:
        """
        텍스트 위치를 변경합니다.
        
        Args:
            x: X 좌표
            y: Y 좌표
        """
        self.position[0] = x
        self.position[1] = y
    
    def get_position(self) -> Tuple[float, float]:
        """
        텍스트 위치를 반환합니다.
        
        Returns:
            (x, y) 좌표의 튜플
        """
        return tuple(self.position)
    
    def get_size(self) -> Tuple[int, int]:
        """
        렌더링된 텍스트 크기를 반환합니다.
        
        Returns:
            (너비, 높이)의 튜플
        """
        return self.surface.get_size()
    
    def get_rect(self) -> pygame.Rect:
        """
        텍스트 경계 사각형을 반환합니다.
        
        Returns:
            텍스트를 위한 Pygame Rect
        """
        rect = self.surface.get_rect()
        
        # 정렬 적용
        if self.alignment == "left":
            rect.topleft = self.position
        elif self.alignment == "center":
            rect.center = self.position
        elif self.alignment == "right":
            rect.topright = self.position
        else:
            rect.topleft = self.position
        
        return rect
    
    def render(self, screen: pygame.Surface) -> None:
        """
        텍스트를 화면에 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        rect = self.get_rect()
        screen.blit(self.surface, rect)
    
    def set_alignment(self, alignment: str) -> None:
        """
        텍스트 정렬을 설정합니다.
        
        Args:
            alignment: 정렬 모드 ("left", "center", "right")
        """
        if alignment in ["left", "center", "right"]:
            self.alignment = alignment


class TextBox:
    """
    단어 줄바꿈이 있는 다중 라인 텍스트 박스
    
    대화나 지시사항과 같은 긴 텍스트를 표시하는 데 유용합니다.
    """
    
    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        font_size: int = 20,
        color: Tuple[int, int, int] = (255, 255, 255),
        bg_color: Optional[Tuple[int, int, int]] = None,
        padding: int = 10,
        line_spacing: int = 5
    ):
        """
        텍스트 박스를 초기화합니다.
        
        Args:
            text: 텍스트 내용
            rect: 텍스트 박스의 경계 사각형
            font_size: 포인트 단위 폰트 크기
            color: 텍스트 색상
            bg_color: 선택적 배경 색상
            padding: 가장자리로부터의 패딩
            line_spacing: 라인 간 간격
        """
        self.text = text
        self.rect = rect
        self.color = color
        self.bg_color = bg_color
        self.padding = padding
        self.line_spacing = line_spacing
        
        self.font = pygame.font.Font(None, font_size)
        self.lines = self._wrap_text()
    
    def _wrap_text(self) -> list:
        """
        박스 너비에 맞도록 텍스트를 줄바꿈합니다.
        
        Returns:
            텍스트 라인 리스트
        """
        words = self.text.split(' ')
        lines = []
        current_line = []
        
        max_width = self.rect.width - 2 * self.padding
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, self.color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def set_text(self, text: str) -> None:
        """
        텍스트 내용을 변경합니다.
        
        Args:
            text: 표시할 새로운 텍스트
        """
        self.text = text
        self.lines = self._wrap_text()
    
    def render(self, screen: pygame.Surface) -> None:
        """
        텍스트 박스를 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        # 배경 그리기
        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # 텍스트 라인 그리기
        y = self.rect.y + self.padding
        for line in self.lines:
            text_surface = self.font.render(line, True, self.color)
            screen.blit(text_surface, (self.rect.x + self.padding, y))
            y += text_surface.get_height() + self.line_spacing
