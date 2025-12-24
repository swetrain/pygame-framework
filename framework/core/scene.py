"""
씬 시스템 모듈

이 모듈은 다양한 게임 상태와 전환을 처리하기 위한
Scene 기본 클래스와 SceneManager를 제공합니다.
"""

from typing import Dict, List, Optional
import pygame


class Scene:
    """
    모든 게임 씬의 기본 클래스
    
    씬은 특정 게임 상태를 나타냅니다 (예: 메뉴, 게임플레이, 게임 오버).
    서브클래스는 메서드를 오버라이드하여 특정 동작을 구현해야 합니다.
    
    Attributes:
        name: 이 씬의 고유 식별자
        game: 메인 게임 인스턴스에 대한 참조
    """
    
    def __init__(self, name: str, game: Optional['Game'] = None):
        """
        씬을 초기화합니다.
        
        Args:
            name: 고유한 씬 식별자
            game: 메인 Game 인스턴스에 대한 참조
        """
        self.name = name
        self.game = game
    
    def on_enter(self) -> None:
        """
        이 씬에 진입할 때 호출됩니다.
        
        씬 전용 리소스를 초기화하거나, 상태를 재설정하거나,
        배경 음악을 시작하려면 이 메서드를 오버라이드하세요.
        """
        pass
    
    def on_exit(self) -> None:
        """
        이 씬을 나갈 때 호출됩니다.
        
        리소스를 정리하거나 상태를 저장하려면 이 메서드를 오버라이드하세요.
        """
        pass
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        이 씬의 pygame 이벤트를 처리합니다.
        
        Args:
            events: 처리할 pygame 이벤트 리스트
        """
        pass
    
    def update(self, dt: float) -> None:
        """
        씬 로직을 업데이트합니다.
        
        Args:
            dt: 지난 프레임 이후의 델타 타임 (초 단위)
        """
        pass
    
    def render(self, screen: pygame.Surface) -> None:
        """
        씬을 화면에 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        pass


class SceneManager:
    """
    씬 전환과 씬 스택을 관리하는 매니저
    
    SceneManager는 씬 간 전환을 처리하고
    푸시/팝 씬 작업(예: 일시정지 메뉴)을 위한 스택을 유지합니다.
    
    Attributes:
        scenes: 씬 이름을 Scene 인스턴스에 매핑하는 딕셔너리
        scene_stack: 활성 씬의 스택
        current_scene: 현재 활성 씬 (스택의 최상위)
    """
    
    def __init__(self):
        """씬 매니저를 초기화합니다."""
        self.scenes: Dict[str, Scene] = {}
        self.scene_stack: List[Scene] = []
        self.current_scene: Optional[Scene] = None
    
    def add_scene(self, scene: Scene) -> None:
        """
        매니저에 씬을 등록합니다.
        
        Args:
            scene: 등록할 Scene 인스턴스
        """
        self.scenes[scene.name] = scene
    
    def remove_scene(self, scene_name: str) -> None:
        """
        매니저에서 씬을 제거합니다.
        
        Args:
            scene_name: 제거할 씬의 이름
        """
        if scene_name in self.scenes:
            del self.scenes[scene_name]
    
    def change_scene(self, scene_name: str) -> None:
        """
        다른 씬으로 전환하여 현재 씬을 대체합니다.
        
        Args:
            scene_name: 전환할 씬의 이름
            
        Raises:
            KeyError: 씬 이름이 등록되지 않은 경우
        """
        if scene_name not in self.scenes:
            raise KeyError(f"Scene '{scene_name}' not found")
        
        # Exit current scene
        if self.current_scene:
            self.current_scene.on_exit()
        
        # 스택을 비우고 새 씬 설정
        self.scene_stack.clear()
        self.current_scene = self.scenes[scene_name]
        self.scene_stack.append(self.current_scene)
        
        # 새 씬 진입
        self.current_scene.on_enter()
    
    def push_scene(self, scene_name: str) -> None:
        """
        현재 씬을 종료하지 않고 스택에 씬을 푸시합니다.
        
        일시정지 메뉴와 같은 오버레이에 유용합니다.
        
        Args:
            scene_name: 푸시할 씬의 이름
            
        Raises:
            KeyError: 씬 이름이 등록되지 않은 경우
        """
        if scene_name not in self.scenes:
            raise KeyError(f"Scene '{scene_name}' not found")
        
        scene = self.scenes[scene_name]
        self.scene_stack.append(scene)
        self.current_scene = scene
        self.current_scene.on_enter()
    
    def pop_scene(self) -> None:
        """
        스택에서 현재 씬을 팝하고 이전 씬으로 돌아갑니다.
        
        Raises:
            IndexError: 스택에 씬이 하나만 있는 경우
        """
        if len(self.scene_stack) <= 1:
            raise IndexError("Cannot pop the last scene")
        
        # Exit current scene
        if self.current_scene:
            self.current_scene.on_exit()
        
        # 팝하고 이전 씬을 현재 씬으로 설정
        self.scene_stack.pop()
        self.current_scene = self.scene_stack[-1]
    
    def get_scene(self, scene_name: str) -> Optional[Scene]:
        """
        이름으로 등록된 씬을 가져옵니다.
        
        Args:
            scene_name: 가져올 씬의 이름
            
        Returns:
            Scene 인스턴스 또는 찾지 못한 경우 None
        """
        return self.scenes.get(scene_name)
