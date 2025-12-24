"""
Simple example game demonstrating the pygame framework.

This example shows:
- Scene system (Title and Game scenes)
- Player entity with keyboard controls
- Simple collision detection
- UI buttons
- Component-based architecture
"""

import pygame
import sys
from framework.core.game import Game
from framework.core.scene import Scene
from framework.core.entity import Entity
from framework.managers.resource import ResourceManager
from framework.managers.input import InputManager
from framework.components.sprite import Sprite
from framework.components.physics import PhysicsComponent
from framework.components.collision import CollisionComponent, CollisionSystem
from framework.ui.button import Button
from framework.ui.text import Text
from framework.utils.helpers import Colors


class Player(Entity):
    """Player entity with movement controls."""
    
    def __init__(self, position):
        super().__init__(position, (40, 40))
        
        # Create a simple player sprite (green square)
        resource_manager = ResourceManager()
        player_image = resource_manager.create_surface((40, 40), Colors.GREEN)
        
        # Add sprite component
        sprite = Sprite(player_image)
        self.add_component('sprite', sprite)
        
        # Add physics for movement
        physics = PhysicsComponent(gravity=0, drag=0.85)
        self.add_component('physics', physics)
        
        # Add collision component
        collision = CollisionComponent(collision_tags={'obstacle', 'collectible'})
        self.add_component('collision', collision)
        
        # Movement speed
        self.speed = 300
    
    def update(self, dt):
        """Update player with input handling."""
        super().update(dt)
        
        # Get input
        keys = pygame.key.get_pressed()
        physics = self.get_component('physics')
        
        # Reset horizontal velocity
        vx, vy = physics.get_velocity()
        vx = 0
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vy = self.speed
        
        physics.set_velocity(vx, vy)


class Obstacle(Entity):
    """Static obstacle entity."""
    
    def __init__(self, position, size):
        super().__init__(position, size)
        
        # Create obstacle sprite (red rectangle)
        resource_manager = ResourceManager()
        obstacle_image = resource_manager.create_surface(size, Colors.RED)
        
        sprite = Sprite(obstacle_image)
        self.add_component('sprite', sprite)
        
        # Add collision
        collision = CollisionComponent(layer='obstacle')
        self.add_component('collision', collision)


class Collectible(Entity):
    """Collectible item entity."""
    
    def __init__(self, position):
        super().__init__(position, (20, 20))
        
        # Create collectible sprite (yellow circle-ish square)
        resource_manager = ResourceManager()
        collectible_image = resource_manager.create_surface((20, 20), Colors.YELLOW)
        
        sprite = Sprite(collectible_image)
        self.add_component('sprite', sprite)
        
        # Add collision
        collision = CollisionComponent(
            layer='collectible',
            on_collision=self.on_collect
        )
        self.add_component('collision', collision)
        
        self.collected = False
    
    def on_collect(self, other_entity):
        """Handle collection."""
        if isinstance(other_entity, Player) and not self.collected:
            self.collected = True
            self.set_active(False)
            print("Collected item!")


class TitleScene(Scene):
    """Title screen scene."""
    
    def __init__(self, game):
        super().__init__("title", game)
        
        self.title_text = None
        self.start_button = None
        self.quit_button = None
    
    def on_enter(self):
        """Initialize title screen."""
        screen_width, screen_height = self.game.get_screen_size()
        
        # Title text
        self.title_text = Text(
            "Pygame Framework Demo",
            (screen_width // 2, 150),
            font_size=48,
            color=Colors.WHITE,
            alignment="center"
        )
        
        # Start button
        self.start_button = Button(
            position=(screen_width // 2 - 100, 300),
            size=(200, 50),
            text="Start Game",
            callback=self.start_game,
            bg_color=Colors.GREEN,
            hover_color=(0, 200, 0)
        )
        
        # Quit button
        self.quit_button = Button(
            position=(screen_width // 2 - 100, 370),
            size=(200, 50),
            text="Quit",
            callback=self.quit_game,
            bg_color=Colors.RED,
            hover_color=(200, 0, 0)
        )
    
    def start_game(self):
        """Start the game."""
        self.game.set_scene("game")
    
    def quit_game(self):
        """Quit the application."""
        self.game.running = False
    
    def handle_events(self, events):
        """Handle events."""
        self.start_button.update(events)
        self.quit_button.update(events)
    
    def render(self, screen):
        """Render title screen."""
        screen.fill(Colors.DARK_GRAY)
        self.title_text.render(screen)
        self.start_button.render(screen)
        self.quit_button.render(screen)


class GameScene(Scene):
    """Main gameplay scene."""
    
    def __init__(self, game):
        super().__init__("game", game)
        
        self.player = None
        self.entities = []
        self.collision_system = CollisionSystem()
        self.input_manager = InputManager()
        self.score = 0
        self.score_text = None
        self.back_button = None
    
    def on_enter(self):
        """Initialize game scene."""
        screen_width, screen_height = self.game.get_screen_size()
        
        # Create player
        self.player = Player((screen_width // 2, screen_height // 2))
        self.entities.append(self.player)
        self.collision_system.add_entity(self.player)
        
        # Create obstacles
        obstacles = [
            Obstacle((100, 100), (80, 80)),
            Obstacle((600, 400), (100, 60)),
            Obstacle((300, 500), (120, 40)),
        ]
        for obstacle in obstacles:
            self.entities.append(obstacle)
            self.collision_system.add_entity(obstacle)
        
        # Create collectibles
        collectibles = [
            Collectible((200, 300)),
            Collectible((500, 200)),
            Collectible((400, 450)),
            Collectible((150, 500)),
        ]
        for collectible in collectibles:
            self.entities.append(collectible)
            self.collision_system.add_entity(collectible)
        
        # Score text
        self.score_text = Text(
            "Use Arrow Keys or WASD to move",
            (10, 10),
            font_size=24,
            color=Colors.WHITE
        )
        
        # Back button
        self.back_button = Button(
            position=(10, 50),
            size=(120, 40),
            text="Back to Menu",
            callback=self.back_to_menu,
            bg_color=Colors.BLUE,
            hover_color=(0, 0, 200),
            font_size=18
        )
    
    def back_to_menu(self):
        """Return to title screen."""
        self.game.set_scene("title")
    
    def on_exit(self):
        """Clean up game scene."""
        self.entities.clear()
        self.collision_system.clear()
    
    def handle_events(self, events):
        """Handle events."""
        self.input_manager.update(events)
        self.back_button.update(events)
    
    def update(self, dt):
        """Update game logic."""
        # Update all entities
        for entity in self.entities:
            entity.update(dt)
        
        # Check collisions
        self.collision_system.check_collisions()
    
    def render(self, screen):
        """Render game scene."""
        screen.fill(Colors.BLACK)
        
        # Render all entities
        for entity in self.entities:
            entity.render(screen)
        
        # Render UI
        self.score_text.render(screen)
        self.back_button.render(screen)


def main():
    """Main entry point."""
    # Create game instance
    game = Game(
        screen_size=(800, 600),
        title="Pygame Framework - Simple Game Example",
        fps=60
    )
    
    # Create and register scenes
    title_scene = TitleScene(game)
    game_scene = GameScene(game)
    
    game.scene_manager.add_scene(title_scene)
    game.scene_manager.add_scene(game_scene)
    
    # Start with title scene
    game.scene_manager.change_scene("title")
    
    # Run game
    game.run()


if __name__ == "__main__":
    main()
