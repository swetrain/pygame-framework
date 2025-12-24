"""
충돌 감지 모듈

이 모듈은 콜백 지원을 포함한 AABB 충돌 감지를 제공합니다.
"""

from typing import Optional, Callable, List, Set
import pygame


class CollisionComponent:
    """
    AABB (축 정렬 경계 상자) 충돌 감지를 위한 컴포넌트
    
    지원 기능:
    - 사각형 기반 충돌 감지
    - 충돌 콜백
    - 필터링을 위한 충돌 레이어/태그
    - 엔티티 위치로부터의 오프셋
    
    Attributes:
        entity: 부모 엔티티에 대한 참조
        offset: 엔티티 위치로부터의 오프셋 [x, y]
        size: 충돌 박스 크기 [너비, 높이] (None = 엔티티 크기 사용)
        on_collision: 충돌 이벤트를 위한 콜백 함수
        layer: 필터링을 위한 충돌 레이어
        collision_tags: 이 충돌체가 충돌할 수 있는 태그 세트
    """
    
    def __init__(
        self,
        offset: tuple = (0, 0),
        size: Optional[tuple] = None,
        on_collision: Optional[Callable] = None,
        layer: str = "default",
        collision_tags: Optional[Set[str]] = None
    ):
        """
        충돌 컴포넌트를 초기화합니다.
        
        Args:
            offset: 엔티티 위치로부터의 오프셋 (x, y)
            size: 충돌 박스 크기 (너비, 높이), 엔티티 크기를 사용하려면 None
            on_collision: 충돌 시 호출되는 콜백 함수(other_entity)
            layer: 충돌 레이어 이름
            collision_tags: 이 충돌체가 상호작용하는 태그 세트
        """
        self.entity: Optional['Entity'] = None
        self.offset = list(offset)
        self.size = list(size) if size else None
        self.on_collision = on_collision
        self.layer = layer
        self.collision_tags = collision_tags or set()
    
    def get_rect(self) -> pygame.Rect:
        """
        월드 공간에서 충돌 사각형을 반환합니다.
        
        Returns:
            충돌 감지를 위한 Pygame Rect
        """
        if not self.entity:
            return pygame.Rect(0, 0, 0, 0)
        
        # 사용자 정의 크기 또는 엔티티 크기 사용
        width, height = self.size if self.size else self.entity.size
        
        # 오프셋 적용
        x = self.entity.position[0] + self.offset[0]
        y = self.entity.position[1] + self.offset[1]
        
        return pygame.Rect(x, y, width, height)
    
    def check_collision(self, other: 'CollisionComponent') -> bool:
        """
        이 충돌체가 다른 충돌체와 교차하는지 확인합니다.
        
        Args:
            other: 확인할 다른 CollisionComponent
            
        Returns:
            충돌 중이면 True
        """
        # 레이어/태그 필터링 확인
        if self.collision_tags and other.layer not in self.collision_tags:
            return False
        
        # 사각형 교차 확인
        rect1 = self.get_rect()
        rect2 = other.get_rect()
        return rect1.colliderect(rect2)
    
    def check_collision_with_rect(self, rect: pygame.Rect) -> bool:
        """
        사각형과의 충돌을 확인합니다.
        
        Args:
            rect: 확인할 Pygame Rect
            
        Returns:
            충돌 중이면 True
        """
        return self.get_rect().colliderect(rect)
    
    def check_collision_with_point(self, x: float, y: float) -> bool:
        """
        점이 충돌 박스 내부에 있는지 확인합니다.
        
        Args:
            x: 점의 x 좌표
            y: 점의 y 좌표
            
        Returns:
            점이 내부에 있으면 True
        """
        return self.get_rect().collidepoint(x, y)
    
    def handle_collision(self, other_entity: 'Entity') -> None:
        """
        다른 엔티티와의 충돌을 처리합니다.
        
        설정된 경우 on_collision 콜백을 호출합니다.
        
        Args:
            other_entity: 충돌한 엔티티
        """
        if self.on_collision:
            self.on_collision(other_entity)
    
    def set_offset(self, x: float, y: float) -> None:
        """
        충돌 박스 오프셋을 설정합니다.
        
        Args:
            x: X 오프셋
            y: Y 오프셋
        """
        self.offset[0] = x
        self.offset[1] = y
    
    def set_size(self, width: float, height: float) -> None:
        """
        충돌 박스 크기를 설정합니다.
        
        Args:
            width: 박스 너비
            height: 박스 높이
        """
        self.size = [width, height]
    
    def add_collision_tag(self, tag: str) -> None:
        """
        이 충돌체가 충돌할 수 있는 태그를 추가합니다.
        
        Args:
            tag: 추가할 태그
        """
        self.collision_tags.add(tag)
    
    def remove_collision_tag(self, tag: str) -> None:
        """
        충돌 태그를 제거합니다.
        
        Args:
            tag: 제거할 태그
        """
        self.collision_tags.discard(tag)
    
    def debug_render(self, screen: pygame.Surface, color: tuple = (255, 0, 0)) -> None:
        """
        디버깅을 위해 충돌 박스를 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
            color: 충돌 박스를 그릴 색상
        """
        rect = self.get_rect()
        pygame.draw.rect(screen, color, rect, 2)


class CollisionSystem:
    """
    엔티티 간 충돌을 관리하고 확인하기 위한 시스템
    
    충돌 컴포넌트가 있는 엔티티 리스트를 유지하고
    충돌 감지를 수행합니다.
    """
    
    def __init__(self):
        """충돌 시스템을 초기화합니다."""
        self.entities: List['Entity'] = []
    
    def add_entity(self, entity: 'Entity') -> None:
        """
        충돌 확인에 엔티티를 추가합니다.
        
        Args:
            entity: 추적할 CollisionComponent가 있는 엔티티
        """
        if entity not in self.entities:
            self.entities.append(entity)
    
    def remove_entity(self, entity: 'Entity') -> None:
        """
        충돌 확인에서 엔티티를 제거합니다.
        
        Args:
            entity: 추적을 중지할 엔티티
        """
        if entity in self.entities:
            self.entities.remove(entity)
    
    def check_collisions(self) -> None:
        """등록된 모든 엔티티 간의 충돌을 확인합니다."""
        # 단순 O(n²) 충돌 감지
        # 많은 엔티티의 경우 더 나은 성능을 위해 공간 분할 사용
        for i, entity1 in enumerate(self.entities):
            if not entity1.active:
                continue
            
            collision1 = entity1.get_component('collision')
            if not collision1:
                continue
            
            for entity2 in self.entities[i + 1:]:
                if not entity2.active:
                    continue
                
                collision2 = entity2.get_component('collision')
                if not collision2:
                    continue
                
                if collision1.check_collision(collision2):
                    collision1.handle_collision(entity2)
                    collision2.handle_collision(entity1)
    
    def clear(self) -> None:
        """시스템에서 모든 엔티티를 제거합니다."""
        self.entities.clear()
