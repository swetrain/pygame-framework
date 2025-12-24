"""Component system for entities."""

from framework.components.sprite import Sprite
from framework.components.animation import Animation
from framework.components.physics import PhysicsComponent
from framework.components.collision import CollisionComponent

__all__ = ['Sprite', 'Animation', 'PhysicsComponent', 'CollisionComponent']
