"""
엔티티 시스템 모듈

이 모듈은 컴포넌트 기반 아키텍처를 사용하는 게임 오브젝트를 위한
기본 Entity 클래스를 제공합니다.
"""

from typing import Dict, List, Optional, Tuple, Any
import pygame


class Entity:
    """
    모든 게임 엔티티/오브젝트의 기본 클래스
    
    엔티티는 모든 게임 오브젝트(플레이어, 적, 아이템 등)를 나타내며
    유연한 동작을 위한 컴포넌트 기반 아키텍처를 지원합니다.
    
    Attributes:
        position: 월드 공간에서의 (x, y) 위치
        size: (너비, 높이) 크기
        active: 엔티티를 업데이트하고 렌더링할지 여부
        components: 연결된 컴포넌트의 딕셔너리
        tags: 식별을 위한 문자열 태그 세트
    """
    
    def __init__(
        self,
        position: Tuple[float, float] = (0, 0),
        size: Tuple[float, float] = (32, 32)
    ):
        """
        엔티티를 초기화합니다.
        
        Args:
            position: 초기 (x, y) 위치
            size: 초기 (너비, 높이) 크기
        """
        self.position = list(position)  # [x, y]
        self.size = list(size)  # [width, height]
        self.active = True
        self.components: Dict[str, Any] = {}
        self.tags: set = set()
    
    def add_component(self, name: str, component: Any) -> None:
        """
        이 엔티티에 컴포넌트를 추가합니다.
        
        Args:
            name: 컴포넌트의 고유 식별자
            component: 연결할 컴포넌트 인스턴스
        """
        self.components[name] = component
        
        # 컴포넌트에 속성이 있으면 엔티티 참조를 설정
        if hasattr(component, 'entity'):
            component.entity = self
    
    def get_component(self, name: str) -> Optional[Any]:
        """
        이름으로 컴포넌트를 가져옵니다.
        
        Args:
            name: 컴포넌트 식별자
            
        Returns:
            컴포넌트 인스턴스 또는 찾지 못한 경우 None
        """
        return self.components.get(name)
    
    def remove_component(self, name: str) -> None:
        """
        이 엔티티에서 컴포넌트를 제거합니다.
        
        Args:
            name: 제거할 컴포넌트 식별자
        """
        if name in self.components:
            del self.components[name]
    
    def has_component(self, name: str) -> bool:
        """
        엔티티가 특정 컴포넌트를 가지고 있는지 확인합니다.
        
        Args:
            name: 컴포넌트 식별자
            
        Returns:
            컴포넌트가 존재하면 True, 그렇지 않으면 False
        """
        return name in self.components
    
    def add_tag(self, tag: str) -> None:
        """
        식별을 위해 이 엔티티에 태그를 추가합니다.
        
        Args:
            tag: 추가할 태그 문자열
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag: str) -> None:
        """
        이 엔티티에서 태그를 제거합니다.
        
        Args:
            tag: 제거할 태그 문자열
        """
        self.tags.discard(tag)
    
    def has_tag(self, tag: str) -> bool:
        """
        엔티티가 특정 태그를 가지고 있는지 확인합니다.
        
        Args:
            tag: 확인할 태그 문자열
            
        Returns:
            엔티티가 태그를 가지고 있으면 True, 그렇지 않으면 False
        """
        return tag in self.tags
    
    def update(self, dt: float) -> None:
        """
        엔티티 로직과 모든 컴포넌트를 업데이트합니다.
        
        Args:
            dt: 지난 프레임 이후의 델타 타임 (초 단위)
        """
        if not self.active:
            return
        
        # update 메서드가 있는 모든 컴포넌트 업데이트
        for component in self.components.values():
            if hasattr(component, 'update'):
                component.update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        엔티티와 모든 컴포넌트를 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        if not self.active:
            return
        
        # render 메서드가 있는 모든 컴포넌트 렌더링
        for component in self.components.values():
            if hasattr(component, 'render'):
                component.render(screen)
    
    def get_rect(self) -> pygame.Rect:
        """
        이 엔티티의 경계 사각형을 반환합니다.
        
        Returns:
            엔티티 경계를 나타내는 Pygame Rect
        """
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1]
        )
    
    def set_position(self, x: float, y: float) -> None:
        """
        엔티티 위치를 설정합니다.
        
        Args:
            x: X 좌표
            y: Y 좌표
        """
        self.position[0] = x
        self.position[1] = y
    
    def get_position(self) -> Tuple[float, float]:
        """
        엔티티 위치를 반환합니다.
        
        Returns:
            (x, y) 좌표의 튜플
        """
        return tuple(self.position)
    
    def set_size(self, width: float, height: float) -> None:
        """
        엔티티 크기를 설정합니다.
        
        Args:
            width: 엔티티 너비
            height: 엔티티 높이
        """
        self.size[0] = width
        self.size[1] = height
    
    def get_size(self) -> Tuple[float, float]:
        """
        엔티티 크기를 반환합니다.
        
        Returns:
            (너비, 높이)의 튜플
        """
        return tuple(self.size)
    
    def set_active(self, active: bool) -> None:
        """
        엔티티 활성 상태를 설정합니다.
        
        Args:
            active: 활성화하려면 True, 비활성화하려면 False
        """
        self.active = active
    
    def is_active(self) -> bool:
        """
        엔티티가 활성 상태인지 확인합니다.
        
        Returns:
            활성 상태이면 True, 그렇지 않으면 False
        """
        return self.active
