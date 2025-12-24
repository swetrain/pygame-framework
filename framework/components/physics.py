"""
물리 컴포넌트 모듈

이 모듈은 속도, 가속도, 중력을 포함한
엔티티를 위한 물리 시뮬레이션을 제공합니다.
"""

from typing import Optional, Tuple
import pygame


class PhysicsComponent:
    """
    물리 시뮬레이션을 위한 컴포넌트
    
    처리 기능:
    - 속도와 가속도
    - 중력 시뮬레이션
    - 최대 속도 제한
    - 저항/마찰
    
    Attributes:
        entity: 부모 엔티티에 대한 참조
        velocity: 현재 속도 [x, y]
        acceleration: 현재 가속도 [x, y]
        gravity: 중력 (양수 = 아래 방향)
        max_velocity: 최대 속도 제한 [x, y]
        drag: 저항 계수 (0-1, 1 = 저항 없음)
        use_gravity: 중력을 적용할지 여부
    """
    
    def __init__(
        self,
        velocity: Tuple[float, float] = (0, 0),
        acceleration: Tuple[float, float] = (0, 0),
        gravity: float = 0,
        max_velocity: Tuple[float, float] = (1000, 1000),
        drag: float = 1.0,
        use_gravity: bool = True
    ):
        """
        물리 컴포넌트를 초기화합니다.
        
        Args:
            velocity: 초기 속도 (x, y)
            acceleration: 일정한 가속도 (x, y)
            gravity: 중력 가속도 (양수 = 아래)
            max_velocity: 최대 속도 제한 (x, y)
            drag: 저항 계수 (0-1, 1 = 저항 없음)
            use_gravity: 중력을 적용할지 여부
        """
        self.entity: Optional['Entity'] = None
        self.velocity = list(velocity)
        self.acceleration = list(acceleration)
        self.gravity = gravity
        self.max_velocity = list(max_velocity)
        self.drag = drag
        self.use_gravity = use_gravity
    
    def apply_force(self, force_x: float, force_y: float) -> None:
        """
        속도에 순간적인 힘을 적용합니다.
        
        Args:
            force_x: x 방향의 힘
            force_y: y 방향의 힘
        """
        self.velocity[0] += force_x
        self.velocity[1] += force_y
    
    def set_velocity(self, vx: float, vy: float) -> None:
        """
        속도를 직접 설정합니다.
        
        Args:
            vx: X 속도
            vy: Y 속도
        """
        self.velocity[0] = vx
        self.velocity[1] = vy
    
    def get_velocity(self) -> Tuple[float, float]:
        """
        현재 속도를 반환합니다.
        
        Returns:
            (vx, vy)의 튜플
        """
        return tuple(self.velocity)
    
    def set_acceleration(self, ax: float, ay: float) -> None:
        """
        가속도를 설정합니다.
        
        Args:
            ax: X 가속도
            ay: Y 가속도
        """
        self.acceleration[0] = ax
        self.acceleration[1] = ay
    
    def get_acceleration(self) -> Tuple[float, float]:
        """
        현재 가속도를 반환합니다.
        
        Returns:
            (ax, ay)의 튜플
        """
        return tuple(self.acceleration)
    
    def update(self, dt: float) -> None:
        """
        물리 시뮬레이션을 업데이트합니다.
        
        Args:
            dt: 델타 타임 (초 단위)
        """
        if not self.entity:
            return
        
        # 가속도 적용
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        
        # 중력 적용
        if self.use_gravity:
            self.velocity[1] += self.gravity * dt
        
        # 저항 적용
        if self.drag < 1.0:
            self.velocity[0] *= self.drag
            self.velocity[1] *= self.drag
        
        # 최대 속도로 제한
        if abs(self.velocity[0]) > self.max_velocity[0]:
            self.velocity[0] = self.max_velocity[0] if self.velocity[0] > 0 else -self.max_velocity[0]
        if abs(self.velocity[1]) > self.max_velocity[1]:
            self.velocity[1] = self.max_velocity[1] if self.velocity[1] > 0 else -self.max_velocity[1]
        
        # 엔티티 위치 업데이트
        self.entity.position[0] += self.velocity[0] * dt
        self.entity.position[1] += self.velocity[1] * dt
    
    def stop(self) -> None:
        """모든 움직임을 중지합니다 (속도를 0으로 설정)."""
        self.velocity = [0, 0]
    
    def is_moving(self) -> bool:
        """
        엔티티가 움직이고 있는지 확인합니다.
        
        Returns:
            속도가 0이 아니면 True
        """
        return self.velocity[0] != 0 or self.velocity[1] != 0
    
    def set_gravity(self, gravity: float) -> None:
        """
        중력을 설정합니다.
        
        Args:
            gravity: 중력 가속도 (양수 = 아래)
        """
        self.gravity = gravity
    
    def enable_gravity(self, enabled: bool = True) -> None:
        """
        중력을 활성화하거나 비활성화합니다.
        
        Args:
            enabled: 중력을 활성화하려면 True
        """
        self.use_gravity = enabled
    
    def set_max_velocity(self, max_x: float, max_y: float) -> None:
        """
        최대 속도 제한을 설정합니다.
        
        Args:
            max_x: 최대 수평 속도
            max_y: 최대 수직 속도
        """
        self.max_velocity[0] = max_x
        self.max_velocity[1] = max_y
    
    def set_drag(self, drag: float) -> None:
        """
        저항 계수를 설정합니다.
        
        Args:
            drag: 저항 값 (0-1, 1 = 저항 없음)
        """
        self.drag = max(0.0, min(1.0, drag))
