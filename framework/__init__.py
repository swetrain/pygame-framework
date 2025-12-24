"""
Pygame Framework - A reusable 2D game development framework.

This framework provides a structured approach to building 2D games with Pygame,
optimized for AI-assisted development with clear architecture and consistent patterns.
"""

__version__ = "0.1.0"
__author__ = "Pygame Framework Contributors"

# Core imports
from framework.core.game import Game
from framework.core.scene import Scene, SceneManager
from framework.core.entity import Entity

# Manager imports
from framework.managers.resource import ResourceManager
from framework.managers.input import InputManager
from framework.managers.audio import AudioManager

# Component imports
from framework.components.sprite import Sprite
from framework.components.animation import Animation
from framework.components.physics import PhysicsComponent
from framework.components.collision import CollisionComponent

# UI imports
from framework.ui.button import Button
from framework.ui.text import Text

# Utility imports
from framework.utils.camera import Camera
from framework.utils.config import Config
from framework.utils.helpers import *

__all__ = [
    # Core
    'Game',
    'Scene',
    'SceneManager',
    'Entity',
    # Managers
    'ResourceManager',
    'InputManager',
    'AudioManager',
    # Components
    'Sprite',
    'Animation',
    'PhysicsComponent',
    'CollisionComponent',
    # UI
    'Button',
    'Text',
    # Utils
    'Camera',
    'Config',
]
