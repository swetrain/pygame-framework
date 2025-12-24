"""
Pygame Framework - 재사용 가능한 2D 게임 개발 프레임워크

이 프레임워크는 Pygame을 사용하여 2D 게임을 구축하기 위한 구조화된 접근 방식을 제공하며,
명확한 아키텍처와 일관된 패턴으로 AI 지원 개발에 최적화되어 있습니다.
"""

__version__ = "0.1.0"
__author__ = "Pygame Framework Contributors"

# 핵심 모듈 임포트
from framework.core.game import Game
from framework.core.scene import Scene, SceneManager
from framework.core.entity import Entity

# 매니저 모듈 임포트
from framework.managers.resource import ResourceManager
from framework.managers.input import InputManager
from framework.managers.audio import AudioManager

# 컴포넌트 모듈 임포트
from framework.components.sprite import Sprite
from framework.components.animation import Animation
from framework.components.physics import PhysicsComponent
from framework.components.collision import CollisionComponent

# UI 모듈 임포트
from framework.ui.button import Button
from framework.ui.text import Text

# 유틸리티 모듈 임포트
from framework.utils.camera import Camera
from framework.utils.config import Config
from framework.utils.helpers import *

__all__ = [
    # 핵심
    'Game',
    'Scene',
    'SceneManager',
    'Entity',
    # 매니저
    'ResourceManager',
    'InputManager',
    'AudioManager',
    # 컴포넌트
    'Sprite',
    'Animation',
    'PhysicsComponent',
    'CollisionComponent',
    # UI
    'Button',
    'Text',
    # 유틸리티
    'Camera',
    'Config',
]
