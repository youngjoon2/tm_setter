#!/usr/bin/env python3
"""TM Setter GUI 테스트 스크립트"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_gui():
    """GUI 테스트 실행"""
    try:
        # 메인 모듈 임포트
        from main import TMSetterApp
        
        print("TM Setter GUI를 시작합니다...")
        print("다크 테마가 적용된 새로운 디자인을 확인하세요.")
        print("-" * 50)
        print("테스트 계정: ID='admin', PW='admin'")
        print("-" * 50)
        
        # 애플리케이션 실행
        app = TMSetterApp()
        app.run()
        
    except ImportError as e:
        print(f"모듈 임포트 오류: {e}")
        print("필요한 의존성을 설치해주세요.")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"GUI 실행 중 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_gui()
    sys.exit(0 if success else 1)