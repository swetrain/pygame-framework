# Pygame Framework Usage Guide

> [🇰🇷 한국어 가이드 (Korean Guide)](GUIDE_KR.md)

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Components Guide](#components-guide)
6. [Managers Guide](#managers-guide)
7. [UI Components](#ui-components)
8. [Utilities](#utilities)
9. [Examples](#examples)
10. [FAQ](#faq)

## Introduction

The Pygame Framework is a structured, component-based framework for building 2D games with Pygame. It's designed to work seamlessly with AI-assisted development tools like GitHub Copilot, providing clear, consistent patterns for game development.

### Key Features
- **Component-based architecture** - Flexible entity system
- **Scene management** - Easy state transitions
- **Resource caching** - Optimized asset loading
- **Input management** - Centralized input handling
- **Collision detection** - Built-in collision system
- **UI widgets** - Ready-to-use buttons and text
- **Camera system** - Scrolling and effects
- **Type hints** - Full type annotation support

## Installation

### Requirements
- Python 3.9 or higher
- Pygame 2.5.0 or higher

### Install from Repository

```bash
# Clone the repository
git clone https://github.com/swetrain/pygame-framework.git
cd pygame-framework

# Install dependencies
pip install -r requirements.txt
```

### Running the Example

```bash
python examples/simple_game.py
```

## Quick Start

Here's a minimal game to get you started:

```python
from framework.core.game import Game
from framework.core.scene import Scene
from framework.ui.text import Text
from framework.utils.helpers import Colors

class MyScene(Scene):
    def __init__(self, game):
        super().__init__("my_scene", game)
        self.text = None
    
    def on_enter(self):
        self.text = Text(
            "Hello, Pygame Framework!",
            (400, 300),
            font_size=36,
            color=Colors.WHITE,
            alignment="center"
        )
    
    def render(self, screen):
        screen.fill(Colors.BLACK)
        self.text.render(screen)

# Create and run game
game = Game(screen_size=(800, 600), title="My Game")
scene = MyScene(game)
game.scene_manager.add_scene(scene)
game.scene_manager.change_scene("my_scene")
game.run()
```

## Core Concepts

### Game Engine

The `Game` class is the heart of the framework. It manages:
- The game loop
- Scene management
- FPS limiting
- Delta time calculation

```python
from framework.core.game import Game

game = Game(
    screen_size=(800, 600),
    title="My Game",
    fps=60
)
```

### Scenes

Scenes represent different game states (menu, gameplay, pause, etc.).

```python
from framework.core.scene import Scene

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__("gameplay", game)
    
    def on_enter(self):
        """Called when entering this scene"""
        pass
    
    def on_exit(self):
        """Called when leaving this scene"""
        pass
    
    def handle_events(self, events):
        """Handle pygame events"""
        pass
    
    def update(self, dt):
        """Update logic (dt = delta time in seconds)"""
        pass
    
    def render(self, screen):
        """Render to screen"""
        pass
```

### Entities

Entities are game objects that can have components attached.

```python
from framework.core.entity import Entity

class Player(Entity):
    def __init__(self, position):
        super().__init__(position, size=(32, 32))
        
        # Add tags for identification
        self.add_tag("player")
        
        # Components will be added here
    
    def update(self, dt):
        super().update(dt)
        # Custom player logic here
```

## Components Guide

### Sprite Component

Renders images with transform support.

```python
from framework.components.sprite import Sprite
from framework.managers.resource import ResourceManager

# Load or create image
resource_manager = ResourceManager()
image = resource_manager.create_surface((32, 32), (255, 0, 0))

# Create sprite component
sprite = Sprite(image, scale=1.0, rotation=0)
entity.add_component('sprite', sprite)

# Modify sprite
sprite.scale = 2.0  # Double size
sprite.rotation = 45  # Rotate 45 degrees
sprite.flip_x = True  # Flip horizontally
sprite.alpha = 128  # Half transparent
```

### Animation Component

Frame-based animation system.

```python
from framework.components.animation import Animation

# Create animation from frames
frames = [frame1, frame2, frame3]
animation = Animation(
    frames=frames,
    frame_duration=0.1,  # 10 FPS
    loop=True
)
entity.add_component('animation', animation)

# Control animation
animation.play()
animation.stop()
animation.restart()
```

### Physics Component

Handles velocity, acceleration, and gravity.

```python
from framework.components.physics import PhysicsComponent

physics = PhysicsComponent(
    velocity=(0, 0),
    acceleration=(0, 0),
    gravity=500,  # Pixels per second squared
    max_velocity=(400, 600),
    drag=0.95
)
entity.add_component('physics', physics)

# Apply forces
physics.apply_force(100, 0)  # Push right
physics.set_velocity(0, -300)  # Jump
```

### Collision Component

AABB collision detection with callbacks.

```python
from framework.components.collision import CollisionComponent

def on_hit(other_entity):
    print(f"Hit {other_entity}!")

collision = CollisionComponent(
    offset=(0, 0),
    size=(32, 32),  # Override entity size if needed
    on_collision=on_hit,
    layer='player',
    collision_tags={'enemy', 'obstacle'}
)
entity.add_component('collision', collision)
```

## Managers Guide

### Resource Manager

Singleton for loading and caching assets.

```python
from framework.managers.resource import ResourceManager

resource_manager = ResourceManager()

# Set base path for resources
resource_manager.set_base_path("assets")

# Load image
image = resource_manager.load_image("player.png")
scaled_image = resource_manager.load_image("enemy.png", scale=(64, 64))

# Create colored surface
red_square = resource_manager.create_surface((32, 32), (255, 0, 0))

# Load sound
sound = resource_manager.load_sound("jump.wav")

# Load font
font = resource_manager.load_font("font.ttf", size=24)
default_font = resource_manager.load_font(size=20)  # System font
```

### Input Manager

Centralized input handling with action mapping.

```python
from framework.managers.input import InputManager
import pygame

input_manager = InputManager()

# Update each frame
input_manager.update(events)

# Check key states
if input_manager.is_key_pressed(pygame.K_SPACE):
    print("Space just pressed!")

if input_manager.is_key_held(pygame.K_w):
    print("W is held down")

# Mouse input
if input_manager.is_mouse_button_pressed(1):  # Left click
    mouse_x, mouse_y = input_manager.get_mouse_pos()
    print(f"Clicked at {mouse_x}, {mouse_y}")

# Action mapping
input_manager.map_action("jump", pygame.K_SPACE)
input_manager.map_action("shoot", pygame.K_LCTRL)

if input_manager.is_action_pressed("jump"):
    player.jump()

# Axis input (for movement)
horizontal = input_manager.get_axis(pygame.K_a, pygame.K_d)
vertical = input_manager.get_axis(pygame.K_w, pygame.K_s)
```

### Audio Manager

Music and sound effects management.

```python
from framework.managers.audio import AudioManager

audio_manager = AudioManager()

# Play background music
audio_manager.play_music("music/theme.mp3", loops=-1)

# Control music
audio_manager.pause_music()
audio_manager.unpause_music()
audio_manager.stop_music(fade_ms=1000)

# Set volumes (0.0 to 1.0)
audio_manager.set_music_volume(0.7)
audio_manager.set_sound_volume(0.8)

# Play sound effects
jump_sound = resource_manager.load_sound("jump.wav")
audio_manager.play_sound(jump_sound)
```

## UI Components

### Button

Interactive buttons with hover and click states.

```python
from framework.ui.button import Button

def on_click():
    print("Button clicked!")

button = Button(
    position=(100, 100),
    size=(200, 50),
    text="Click Me",
    callback=on_click,
    bg_color=(100, 100, 100),
    hover_color=(150, 150, 150)
)

# Update and render
button.update(events)
button.render(screen)
```

### Text

Text rendering with alignment options.

```python
from framework.ui.text import Text

text = Text(
    "Score: 0",
    position=(400, 50),
    font_size=32,
    color=(255, 255, 255),
    alignment="center"
)

# Update text
text.set_text(f"Score: {score}")

# Render
text.render(screen)
```

## Utilities

### Camera

Scrolling camera with follow and shake effects.

```python
from framework.utils.camera import Camera

camera = Camera(viewport_size=(800, 600))

# Follow entity
camera.follow(player, speed=0.5)

# Manual control
camera.set_position(100, 100)
camera.move(10, 0)

# Screen shake
camera.shake(intensity=10, duration=0.5)

# Update camera
camera.update(dt)

# Transform world to screen coordinates
screen_pos = camera.world_to_screen(entity.position[0], entity.position[1])
```

### Config

JSON-based configuration management.

```python
from framework.utils.config import Config

config = Config("game_config.json")

# Get values
screen_width = config.get("screen_width", 800)
music_volume = config.get("music_volume", 1.0)

# Set values
config.set("difficulty", "hard")
config.set_nested("controls", "jump", "space")

# Save changes
config.save()
```

### Helpers

Utility functions for common tasks.

```python
from framework.utils.helpers import *

# Colors
screen.fill(Colors.BLACK)

# Distance calculations
dist = distance(x1, y1, x2, y2)
dist_sq = distance_squared(x1, y1, x2, y2)  # Faster

# Angles
angle_rad = angle_to(x1, y1, x2, y2)
angle_deg = angle_to_degrees(x1, y1, x2, y2)

# Vector operations
nx, ny = normalize_vector(vx, vy)

# Interpolation and mapping
result = lerp(0, 100, 0.5)  # 50
clamped = clamp(150, 0, 100)  # 100

# Timer
timer = Timer(duration=5.0, autostart=True)
timer.update(dt)
if timer.is_finished():
    print("5 seconds elapsed!")
```

## Examples

### Creating a Player with Movement

```python
from framework.core.entity import Entity
from framework.components.sprite import Sprite
from framework.components.physics import PhysicsComponent
from framework.managers.resource import ResourceManager
import pygame

class Player(Entity):
    def __init__(self, position):
        super().__init__(position, (32, 32))
        
        # Create sprite
        rm = ResourceManager()
        image = rm.create_surface((32, 32), (0, 255, 0))
        self.add_component('sprite', Sprite(image))
        
        # Add physics
        physics = PhysicsComponent(gravity=800)
        self.add_component('physics', physics)
        
        self.speed = 200
        self.jump_force = -400
    
    def update(self, dt):
        super().update(dt)
        
        keys = pygame.key.get_pressed()
        physics = self.get_component('physics')
        
        # Horizontal movement
        vx = 0
        if keys[pygame.K_LEFT]:
            vx = -self.speed
        if keys[pygame.K_RIGHT]:
            vx = self.speed
        
        vy = physics.get_velocity()[1]
        physics.set_velocity(vx, vy)
```

### Scene Transitions

```python
class MenuScene(Scene):
    def __init__(self, game):
        super().__init__("menu", game)
    
    def on_enter(self):
        self.button = Button(
            position=(300, 250),
            size=(200, 50),
            text="Start Game",
            callback=lambda: self.game.set_scene("game")
        )
    
    def handle_events(self, events):
        self.button.update(events)
    
    def render(self, screen):
        screen.fill(Colors.BLACK)
        self.button.render(screen)

# In your game setup
menu = MenuScene(game)
gameplay = GameplayScene(game)
game.scene_manager.add_scene(menu)
game.scene_manager.add_scene(gameplay)
game.scene_manager.change_scene("menu")
```

## FAQ

### How do I create custom components?

Components are simple classes that can have `update()` and `render()` methods:

```python
class CustomComponent:
    def __init__(self):
        self.entity = None  # Set automatically when added
    
    def update(self, dt):
        # Update logic
        pass
    
    def render(self, screen):
        # Render logic
        pass

# Add to entity
entity.add_component('custom', CustomComponent())
```

### How do I handle collisions between specific entity types?

Use tags and collision callbacks:

```python
def player_hit_enemy(other):
    if other.has_tag("enemy"):
        print("Player hit enemy!")

player_collision = CollisionComponent(
    on_collision=player_hit_enemy,
    collision_tags={'enemy'}
)
```

### Can I use multiple scenes simultaneously?

Yes! Use `push_scene()` and `pop_scene()` for overlays:

```python
# Push pause menu over game
game.scene_manager.push_scene("pause")

# Pop pause menu to return to game
game.scene_manager.pop_scene()
```

### How do I optimize performance with many entities?

- Use spatial partitioning for collision detection
- Cull entities outside camera view
- Use object pooling for frequently created/destroyed entities
- Batch sprite rendering when possible

### Can I use this with other Pygame code?

Yes! The framework is built on top of Pygame and doesn't restrict access to Pygame functionality. You can mix framework and vanilla Pygame code as needed.

### How do I create animations?

Load multiple frames and create an Animation component:

```python
frames = [
    resource_manager.load_image("walk1.png"),
    resource_manager.load_image("walk2.png"),
    resource_manager.load_image("walk3.png"),
]
animation = Animation(frames, frame_duration=0.1, loop=True)
entity.add_component('animation', animation)
```

### Where should I put game assets?

Create an `assets` folder in your project and organize it:
```
assets/
  images/
  sounds/
  music/
  fonts/
```

Then set the resource manager base path:
```python
ResourceManager().set_base_path("assets")
```

---

For more examples and updates, visit the [GitHub repository](https://github.com/swetrain/pygame-framework).
