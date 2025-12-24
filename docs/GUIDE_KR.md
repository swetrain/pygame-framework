# Pygame Framework 사용 가이드

> [English Guide](GUIDE.md) 📚

---

## 📑 목차

1. [소개](#소개)
2. [설치 및 설정](#설치-및-설정)
3. [핵심 개념](#핵심-개념)
4. [첫 게임 만들기](#첫-게임-만들기)
5. [주요 클래스 레퍼런스](#주요-클래스-레퍼런스)
6. [고급 기능](#고급-기능)
7. [실전 예제](#실전-예제)
8. [AI와 함께 개발하기](#ai와-함께-개발하기)
9. [문제 해결](#문제-해결)
10. [FAQ](#faq)

---

## 📖 소개

### Pygame Framework란?

Pygame Framework는 2D 게임 개발을 위한 재사용 가능한 프레임워크입니다. Pygame을 기반으로 구축되었으며, 다음과 같은 특징을 가지고 있습니다:

- 🎮 **게임 루프 자동 관리**: 초기화, 업데이트, 렌더링을 자동으로 처리
- 🎬 **씬 시스템**: 메뉴, 게임플레이, 게임오버 등 화면 전환을 쉽게 관리
- 🎨 **컴포넌트 기반**: 스프라이트, 물리, 충돌 등 기능을 조합하여 사용
- 🔧 **리소스 관리**: 이미지, 사운드, 폰트 자동 로딩 및 캐싱
- 🎯 **AI 친화적**: GitHub Copilot과 함께 사용하기 최적화된 구조

### 누구를 위한 프레임워크인가?

- ✅ 기획자가 AI와 협업하여 게임을 만들고 싶을 때
- ✅ 여러 개의 2D 게임을 빠르게 프로토타이핑하고 싶을 때
- ✅ 반복적인 보일러플레이트 코드 작성을 줄이고 싶을 때
- ✅ 체계적인 게임 아키텍처를 배우고 싶을 때

### 프레임워크 구조

```
framework/
├── core/           # 핵심 엔진 (Game, Scene, Entity)
├── managers/       # 매니저들 (Resource, Input, Audio)
├── components/     # 컴포넌트들 (Sprite, Physics, Collision, Animation)
├── ui/             # UI 요소들 (Button, Text)
└── utils/          # 유틸리티 (Camera, Config, Helpers)
```

---

## 🚀 설치 및 설정

### 1. Python 설치

Python 3.9 이상이 필요합니다.

- [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드
- 설치 시 "Add Python to PATH" 옵션 체크 필수

### 2. 저장소 클론

```bash
git clone https://github.com/swetrain/pygame-framework.git
cd pygame-framework
```

### 3. 가상환경 생성 (권장)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 5. 예제 실행하여 테스트

```bash
python examples/simple_game.py
```

게임 창이 열리면 설치 완료! 🎉

### 6. VSCode 설정 (선택사항)

**추천 확장 프로그램:**
- Python (Microsoft)
- Pylance
- GitHub Copilot (AI 개발용)

---

## 🎯 핵심 개념

### 1. Game 클래스

모든 게임의 시작점입니다. 게임 루프를 자동으로 관리합니다.

**주요 기능:**
- 게임 윈도우 생성
- FPS 관리
- 씬 전환
- 이벤트 처리

**기본 사용법:**
```python
from framework.core.game import Game

class MyGame(Game):
    def __init__(self):
        super().__init__(
            title="내 게임",
            width=800,
            height=600,
            fps=60
        )

if __name__ == "__main__":
    game = MyGame()
    game.run()
```

### 2. Scene 시스템

게임의 각 화면(메뉴, 게임플레이, 게임오버 등)을 나타냅니다.

**씬 생명주기:**
1. `on_enter()` - 씬 시작 시 호출
2. `handle_events(events)` - 이벤트 처리
3. `update(dt)` - 매 프레임마다 게임 로직 업데이트
4. `render(screen)` - 화면에 그리기
5. `on_exit()` - 씬 종료 시 호출

**기본 사용법:**
```python
from framework.core.scene import Scene
import pygame

class GameScene(Scene):
    def on_enter(self):
        """씬 시작 시 초기화"""
        self.player_x = 400
        self.player_y = 300

    def update(self, dt):
        """게임 로직 (dt는 델타타임)"""
        self.player_x += 100 * dt  # 초당 100픽셀 이동

    def render(self, screen):
        """화면 그리기"""
        screen.fill((0, 0, 0))  # 검은 배경
        pygame.draw.circle(screen, (255, 0, 0),
                          (int(self.player_x), int(self.player_y)), 20)
```

### 3. Entity (엔티티)

게임 오브젝트의 기본 클래스입니다. 플레이어, 적, 아이템 등 모든 것이 Entity입니다.

**특징:**
- 위치(x, y)와 크기(width, height) 관리
- 컴포넌트 시스템 지원
- 자동 업데이트 및 렌더링

**기본 사용법:**
```python
from framework.core.entity import Entity
from framework.components.sprite import Sprite

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 64, 64)
        # 스프라이트 컴포넌트 추가
        self.sprite = Sprite("assets/player.png")
        self.add_component(self.sprite)
```

### 4. Component (컴포넌트) 패턴

엔티티에 기능을 추가하는 방식입니다. 레고 블록처럼 조합하여 사용합니다.

**제공되는 컴포넌트:**
- `Sprite` - 이미지 표시
- `Animation` - 스프라이트 애니메이션
- `PhysicsComponent` - 물리 (속도, 가속도, 중력)
- `CollisionComponent` - 충돌 감지

**사용 예:**
```python
from framework.components.physics import PhysicsComponent
from framework.components.collision import CollisionComponent

# 물리 컴포넌트 추가
physics = PhysicsComponent()
physics.velocity_x = 200  # 초당 200픽셀
physics.gravity = 500     # 중력 적용
player.add_component(physics)

# 충돌 컴포넌트 추가
collision = CollisionComponent()
collision.on_collision = lambda other: print("충돌!")
player.add_component(collision)
```

---

## 🎮 첫 게임 만들기

단계별로 간단한 게임을 만들어 봅시다.

### Step 1: 게임 클래스 생성

```python
# my_game.py
from framework.core.game import Game
from my_scene import GameScene

class MyGame(Game):
    def __init__(self):
        super().__init__(
            title="내 첫 게임",
            width=800,
            height=600,
            fps=60
        )

        # 첫 씬 설정
        self.change_scene(GameScene(self))

if __name__ == "__main__":
    game = MyGame()
    game.run()
```

### Step 2: 게임 씬 만들기

```python
# my_scene.py
from framework.core.scene import Scene
from framework.managers.input import InputManager
import pygame

class GameScene(Scene):
    def on_enter(self):
        """씬 초기화"""
        self.player_x = 400
        self.player_y = 300
        self.player_speed = 300  # 초당 300픽셀

    def update(self, dt):
        """게임 로직"""
        # 방향키로 플레이어 이동
        if InputManager.is_key_pressed(pygame.K_LEFT):
            self.player_x -= self.player_speed * dt
        if InputManager.is_key_pressed(pygame.K_RIGHT):
            self.player_x += self.player_speed * dt
        if InputManager.is_key_pressed(pygame.K_UP):
            self.player_y -= self.player_speed * dt
        if InputManager.is_key_pressed(pygame.K_DOWN):
            self.player_y += self.player_speed * dt

    def render(self, screen):
        """화면 그리기"""
        # 배경
        screen.fill((50, 50, 100))

        # 플레이어 (빨간 원)
        pygame.draw.circle(screen, (255, 0, 0),
                          (int(self.player_x), int(self.player_y)), 25)
```

### Step 3: 실행!

```bash
python my_game.py
```

방향키로 빨간 원을 움직일 수 있습니다! 🎮

---

## 📚 주요 클래스 레퍼런스

### Game 클래스

```python
from framework.core.game import Game

class Game:
    def __init__(self, title: str, width: int, height: int, fps: int = 60)
    def run(self) -> None
    def change_scene(self, scene: Scene) -> None
    def quit(self) -> None
```

**주요 메서드:**

#### `__init__(title, width, height, fps=60)`
게임을 초기화합니다.
- `title`: 게임 창 제목
- `width`: 화면 너비 (픽셀)
- `height`: 화면 높이 (픽셀)
- `fps`: 목표 FPS (기본값: 60)

#### `run()`
게임 루프를 시작합니다. 이 메서드는 게임이 종료될 때까지 반환되지 않습니다.

#### `change_scene(scene)`
현재 씬을 다른 씬으로 전환합니다.

```python
# 예: 게임오버 씬으로 전환
game.change_scene(GameOverScene(game))
```

#### `quit()`
게임을 종료합니다.

---

### Scene 클래스

```python
from framework.core.scene import Scene

class Scene:
    def on_enter(self) -> None
    def on_exit(self) -> None
    def handle_events(self, events: list) -> None
    def update(self, dt: float) -> None
    def render(self, screen: pygame.Surface) -> None
```

**라이프사이클 메서드:**

#### `on_enter()`
씬이 시작될 때 한 번 호출됩니다. 초기화 작업을 여기서 수행합니다.

#### `on_exit()`
씬이 종료될 때 한 번 호출됩니다. 정리 작업을 여기서 수행합니다.

#### `handle_events(events)`
Pygame 이벤트를 처리합니다.

```python
def handle_events(self, events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("스페이스바 눌림!")
```

#### `update(dt)`
매 프레임마다 호출됩니다. 게임 로직을 여기서 업데이트합니다.
- `dt`: 델타 타임 (이전 프레임으로부터 경과한 시간, 초 단위)

#### `render(screen)`
화면에 그리기를 수행합니다.
- `screen`: Pygame Surface 객체

---

### Entity 클래스

```python
from framework.core.entity import Entity

class Entity:
    def __init__(self, x: float, y: float, width: int, height: int)
    def add_component(self, component) -> None
    def get_component(self, component_type: type)
    def update(self, dt: float) -> None
    def render(self, screen: pygame.Surface) -> None
```

**주요 속성:**
- `x, y`: 위치
- `width, height`: 크기
- `active`: 활성화 여부

**주요 메서드:**

#### `add_component(component)`
엔티티에 컴포넌트를 추가합니다.

```python
sprite = Sprite("player.png")
entity.add_component(sprite)
```

#### `get_component(component_type)`
특정 타입의 컴포넌트를 가져옵니다.

```python
sprite = entity.get_component(Sprite)
```

---

### ResourceManager (리소스 관리자)

```python
from framework.managers.resource import ResourceManager

# 이미지 로드
image = ResourceManager.load_image("assets/player.png")

# 사운드 로드
sound = ResourceManager.load_sound("assets/jump.wav")

# 폰트 로드
font = ResourceManager.load_font("assets/font.ttf", 24)
```

**특징:**
- 자동 캐싱 (같은 파일은 한 번만 로드)
- 경로 자동 처리
- 싱글톤 패턴

---

### InputManager (입력 관리자)

```python
from framework.managers.input import InputManager
import pygame

# 키보드
if InputManager.is_key_down(pygame.K_SPACE):
    print("스페이스바 방금 눌림")

if InputManager.is_key_pressed(pygame.K_LEFT):
    print("왼쪽 키 누르는 중")

if InputManager.is_key_up(pygame.K_SPACE):
    print("스페이스바 뗌")

# 마우스
mouse_x, mouse_y = InputManager.get_mouse_pos()
if InputManager.is_mouse_button_down(0):  # 0 = 왼쪽 버튼
    print(f"마우스 클릭: ({mouse_x}, {mouse_y})")
```

**메서드:**
- `is_key_down(key)`: 키를 방금 눌렀는가?
- `is_key_pressed(key)`: 키를 누르고 있는가?
- `is_key_up(key)`: 키를 방금 뗐는가?
- `get_mouse_pos()`: 마우스 위치 (x, y)
- `is_mouse_button_down(button)`: 마우스 버튼 눌림

---

### AudioManager (오디오 관리자)

```python
from framework.managers.audio import AudioManager

# 배경 음악 재생 (루프)
AudioManager.play_music("assets/bgm.mp3")

# 효과음 재생
AudioManager.play_sound("assets/jump.wav")

# 음악 일시정지
AudioManager.pause_music()

# 음악 재개
AudioManager.unpause_music()

# 음악 정지
AudioManager.stop_music()

# 볼륨 조절 (0.0 ~ 1.0)
AudioManager.set_music_volume(0.5)
AudioManager.set_sound_volume(0.7)
```

---

### 컴포넌트들

#### Sprite (스프라이트)

```python
from framework.components.sprite import Sprite

sprite = Sprite("assets/player.png")
sprite.scale = 2.0  # 2배 크기
sprite.rotation = 45  # 45도 회전
sprite.flip_x = True  # 좌우 반전
entity.add_component(sprite)
```

#### Animation (애니메이션)

```python
from framework.components.animation import Animation

# 프레임 기반 애니메이션
animation = Animation([
    "assets/walk_1.png",
    "assets/walk_2.png",
    "assets/walk_3.png",
    "assets/walk_4.png"
], fps=10)  # 초당 10프레임

animation.play()  # 재생
animation.pause()  # 일시정지
animation.loop = True  # 루프 설정
entity.add_component(animation)
```

#### PhysicsComponent (물리)

```python
from framework.components.physics import PhysicsComponent

physics = PhysicsComponent()
physics.velocity_x = 200  # 초당 200픽셀 (오른쪽)
physics.velocity_y = -300  # 초당 -300픽셀 (위)
physics.gravity = 980  # 중력 (픽셀/초²)
physics.max_velocity_y = 500  # 최대 낙하 속도

entity.add_component(physics)
```

#### CollisionComponent (충돌)

```python
from framework.components.collision import CollisionComponent

collision = CollisionComponent()
collision.on_collision = lambda other: print(f"{other}와 충돌!")
entity.add_component(collision)

# 충돌 체크
if collision.check_collision(other_entity):
    print("충돌 감지!")
```

---

### UI 컴포넌트들

#### Button (버튼)

```python
from framework.ui.button import Button

def on_click():
    print("버튼 클릭!")

button = Button(
    x=300, y=200,
    width=200, height=60,
    text="시작하기",
    on_click=on_click
)

# update와 render에서 사용
button.update(dt)
button.render(screen)
```

#### Text (텍스트)

```python
from framework.ui.text import Text

text = Text(
    text="점수: 0",
    x=10, y=10,
    font_size=32,
    color=(255, 255, 255)
)

# 텍스트 변경
text.set_text("점수: 100")

text.render(screen)
```

---

### Utils (유틸리티)

#### Camera (카메라)

```python
from framework.utils.camera import Camera

camera = Camera(screen_width, screen_height)

# 플레이어 따라가기
camera.follow(player_x, player_y)

# 렌더링 시 카메라 오프셋 적용
camera.apply(entity)
```

#### Config (설정)

```python
from framework.utils.config import Config

# 설정 저장
Config.set("volume", 0.8)
Config.set("fullscreen", False)
Config.save("config.json")

# 설정 로드
Config.load("config.json")
volume = Config.get("volume", default=1.0)
```

---

## 🎨 고급 기능

### 씬 전환 효과

```python
class FadeTransition:
    def __init__(self, from_scene, to_scene, duration=1.0):
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.duration = duration
        self.elapsed = 0

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            return self.to_scene
        return None

    def render(self, screen):
        self.from_scene.render(screen)
        alpha = int(255 * (self.elapsed / self.duration))
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(alpha)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
```

### 파티클 시스템

```python
class Particle(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 4, 4)
        self.lifetime = 1.0
        self.age = 0

        physics = PhysicsComponent()
        physics.velocity_x = random.uniform(-100, 100)
        physics.velocity_y = random.uniform(-200, -50)
        physics.gravity = 200
        self.add_component(physics)

    def update(self, dt):
        super().update(dt)
        self.age += dt
        if self.age >= self.lifetime:
            self.active = False
```

### 타일맵

```python
class TileMap:
    def __init__(self, tile_data, tile_size=32):
        self.tile_data = tile_data
        self.tile_size = tile_size

    def render(self, screen, camera):
        for y, row in enumerate(self.tile_data):
            for x, tile_id in enumerate(row):
                if tile_id != 0:
                    pos_x = x * self.tile_size - camera.offset_x
                    pos_y = y * self.tile_size - camera.offset_y
                    pygame.draw.rect(screen, (100, 100, 100),
                                   (pos_x, pos_y, self.tile_size, self.tile_size))
```

---

## 🎯 실전 예제

### 예제 1: 플랫포머 게임

```python
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 48)

        # 스프라이트
        self.sprite = Sprite("player.png")
        self.add_component(self.sprite)

        # 물리
        self.physics = PhysicsComponent()
        self.physics.gravity = 980
        self.add_component(self.physics)

        # 충돌
        self.collision = CollisionComponent()
        self.add_component(self.collision)

        self.jump_power = -400
        self.move_speed = 200
        self.on_ground = False

    def update(self, dt):
        # 이동
        if InputManager.is_key_pressed(pygame.K_LEFT):
            self.physics.velocity_x = -self.move_speed
        elif InputManager.is_key_pressed(pygame.K_RIGHT):
            self.physics.velocity_x = self.move_speed
        else:
            self.physics.velocity_x = 0

        # 점프
        if InputManager.is_key_down(pygame.K_SPACE) and self.on_ground:
            self.physics.velocity_y = self.jump_power
            self.on_ground = False

        super().update(dt)
```

### 예제 2: 슈팅 게임

```python
class Bullet(Entity):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 8, 8)

        physics = PhysicsComponent()
        physics.velocity_y = -500 * direction  # 위로 발사
        self.add_component(physics)

    def update(self, dt):
        super().update(dt)
        # 화면 밖으로 나가면 제거
        if self.y < -10:
            self.active = False

class ShooterPlayer(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 48)
        self.shoot_cooldown = 0

    def update(self, dt):
        # 이동
        if InputManager.is_key_pressed(pygame.K_LEFT):
            self.x -= 300 * dt
        if InputManager.is_key_pressed(pygame.K_RIGHT):
            self.x += 300 * dt

        # 발사
        self.shoot_cooldown -= dt
        if InputManager.is_key_pressed(pygame.K_SPACE) and self.shoot_cooldown <= 0:
            bullet = Bullet(self.x, self.y, 1)
            self.scene.add_entity(bullet)
            self.shoot_cooldown = 0.2  # 0.2초 쿨다운

        super().update(dt)
```

---

## 🤖 AI와 함께 개발하기

### GitHub Copilot 활용 팁

프레임워크는 AI 기반 개발에 최적화되어 있습니다.

#### 1. 명확한 클래스 구조 활용

```python
# 효과적인 프롬프트:
# "Enemy 클래스를 Entity를 상속받아 만들어줘.
#  위에서 아래로 이동하고, 플레이어와 충돌하면 데미지를 입혀줘."

class Enemy(Entity):
    # Copilot이 자동으로 완성
```

#### 2. 컴포넌트 패턴 활용

```python
# "이 엔티티에 물리와 충돌 컴포넌트를 추가해줘"
physics = PhysicsComponent()
collision = CollisionComponent()
entity.add_component(physics)
entity.add_component(collision)
```

#### 3. 씬 기반 구조

```python
# "메뉴 씬을 만들어줘.
#  시작 버튼과 종료 버튼이 있고,
#  시작 버튼을 누르면 게임 씬으로 전환되게 해줘."

class MenuScene(Scene):
    # Copilot이 자동으로 완성
```

### 효과적인 프롬프트 작성법

**좋은 예:**
```
"Player 클래스를 만들어줘. Entity를 상속받고,
 방향키로 이동할 수 있고, 스페이스바로 점프할 수 있게 해줘.
 PhysicsComponent를 사용해서 중력도 적용해줘."
```

**나쁜 예:**
```
"플레이어 만들어줘"  # 너무 모호함
```

---

## 🔧 문제 해결

### 자주 발생하는 문제

#### 1. "No module named 'pygame'"

**원인:** pygame이 설치되지 않음

**해결:**
```bash
pip install pygame
```

#### 2. "FileNotFoundError: assets/player.png"

**원인:** 리소스 파일 경로가 잘못됨

**해결:**
- 파일이 실제로 존재하는지 확인
- 경로가 정확한지 확인 (상대 경로 사용)
- 작업 디렉토리 확인

#### 3. 게임이 느려요

**해결:**
- FPS를 확인 (60 FPS가 유지되는지)
- 리소스 캐싱 확인 (ResourceManager 사용)
- 불필요한 렌더링 줄이기
- 충돌 체크 최적화

#### 4. 충돌 감지가 안 돼요

**해결:**
- CollisionComponent가 추가되었는지 확인
- 엔티티의 크기(width, height)가 올바른지 확인
- 충돌 체크 로직이 update에서 호출되는지 확인

### 디버깅 팁

```python
# FPS 표시
def render(self, screen):
    # ... 렌더링 코드 ...

    # FPS 표시
    fps_text = Text(f"FPS: {int(self.game.clock.get_fps())}", 10, 10)
    fps_text.render(screen)

# 엔티티 위치 표시
def render(self, screen):
    super().render(screen)
    # 경계 상자 그리기
    pygame.draw.rect(screen, (0, 255, 0),
                    (self.x, self.y, self.width, self.height), 2)
```

---

## ❓ FAQ

### Q: 다른 게임 라이브러리와의 차이점은?

**A:** Pygame Framework는:
- ✅ Pygame 위에 구축되어 Pygame의 모든 기능 사용 가능
- ✅ 보일러플레이트 코드 자동 처리
- ✅ 컴포넌트 기반 아키텍처
- ✅ AI 개발에 최적화

### Q: 상용 게임 개발이 가능한가요?

**A:** 네! 하지만:
- ✅ 2D 게임에 적합
- ✅ 인디 게임, 프로토타입에 최적
- ⚠️ 대규모 프로젝트는 Unity, Godot 고려

### Q: 멀티플레이어 지원은?

**A:** 현재는 싱글플레이어만 지원합니다.
네트워크 기능은 직접 추가해야 합니다.

### Q: 모바일 게임 개발은?

**A:** Pygame은 PC용입니다.
모바일은 Kivy, BeeWare 등 다른 도구 필요.

### Q: 프레임워크를 수정해도 되나요?

**A:** 물론입니다! 오픈소스이며 자유롭게 수정 가능합니다.

### Q: 3D 게임도 만들 수 있나요?

**A:** 아니요. 이 프레임워크는 2D 전용입니다.
3D는 Pygame-3D, Panda3D, Unity 등을 사용하세요.

### Q: 게임을 배포하려면?

**A:**
- PyInstaller로 실행 파일 생성
- `pyinstaller --onefile my_game.py`
- assets 폴더도 함께 배포 필요

### Q: 프레임워크 업데이트는?

**A:**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 📞 지원 및 커뮤니티

- 📧 이슈: [GitHub Issues](https://github.com/swetrain/pygame-framework/issues)
- 📖 문서: [English Guide](GUIDE.md)
- 💻 예제: `examples/` 폴더 참고

---

## 🎉 마치며

이제 프레임워크를 사용하여 멋진 게임을 만들 준비가 되었습니다!

**다음 단계:**
1. 예제 게임들을 실행해보세요
2. 간단한 게임부터 만들어보세요
3. AI와 함께 개발해보세요
4. 커뮤니티에 공유하세요!

Happy Game Making! 🎮✨
