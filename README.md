# Pygame Framework

**A structured, component-based 2D game development framework built on Pygame**

Pygame Framework는 AI 기반 개발 도구(GitHub Copilot 등)와 함께 사용하기 최적화된 Pygame 기반 2D 게임 개발 프레임워크입니다. 명확하고 일관된 아키텍처로 기획자가 쉽게 게임을 개발할 수 있도록 설계되었습니다.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Pygame Version](https://img.shields.io/badge/pygame-2.5.0%2B-green)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

## ✨ 주요 기능

- **🎮 컴포넌트 기반 아키텍처** - 유연한 엔티티-컴포넌트 시스템
- **🎬 씬 관리 시스템** - 메뉴, 게임플레이, 일시정지 등 게임 상태 관리
- **🎨 리소스 관리** - 이미지, 사운드, 폰트 자동 캐싱
- **⌨️ 입력 관리** - 키보드/마우스 입력 통합 관리 및 액션 매핑
- **💥 충돌 감지** - AABB 기반 충돌 감지 시스템
- **🎪 물리 시스템** - 속도, 가속도, 중력 시뮬레이션
- **🎯 UI 위젯** - 버튼, 텍스트 등 즉시 사용 가능한 UI 컴포넌트
- **📹 카메라 시스템** - 스크롤, 팔로우, 화면 흔들림 효과
- **⚙️ 설정 관리** - JSON 기반 게임 설정 저장/로드
- **📝 타입 힌팅** - 완전한 타입 어노테이션 지원

## 📦 설치

### 요구사항
- Python 3.9 이상
- Pygame 2.5.0 이상

### 설치 방법

```bash
# 저장소 클론
git clone https://github.com/swetrain/pygame-framework.git
cd pygame-framework

# 의존성 설치
pip install -r requirements.txt
```

## 🚀 빠른 시작

### 간단한 예제

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

# 게임 생성 및 실행
game = Game(screen_size=(800, 600), title="My Game")
scene = MyScene(game)
game.scene_manager.add_scene(scene)
game.scene_manager.change_scene("my_scene")
game.run()
```

### 예제 게임 실행

포함된 예제 게임을 실행하여 프레임워크의 기능을 확인하세요:

```bash
python examples/simple_game.py
```

예제 게임은 다음 기능을 시연합니다:
- 씬 전환 (타이틀 화면 ↔ 게임플레이)
- 플레이어 캐릭터 이동 (방향키 또는 WASD)
- 장애물 및 수집 아이템
- UI 버튼
- 충돌 감지

## 📖 문서

자세한 사용법은 [프레임워크 가이드](docs/GUIDE.md)를 참조하세요.

### 주요 문서 섹션

- **설치 및 설정** - 프레임워크 설치 방법
- **핵심 개념** - Game, Scene, Entity 이해하기
- **컴포넌트 가이드** - Sprite, Animation, Physics, Collision
- **매니저 가이드** - Resource, Input, Audio 관리
- **UI 컴포넌트** - Button, Text 사용법
- **유틸리티** - Camera, Config, Helpers
- **예제 코드** - 실전 코드 스니펫
- **FAQ** - 자주 묻는 질문

## 🏗️ 프로젝트 구조

```
pygame-framework/
├── framework/              # 프레임워크 코어
│   ├── core/              # 게임 엔진, 씬, 엔티티
│   ├── managers/          # 리소스, 입력, 오디오 관리자
│   ├── components/        # 스프라이트, 애니메이션, 물리, 충돌
│   ├── ui/                # UI 위젯 (버튼, 텍스트)
│   └── utils/             # 카메라, 설정, 헬퍼 함수
├── examples/              # 예제 게임
│   └── simple_game.py     # 프레임워크 데모
├── docs/                  # 문서
│   └── GUIDE.md           # 상세 사용 가이드
├── requirements.txt       # 의존성
└── README.md             # 프로젝트 소개 (이 파일)
```

## 🎯 사용 예시

### 플레이어 엔티티 생성

```python
from framework.core.entity import Entity
from framework.components.sprite import Sprite
from framework.components.physics import PhysicsComponent

class Player(Entity):
    def __init__(self, position):
        super().__init__(position, (32, 32))
        
        # 스프라이트 추가
        sprite = Sprite(player_image)
        self.add_component('sprite', sprite)
        
        # 물리 추가
        physics = PhysicsComponent(gravity=800)
        self.add_component('physics', physics)
    
    def update(self, dt):
        super().update(dt)
        # 플레이어 로직
```

### 씬 전환

```python
# 씬 생성
menu_scene = MenuScene(game)
game_scene = GameScene(game)

# 씬 등록
game.scene_manager.add_scene(menu_scene)
game.scene_manager.add_scene(game_scene)

# 씬 전환
game.scene_manager.change_scene("menu")
```

### 충돌 감지

```python
from framework.components.collision import CollisionComponent

def on_collision(other_entity):
    print(f"Collision with {other_entity}!")

collision = CollisionComponent(
    on_collision=on_collision,
    collision_tags={'enemy', 'obstacle'}
)
entity.add_component('collision', collision)
```

## 🤝 AI 기반 개발

이 프레임워크는 GitHub Copilot 등 AI 코딩 어시스턴트와 함께 사용하도록 최적화되었습니다:

- **명확한 타입 힌팅** - AI가 정확한 제안을 제공
- **일관된 네이밍** - snake_case 컨벤션
- **포괄적인 독스트링** - 모든 클래스와 메서드에 문서화
- **모듈화된 구조** - 각 기능이 독립적인 모듈로 분리

### AI와 함께 개발하기

```python
# AI에게 명확하게 지시
"Player 클래스를 Entity를 상속받아 만들어줘"
"점프 기능을 PhysicsComponent를 사용해서 구현해줘"
"버튼을 클릭하면 씬이 전환되도록 만들어줘"
```

## 🛠️ 개발 가이드라인

- **Python 3.9+** 호환
- **타입 힌팅** 사용
- **독스트링** 작성
- **snake_case** 네이밍
- **모듈화** 설계
- **에러 처리** 구현

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🌟 기여

기여를 환영합니다! 이슈를 열거나 풀 리퀘스트를 보내주세요.

## 📬 연락처

문제가 있거나 제안사항이 있으시면 GitHub Issues를 통해 알려주세요.

---

Made with ❤️ using Pygame
