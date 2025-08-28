"""설정 관리 모듈"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """애플리케이션 설정 관리"""
    
    DEFAULT_CONFIG = {
        "window": {
            "width": 600,
            "height": 500,
            "min_width": 500,
            "min_height": 400
        },
        "api": {
            "jira_url": "",
            "timeout": 30
        },
        "db_codes": {
            "item1_options": ["Option 1", "Option 2", "Option 3"],
            "item2_options": ["Option A", "Option B", "Option C"],
            "item3_options": ["Item X", "Item Y", "Item Z"]
        },
        "sw_versions": ["1.0.0", "1.1.0", "2.0.0", "2.1.0"],
        "theme": {
            "primary_color": "#667eea",
            "secondary_color": "#764ba2",
            "bg_color": "#ffffff",
            "text_color": "#333333"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        설정 초기화
        
        Args:
            config_path: 설정 파일 경로 (기본값: ~/.tm_setter/config.json)
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            home = Path.home()
            self.config_dir = home / ".tm_setter"
            self.config_dir.mkdir(exist_ok=True)
            self.config_path = self.config_dir / "config.json"
            
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 기본 설정과 병합
                    return self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
            except Exception as e:
                print(f"설정 파일 로드 실패: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # 기본 설정 파일 생성
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
            
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """기본 설정과 로드된 설정 병합"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
        
    def _save_config(self, config: Dict[str, Any]):
        """설정 파일 저장"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"설정 파일 저장 실패: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        설정 값 가져오기
        
        Args:
            key: 설정 키 (점 표기법 지원, 예: "window.width")
            default: 기본값
            
        Returns:
            설정 값
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """
        설정 값 저장
        
        Args:
            key: 설정 키 (점 표기법 지원)
            value: 설정 값
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        self._save_config(self.config)
        
    def save(self):
        """현재 설정 저장"""
        self._save_config(self.config)


class SessionManager:
    """세션 관리"""
    
    def __init__(self):
        self.session_data: Dict[str, Any] = {}
        self.user_id: Optional[str] = None
        self.user_name: Optional[str] = None
        self.is_authenticated: bool = False
        
    def login(self, user_id: str, user_name: str = None, **kwargs):
        """로그인 처리"""
        self.user_id = user_id
        self.user_name = user_name or user_id
        self.is_authenticated = True
        self.session_data.update(kwargs)
        
    def logout(self):
        """로그아웃 처리"""
        self.user_id = None
        self.user_name = None
        self.is_authenticated = False
        self.session_data.clear()
        
    def get(self, key: str, default: Any = None) -> Any:
        """세션 데이터 가져오기"""
        return self.session_data.get(key, default)
        
    def set(self, key: str, value: Any):
        """세션 데이터 설정"""
        self.session_data[key] = value
        
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """사용자 정보 가져오기"""
        if self.is_authenticated:
            return {
                'user_id': self.user_id,
                'user_name': self.user_name,
                **self.session_data
            }
        return None