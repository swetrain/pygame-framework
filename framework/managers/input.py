"""
입력 관리 모듈

이 모듈은 상태 추적과 입력 매핑 지원을 포함한
키보드와 마우스의 중앙집중식 입력 처리를 제공합니다.
"""

from typing import Dict, Set, Tuple, Optional
import pygame


class InputManager:
    """
    키보드와 마우스 입력 처리를 위한 매니저
    
    이 매니저는 다음을 추적합니다:
    - 키 상태 (눌림, 홀드, 해제)
    - 마우스 위치와 버튼 상태
    - 입력 액션 매핑 (예: "점프" -> SPACE 키)
    
    Attributes:
        keys_pressed: 이번 프레임에 눌린 키 세트
        keys_held: 현재 눌려있는 키 세트
        keys_released: 이번 프레임에 해제된 키 세트
        mouse_pos: 현재 마우스 위치 (x, y)
        mouse_buttons: 마우스 버튼 상태 딕셔너리
        action_map: 액션 이름을 키에 매핑하는 딕셔너리
    """
    
    def __init__(self):
        """입력 매니저를 초기화합니다."""
        self.keys_pressed: Set[int] = set()
        self.keys_held: Set[int] = set()
        self.keys_released: Set[int] = set()
        
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_buttons: Dict[int, bool] = {}
        self.mouse_pressed: Set[int] = set()
        self.mouse_released: Set[int] = set()
        
        self.action_map: Dict[str, int] = {}
    
    def update(self, events: list) -> None:
        """
        pygame 이벤트를 기반으로 입력 상태를 업데이트합니다.
        
        이벤트 리스트와 함께 프레임당 한 번 호출되어야 합니다.
        
        Args:
            events: pygame.event.get()의 pygame 이벤트 리스트
        """
        # 프레임별 상태 초기화
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_pressed.clear()
        self.mouse_released.clear()
        
        # 이벤트 처리
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_held.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_released.add(event.key)
                self.keys_held.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed.add(event.button)
                self.mouse_buttons[event.button] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_released.add(event.button)
                self.mouse_buttons[event.button] = False
        
        # 마우스 위치 업데이트
        self.mouse_pos = pygame.mouse.get_pos()
    
    def is_key_pressed(self, key: int) -> bool:
        """
        이번 프레임에 키가 방금 눌렸는지 확인합니다.
        
        Args:
            key: Pygame 키 상수 (예: pygame.K_SPACE)
            
        Returns:
            이번 프레임에 키가 눌렸으면 True
        """
        return key in self.keys_pressed
    
    def is_key_held(self, key: int) -> bool:
        """
        키가 현재 눌려있는지 확인합니다.
        
        Args:
            key: Pygame 키 상수
            
        Returns:
            키가 현재 눌려있으면 True
        """
        return key in self.keys_held
    
    def is_key_released(self, key: int) -> bool:
        """
        이번 프레임에 키가 방금 해제되었는지 확인합니다.
        
        Args:
            key: Pygame 키 상수
            
        Returns:
            이번 프레임에 키가 해제되었으면 True
        """
        return key in self.keys_released
    
    def is_mouse_button_pressed(self, button: int) -> bool:
        """
        이번 프레임에 마우스 버튼이 방금 눌렸는지 확인합니다.
        
        Args:
            button: 마우스 버튼 번호 (1=왼쪽, 2=가운데, 3=오른쪽)
            
        Returns:
            이번 프레임에 버튼이 눌렸으면 True
        """
        return button in self.mouse_pressed
    
    def is_mouse_button_held(self, button: int) -> bool:
        """
        마우스 버튼이 현재 눌려있는지 확인합니다.
        
        Args:
            button: 마우스 버튼 번호
            
        Returns:
            버튼이 현재 눌려있으면 True
        """
        return self.mouse_buttons.get(button, False)
    
    def is_mouse_button_released(self, button: int) -> bool:
        """
        이번 프레임에 마우스 버튼이 방금 해제되었는지 확인합니다.
        
        Args:
            button: 마우스 버튼 번호
            
        Returns:
            이번 프레임에 버튼이 해제되었으면 True
        """
        return button in self.mouse_released
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """
        현재 마우스 위치를 반환합니다.
        
        Returns:
            (x, y) 좌표의 튜플
        """
        return self.mouse_pos
    
    def map_action(self, action_name: str, key: int) -> None:
        """
        액션 이름을 키에 매핑합니다.
        
        이를 통해 키 코드 대신 의미있는 액션 이름을 사용할 수 있습니다.
        
        Args:
            action_name: 액션의 이름 (예: "jump", "fire")
            key: 이 액션에 매핑할 Pygame 키 상수
        """
        self.action_map[action_name] = key
    
    def is_action_pressed(self, action_name: str) -> bool:
        """
        매핑된 액션이 이번 프레임에 눌렸는지 확인합니다.
        
        Args:
            action_name: 액션의 이름
            
        Returns:
            액션의 키가 이번 프레임에 눌렸으면 True
        """
        key = self.action_map.get(action_name)
        if key is None:
            return False
        return self.is_key_pressed(key)
    
    def is_action_held(self, action_name: str) -> bool:
        """
        매핑된 액션이 현재 눌려있는지 확인합니다.
        
        Args:
            action_name: 액션의 이름
            
        Returns:
            액션의 키가 현재 눌려있으면 True
        """
        key = self.action_map.get(action_name)
        if key is None:
            return False
        return self.is_key_held(key)
    
    def is_action_released(self, action_name: str) -> bool:
        """
        매핑된 액션이 이번 프레임에 해제되었는지 확인합니다.
        
        Args:
            action_name: 액션의 이름
            
        Returns:
            액션의 키가 이번 프레임에 해제되었으면 True
        """
        key = self.action_map.get(action_name)
        if key is None:
            return False
        return self.is_key_released(key)
    
    def clear_action_map(self) -> None:
        """모든 액션 매핑을 지웁니다."""
        self.action_map.clear()
    
    def get_axis(self, negative_key: int, positive_key: int) -> float:
        """
        두 키에서 축 값을 가져옵니다 (예: 이동용).
        
        Args:
            negative_key: 음수 방향 키 (-1)
            positive_key: 양수 방향 키 (+1)
            
        Returns:
            -1과 1 사이의 값
        """
        value = 0.0
        if self.is_key_held(negative_key):
            value -= 1.0
        if self.is_key_held(positive_key):
            value += 1.0
        return value
