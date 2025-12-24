"""
애니메이션 컴포넌트 모듈

이 모듈은 프레임 기반 스프라이트 애니메이션 지원을 제공합니다.
"""

from typing import List, Optional
import pygame


class Animation:
    """
    프레임 기반 스프라이트 애니메이션을 위한 컴포넌트
    
    지원 기능:
    - 다중 애니메이션 프레임
    - 조정 가능한 재생 속도
    - 루프 및 원샷 모드
    - 애니메이션 상태 추적
    
    Attributes:
        entity: 부모 엔티티에 대한 참조
        frames: 애니메이션 프레임을 위한 pygame Surface 리스트
        frame_duration: 각 프레임의 지속 시간 (초 단위)
        loop: 애니메이션을 반복할지 여부
        current_frame: 현재 프레임 인덱스
        playing: 애니메이션이 현재 재생 중인지 여부
        finished: 원샷 애니메이션이 완료되었는지 여부
    """
    
    def __init__(
        self,
        frames: List[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True,
        autoplay: bool = True
    ):
        """
        애니메이션 컴포넌트를 초기화합니다.
        
        Args:
            frames: pygame Surface의 리스트 (애니메이션 프레임)
            frame_duration: 각 프레임의 지속 시간 (초 단위)
            loop: 애니메이션을 반복할지 여부
            autoplay: 자동으로 재생 시작
        """
        self.entity: Optional['Entity'] = None
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.playing = autoplay
        self.finished = False
        
        if not frames:
            raise ValueError("Animation must have at least one frame")
    
    def play(self) -> None:
        """애니메이션 재생을 시작하거나 재개합니다."""
        self.playing = True
        self.finished = False
    
    def stop(self) -> None:
        """애니메이션 재생을 중지합니다."""
        self.playing = False
    
    def reset(self) -> None:
        """애니메이션을 첫 프레임으로 리셋합니다."""
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.finished = False
    
    def restart(self) -> None:
        """리셋하고 애니메이션 재생을 시작합니다."""
        self.reset()
        self.play()
    
    def update(self, dt: float) -> None:
        """
        애니메이션 상태를 업데이트합니다.
        
        Args:
            dt: 델타 타임 (초 단위)
        """
        if not self.playing or self.finished:
            return
        
        self.time_accumulator += dt
        
        # 다음 프레임으로 진행해야 하는지 확인
        while self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame += 1
            
            # 애니메이션 종료 처리
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    self.playing = False
    
    def get_current_frame(self) -> pygame.Surface:
        """
        현재 애니메이션 프레임을 반환합니다.
        
        Returns:
            pygame Surface로서의 현재 프레임
        """
        return self.frames[self.current_frame]
    
    def set_frame(self, frame_index: int) -> None:
        """
        현재 프레임 인덱스를 설정합니다.
        
        Args:
            frame_index: 설정할 프레임 인덱스
        """
        self.current_frame = max(0, min(frame_index, len(self.frames) - 1))
    
    def is_finished(self) -> bool:
        """
        애니메이션이 완료되었는지 확인합니다 (원샷 애니메이션용).
        
        Returns:
            애니메이션이 완료되었으면 True
        """
        return self.finished
    
    def is_playing(self) -> bool:
        """
        애니메이션이 현재 재생 중인지 확인합니다.
        
        Returns:
            애니메이션이 재생 중이면 True
        """
        return self.playing
    
    def set_frame_duration(self, duration: float) -> None:
        """
        프레임 지속 시간(애니메이션 속도)을 변경합니다.
        
        Args:
            duration: 새로운 프레임 지속 시간 (초 단위)
        """
        self.frame_duration = max(0.001, duration)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        현재 애니메이션 프레임을 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        if not self.entity or not self.frames:
            return
        
        current_image = self.get_current_frame()
        
        # 엔티티 위치에 프레임을 중앙 배치하기 위한 위치 계산
        rect = current_image.get_rect()
        rect.center = (
            self.entity.position[0] + self.entity.size[0] / 2,
            self.entity.position[1] + self.entity.size[1] / 2
        )
        
        screen.blit(current_image, rect)


class AnimationController:
    """
    다중 명명된 애니메이션을 관리하기 위한 컨트롤러
    
    다양한 애니메이션 상태(예: idle, walk, jump) 간 전환을 허용합니다.
    """
    
    def __init__(self):
        """애니메이션 컨트롤러를 초기화합니다."""
        self.animations: dict = {}
        self.current_animation: Optional[str] = None
    
    def add_animation(self, name: str, animation: Animation) -> None:
        """
        명명된 애니메이션을 추가합니다.
        
        Args:
            name: 고유한 애니메이션 이름
            animation: Animation 인스턴스
        """
        self.animations[name] = animation
    
    def play_animation(self, name: str, restart: bool = False) -> None:
        """
        명명된 애니메이션을 재생합니다.
        
        Args:
            name: 재생할 애니메이션의 이름
            restart: 이미 이 애니메이션이 재생 중인 경우 재시작할지 여부
        """
        if name not in self.animations:
            return
        
        # 다른 경우 현재 애니메이션 중지
        if self.current_animation and self.current_animation != name:
            self.animations[self.current_animation].stop()
        
        # 새 애니메이션 재생
        if restart or self.current_animation != name:
            self.animations[name].restart()
        else:
            self.animations[name].play()
        
        self.current_animation = name
    
    def update(self, dt: float) -> None:
        """
        현재 애니메이션을 업데이트합니다.
        
        Args:
            dt: 델타 타임 (초 단위)
        """
        if self.current_animation:
            self.animations[self.current_animation].update(dt)
    
    def render(self, screen: pygame.Surface) -> None:
        """
        현재 애니메이션을 렌더링합니다.
        
        Args:
            screen: 렌더링할 Pygame 화면
        """
        if self.current_animation:
            self.animations[self.current_animation].render(screen)
    
    def get_current_animation(self) -> Optional[Animation]:
        """
        현재 재생 중인 애니메이션을 반환합니다.
        
        Returns:
            현재 Animation 인스턴스 또는 None
        """
        if self.current_animation:
            return self.animations.get(self.current_animation)
        return None
