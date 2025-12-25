"""
pygame 프레임워크를 보여주는 간단한 예제 게임

이 예제는 다음을 보여줍니다:
- 씬 시스템 (타이틀과 게임 씬)
- 키보드 조작이 가능한 플레이어 엔티티
- 간단한 충돌 감지
- UI 버튼
- 컴포넌트 기반 아키텍처
"""

import os
import sys
import pygame

# 프로젝트 루트를 PYTHONPATH에 추가하여 `framework` 패키지를 찾을 수 있게 함
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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
    """이동 조작이 가능한 플레이어 엔티티"""
    
    def __init__(self, position):
        super().__init__(position, (40, 40))
        
        # 간단한 플레이어 스프라이트 생성 (녹색 사각형)
        resource_manager = ResourceManager()
        player_image = resource_manager.create_surface((40, 40), Colors.GREEN)
        
        # 스프라이트 컴포넌트 추가
        sprite = Sprite(player_image)
        self.add_component('sprite', sprite)
        
        # 이동을 위한 물리 추가
        physics = PhysicsComponent(gravity=0, drag=0.85)
        self.add_component('physics', physics)
        
        # 충돌 컴포넌트 추가
        collision = CollisionComponent(collision_tags={'obstacle', 'collectible'})
        self.add_component('collision', collision)
        
        # 이동 속도
        self.speed = 300
    
    def update(self, dt):
        """입력 처리와 함께 플레이어를 업데이트합니다."""
        super().update(dt)
        
        # 입력 가져오기
        keys = pygame.key.get_pressed()
        physics = self.get_component('physics')
        
        # 수평 속도 리셋
        vx, vy = physics.get_velocity()
        vx = 0
        
        # 이동
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
    """정적 장애물 엔티티"""
    
    def __init__(self, position, size):
        super().__init__(position, size)
        
        # 장애물 스프라이트 생성 (빨간색 사각형)
        resource_manager = ResourceManager()
        obstacle_image = resource_manager.create_surface(size, Colors.RED)
        
        sprite = Sprite(obstacle_image)
        self.add_component('sprite', sprite)
        
        # 충돌 추가
        collision = CollisionComponent(layer='obstacle')
        self.add_component('collision', collision)


class Collectible(Entity):
    """수집 가능한 아이템 엔티티"""
    
    def __init__(self, position):
        super().__init__(position, (20, 20))
        
        # 수집 가능한 스프라이트 생성 (노란색 원형 사각형)
        resource_manager = ResourceManager()
        collectible_image = resource_manager.create_surface((20, 20), Colors.YELLOW)
        
        sprite = Sprite(collectible_image)
        self.add_component('sprite', sprite)
        
        # 충돌 추가
        collision = CollisionComponent(
            layer='collectible',
            on_collision=self.on_collect
        )
        self.add_component('collision', collision)
        
        self.collected = False
    
    def on_collect(self, other_entity):
        """수집을 처리합니다."""
        if isinstance(other_entity, Player) and not self.collected:
            self.collected = True
            self.set_active(False)
            print("Collected item!")


class TitleScene(Scene):
    """타이틀 화면 씬"""
    
    def __init__(self, game):
        super().__init__("title", game)
        
        self.title_text = None
        self.start_button = None
        self.quit_button = None
    
    def on_enter(self):
        """타이틀 화면을 초기화합니다."""
        screen_width, screen_height = self.game.get_screen_size()
        
        # 타이틀 텍스트
        self.title_text = Text(
            "Pygame Framework Demo",
            (screen_width // 2, 150),
            font_size=48,
            color=Colors.WHITE,
            alignment="center"
        )
        
        # 시작 버튼
        self.start_button = Button(
            position=(screen_width // 2 - 100, 300),
            size=(200, 50),
            text="Start Game",
            callback=self.start_game,
            bg_color=Colors.GREEN,
            hover_color=(0, 200, 0)
        )
        
        # 종료 버튼
        self.quit_button = Button(
            position=(screen_width // 2 - 100, 370),
            size=(200, 50),
            text="Quit",
            callback=self.quit_game,
            bg_color=Colors.RED,
            hover_color=(200, 0, 0)
        )
    
    def start_game(self):
        """게임을 시작합니다."""
        self.game.set_scene("game")
    
    def quit_game(self):
        """애플리케이션을 종료합니다."""
        self.game.running = False
    
    def handle_events(self, events):
        """이벤트를 처리합니다."""
        self.start_button.update(events)
        self.quit_button.update(events)
    
    def render(self, screen):
        """타이틀 화면을 렌더링합니다."""
        screen.fill(Colors.DARK_GRAY)
        self.title_text.render(screen)
        self.start_button.render(screen)
        self.quit_button.render(screen)


class GameScene(Scene):
    """메인 게임플레이 씬"""
    
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
        """게임 씬을 초기화합니다."""
        screen_width, screen_height = self.game.get_screen_size()
        
        # 플레이어 생성
        self.player = Player((screen_width // 2, screen_height // 2))
        self.entities.append(self.player)
        self.collision_system.add_entity(self.player)
        
        # 장애물 생성
        obstacles = [
            Obstacle((100, 100), (80, 80)),
            Obstacle((600, 400), (100, 60)),
            Obstacle((300, 500), (120, 40)),
        ]
        for obstacle in obstacles:
            self.entities.append(obstacle)
            self.collision_system.add_entity(obstacle)
        
        # 수집 가능 아이템 생성
        collectibles = [
            Collectible((200, 300)),
            Collectible((500, 200)),
            Collectible((400, 450)),
            Collectible((150, 500)),
        ]
        for collectible in collectibles:
            self.entities.append(collectible)
            self.collision_system.add_entity(collectible)
        
        # 점수 텍스트
        self.score_text = Text(
            "Use Arrow Keys or WASD to move",
            (10, 10),
            font_size=24,
            color=Colors.WHITE
        )
        
        # 뒤로가기 버튼
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
        """타이틀 화면으로 돌아갑니다."""
        self.game.set_scene("title")
    
    def on_exit(self):
        """게임 씬을 정리합니다."""
        self.entities.clear()
        self.collision_system.clear()
    
    def handle_events(self, events):
        """이벤트를 처리합니다."""
        self.input_manager.update(events)
        self.back_button.update(events)
    
    def update(self, dt):
        """게임 로직을 업데이트합니다."""
        # 모든 엔티티 업데이트
        for entity in self.entities:
            entity.update(dt)
        
        # 충돌 확인
        self.collision_system.check_collisions()
    
    def render(self, screen):
        """게임 씬을 렌더링합니다."""
        screen.fill(Colors.BLACK)
        
        # 모든 엔티티 렌더링
        for entity in self.entities:
            entity.render(screen)
        
        # UI 렌더링
        self.score_text.render(screen)
        self.back_button.render(screen)


def main():
    """메인 진입점"""
    # 게임 인스턴스 생성
    game = Game(
        screen_size=(800, 600),
        title="Pygame Framework - Simple Game Example",
        fps=60
    )
    
    # 씬 생성 및 등록
    title_scene = TitleScene(game)
    game_scene = GameScene(game)
    
    game.scene_manager.add_scene(title_scene)
    game.scene_manager.add_scene(game_scene)
    
    # 타이틀 씬으로 시작
    game.scene_manager.change_scene("title")
    
    # 게임 실행
    game.run()


if __name__ == "__main__":
    main()
