#!/usr/bin/env python3
"""PyQt5 임포트 테스트"""

import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """모듈 임포트 테스트"""
    print("PyQt5 모듈 임포트 테스트 시작...")
    print("-" * 50)
    
    errors = []
    
    # PyQt5 기본 모듈 테스트
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
        print("✅ PyQt5.QtWidgets 임포트 성공")
    except ImportError as e:
        errors.append(f"PyQt5.QtWidgets: {e}")
        print(f"❌ PyQt5.QtWidgets 임포트 실패: {e}")
        
    try:
        from PyQt5.QtCore import Qt, pyqtSignal, QThread
        print("✅ PyQt5.QtCore 임포트 성공")
    except ImportError as e:
        errors.append(f"PyQt5.QtCore: {e}")
        print(f"❌ PyQt5.QtCore 임포트 실패: {e}")
        
    try:
        from PyQt5.QtGui import QFont, QPalette
        print("✅ PyQt5.QtGui 임포트 성공")
    except ImportError as e:
        errors.append(f"PyQt5.QtGui: {e}")
        print(f"❌ PyQt5.QtGui 임포트 실패: {e}")
    
    print("-" * 50)
    
    # 커스텀 모듈 테스트
    try:
        from utils.pyqt_theme import PyQtDarkTheme
        print("✅ utils.pyqt_theme 임포트 성공")
    except ImportError as e:
        errors.append(f"utils.pyqt_theme: {e}")
        print(f"❌ utils.pyqt_theme 임포트 실패: {e}")
        
    try:
        from pyqt_views.login_view import LoginView
        print("✅ pyqt_views.login_view 임포트 성공")
    except ImportError as e:
        errors.append(f"pyqt_views.login_view: {e}")
        print(f"❌ pyqt_views.login_view 임포트 실패: {e}")
        
    try:
        from pyqt_views.db_code_view import DBCodeView
        print("✅ pyqt_views.db_code_view 임포트 성공")
    except ImportError as e:
        errors.append(f"pyqt_views.db_code_view: {e}")
        print(f"❌ pyqt_views.db_code_view 임포트 실패: {e}")
        
    try:
        from pyqt_views.jira_issue_view import JiraIssueView
        print("✅ pyqt_views.jira_issue_view 임포트 성공")
    except ImportError as e:
        errors.append(f"pyqt_views.jira_issue_view: {e}")
        print(f"❌ pyqt_views.jira_issue_view 임포트 실패: {e}")
        
    try:
        from pyqt_views.options_view import OptionsView
        print("✅ pyqt_views.options_view 임포트 성공")
    except ImportError as e:
        errors.append(f"pyqt_views.options_view: {e}")
        print(f"❌ pyqt_views.options_view 임포트 실패: {e}")
        
    try:
        from main_pyqt import TMSetterMainWindow
        print("✅ main_pyqt 임포트 성공")
    except ImportError as e:
        errors.append(f"main_pyqt: {e}")
        print(f"❌ main_pyqt 임포트 실패: {e}")
        
    print("-" * 50)
    
    # 결과 요약
    if not errors:
        print("✅ 모든 모듈 임포트 성공!")
        print("\nPyQt5 GUI 구현이 완료되었습니다.")
        print("\n실행 방법:")
        print("  1. GUI 환경에서: python run_pyqt_gui.py")
        print("  2. 또는: python src/main_pyqt.py")
        return True
    else:
        print(f"❌ 임포트 실패 개수: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
        return False


def check_file_structure():
    """파일 구조 확인"""
    print("\n파일 구조 확인...")
    print("-" * 50)
    
    required_files = [
        "src/main_pyqt.py",
        "src/utils/pyqt_theme.py",
        "src/pyqt_views/login_view.py",
        "src/pyqt_views/db_code_view.py",
        "src/pyqt_views/jira_issue_view.py",
        "src/pyqt_views/options_view.py",
        "run_pyqt_gui.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        exists = os.path.exists(full_path)
        if exists:
            size = os.path.getsize(full_path)
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} (파일 없음)")
            all_exist = False
            
    print("-" * 50)
    if all_exist:
        print("✅ 모든 필수 파일이 존재합니다.")
    else:
        print("❌ 일부 파일이 누락되었습니다.")
        
    return all_exist


if __name__ == "__main__":
    # 파일 구조 확인
    structure_ok = check_file_structure()
    
    # 임포트 테스트
    import_ok = test_imports()
    
    # 최종 결과
    print("\n" + "=" * 50)
    if structure_ok and import_ok:
        print("✅ PyQt5 GUI 구현 완료!")
        print("\n주요 기능:")
        print("  • 다크 테마 적용")
        print("  • 4단계 스텝 인디케이터")
        print("  • 로그인 화면 (Jira 연동 옵션)")
        print("  • DB Code 선택 화면")
        print("  • Jira Issue 검색 및 선택 화면")
        print("  • 옵션 설정 화면")
        print("  • 비동기 처리 지원 (QThread)")
        sys.exit(0)
    else:
        print("❌ 일부 문제가 발견되었습니다.")
        sys.exit(1)