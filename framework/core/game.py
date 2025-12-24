"""
메인 게임 엔진 모듈

이 모듈은 게임 루프, 화면 초기화, 씬 관리를 담당하는
핵심 Game 클래스를 제공합니다.
"""

from typing import Optional, Tuple
import pygame
from framework.core.scene import SceneManager


class Game:
    """
    초기화와 게임 루프를 처리하는 메인 게임 엔진 클래스
    
    이 클래스는 다음을 관리합니다:
    - 창 초기화
    - 게임 루프 (이벤트, 업데이트, 렌더링)
    - FPS 제한과 델타 타임 계산
    - 씬 관리 통합
    
    Attributes:
        screen_size: 게임 창의 (너비, 높이) 튜플
        title: 창 제목
        fps: 목표 프레임 속도
        screen: Pygame 디스플레이 화면
        clock: FPS 관리를 위한 Pygame Clock
        scene_manager: 씬 전환을 위한 SceneManager 인스턴스
        running: 게임 루프가 활성화되었는지 나타내는 플래그
        dt: 지난 프레임 이후의 델타 타임 (초 단위)
    """
    
    def __init__(
        self,
        screen_size: Tuple[int, int] = (800, 600),
        title: str = "Pygame Framework Game",
        fps: int = 60,
        flags: int = 0
    ):
        """
        게임 엔진을 초기화합니다.
        
        Args:
            screen_size: 창 크기 (너비, 높이)
            title: 창 제목
            fps: 목표 프레임 속도
            flags: Pygame 디스플레이 플래그 (예: pygame.FULLSCREEN)
        """
        self.screen_size = screen_size
        self.title = title
        self.fps = fps
        self.flags = flags
        
        # Pygame 초기화
        pygame.init()
        
        # 디스플레이 생성
        self.screen = pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption(title)
        
        # FPS 관리를 위한 Clock 생성
        self.clock = pygame.time.Clock()
        
        # 씬 관리
        self.scene_manager = SceneManager()
        
        # 게임 상태
        self.running = False
        self.dt = 0.0
    
    def run(self) -> None:
        """
        메인 게임 루프를 시작합니다.
        
        게임 루프는 다음을 처리합니다:
        1. 이벤트 처리
        2. 씬 업데이트
        3. 씬 렌더링
        4. FPS 제한과 델타 타임 계산
        """
        self.running = True
        
        while self.running:
            # 델타 타임 계산 (초 단위)
            self.dt = self.clock.tick(self.fps) / 1000.0
            
            # 이벤트 처리
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # 현재 씬 업데이트
            if self.scene_manager.current_scene:
                self.scene_manager.current_scene.handle_events(events)
                self.scene_manager.current_scene.update(self.dt)
            
            # 현재 씬 렌더링
            self.screen.fill((0, 0, 0))  # 화면을 검은색으로 초기화
            if self.scene_manager.current_scene:
                self.scene_manager.current_scene.render(self.screen)
            
            # 디스플레이 업데이트
            pygame.display.flip()
        
        # 정리
        self.quit()
    
    def quit(self) -> None:
        """리소스를 정리하고 pygame을 종료합니다."""
        pygame.quit()
    
    def set_scene(self, scene_name: str) -> None:
        """
        다른 씬으로 전환합니다.
        
        Args:
            scene_name: 전환할 씬의 이름
        """
        self.scene_manager.change_scene(scene_name)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        현재 화면 크기를 반환합니다.
        
        Returns:
            (너비, 높이) 튜플
        """
        return self.screen_size
    
    def get_fps(self) -> float:
        """
        현재 프레임 속도를 반환합니다.
        
        Returns:
            현재 FPS (float 타입)
        """
        return self.clock.get_fps()
