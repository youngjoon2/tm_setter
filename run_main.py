#!/usr/bin/env python3
"""메인 실행 스크립트"""
import sys
import os
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    try:
        print("=" * 50)
        print("TM Setter GUI 시작")
        print("=" * 50)
        
        # PyQt5 임포트 확인
        try:
            from PyQt5.QtWidgets import QApplication
            print("✓ PyQt5 임포트 성공")
        except ImportError as e:
            print(f"✗ PyQt5 임포트 실패: {e}")
            sys.exit(1)
            
        # 메인 모듈 임포트
        try:
            from main_pyqt import main
            print("✓ main_pyqt 모듈 임포트 성공")
        except ImportError as e:
            print(f"✗ main_pyqt 모듈 임포트 실패: {e}")
            print(traceback.format_exc())
            sys.exit(1)
        
        print("-" * 50)
        print("프로그램 실행 중...")
        print("로그인 화면이 표시되어야 합니다:")
        print("- 다크 그레이 카드")
        print("- ID/PW 입력 필드")  
        print("- 로그인 버튼 (파란색)")
        print("- 다음 버튼 (회색)")
        print("-" * 50)
        
        # 메인 함수 실행
        main()
        
    except Exception as e:
        print("=" * 50)
        print(f"프로그램 실행 중 오류 발생: {e}")
        print("=" * 50)
        print(traceback.format_exc())
        print("=" * 50)
        input("Enter 키를 눌러 종료...")
        sys.exit(1)