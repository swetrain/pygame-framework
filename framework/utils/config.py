"""
설정 관리 모듈

이 모듈은 JSON 기반의 설정 로딩과 저장을 제공합니다.
"""

from typing import Any, Dict, Optional
import json
import os


class Config:
    """
    게임 설정을 위한 설정 매니저
    
    기본값 지원과 함께 JSON 파일로부터/로
    설정 로딩과 저장을 처리합니다.
    
    Attributes:
        config_path: 설정 파일 경로
        data: 설정 값의 딕셔너리
        defaults: 기본값의 딕셔너리
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        설정 매니저를 초기화합니다.
        
        Args:
            config_path: 설정 파일 경로
        """
        self.config_path = config_path
        self.data: Dict[str, Any] = {}
        self.defaults: Dict[str, Any] = self._get_defaults()
        
        # 설정 로드
        self.load()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """
        기본 설정 값을 반환합니다.
        
        Returns:
            기본 설정 딕셔너리
        """
        return {
            # 디스플레이 설정
            "screen_width": 800,
            "screen_height": 600,
            "fullscreen": False,
            "fps": 60,
            
            # 오디오 설정
            "music_volume": 1.0,
            "sound_volume": 1.0,
            "mute_music": False,
            "mute_sound": False,
            
            # 게임 설정
            "difficulty": "normal",
            "language": "en",
            
            # 컨트롤 (사용자 정의 가능)
            "controls": {
                "up": "w",
                "down": "s",
                "left": "a",
                "right": "d",
                "jump": "space",
                "action": "e"
            }
        }
    
    def load(self) -> None:
        """
        파일에서 설정을 로드합니다.
        
        파일이 존재하지 않으면 기본값을 사용합니다.
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.data = json.load(f)
                # 누락된 키에 대해 기본값과 병합
                for key, value in self.defaults.items():
                    if key not in self.data:
                        self.data[key] = value
            except json.JSONDecodeError as e:
                print(f"Error loading config: {e}")
                self.data = self.defaults.copy()
        else:
            # 파일이 존재하지 않으면 기본값 사용
            self.data = self.defaults.copy()
    
    def save(self) -> None:
        """설정을 파일에 저장합니다."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        설정 값을 가져옵니다.
        
        Args:
            key: 설정 키
            default: 키가 존재하지 않을 경우 기본값
            
        Returns:
            설정 값 또는 기본값
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        설정 값을 설정합니다.
        
        Args:
            key: 설정 키
            value: 설정할 값
        """
        self.data[key] = value
    
    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """
        중첩된 설정 값을 가져옵니다.
        
        예제: config.get_nested("controls", "jump")
        
        Args:
            keys: 탐색할 키 시퀀스
            default: 경로가 존재하지 않을 경우 기본값
            
        Returns:
            설정 값 또는 기본값
        """
        value = self.data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set_nested(self, *keys: str, value: Any) -> None:
        """
        중첩된 설정 값을 설정합니다.
        
        예제: config.set_nested("controls", "jump", "space")
        
        Args:
            keys: 탐색할 키 시퀀스 (마지막 키가 설정됨)
            value: 설정할 값
        """
        if len(keys) < 2:
            if keys:
                self.data[keys[0]] = value
            return
        
        # 부모로 이동
        current = self.data
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        # 최종 값 설정
        current[keys[-1]] = value
    
    def reset_to_defaults(self) -> None:
        """모든 설정을 기본값으로 재설정합니다."""
        self.data = self.defaults.copy()
    
    def reset_key(self, key: str) -> None:
        """
        특정 키를 기본값으로 재설정합니다.
        
        Args:
            key: 재설정할 설정 키
        """
        if key in self.defaults:
            self.data[key] = self.defaults[key]
    
    def has_key(self, key: str) -> bool:
        """
        설정에 키가 있는지 확인합니다.
        
        Args:
            key: 설정 키
            
        Returns:
            키가 존재하면 True
        """
        return key in self.data
    
    def get_all(self) -> Dict[str, Any]:
        """
        모든 설정 데이터를 가져옵니다.
        
        Returns:
            모든 설정의 딕셔너리
        """
        return self.data.copy()
    
    def update(self, new_data: Dict[str, Any]) -> None:
        """
        새로운 값으로 설정을 업데이트합니다.
        
        Args:
            new_data: 업데이트할 값의 딕셔너리
        """
        self.data.update(new_data)
