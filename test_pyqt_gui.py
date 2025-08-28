#!/usr/bin/env python3
"""PyQt5 GUI 테스트 스크립트"""

import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main_pyqt import TMSetterMainWindow
from pyqt_views.login_view import LoginView
from pyqt_views.db_code_view import DBCodeView
from pyqt_views.jira_issue_view import JiraIssueView
from pyqt_views.options_view import OptionsView


class TestPyQtGUI(unittest.TestCase):
    """PyQt5 GUI 테스트"""
    
    @classmethod
    def setUpClass(cls):
        """테스트 클래스 설정"""
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
            
    def setUp(self):
        """각 테스트 전 설정"""
        self.window = TMSetterMainWindow()
        
    def tearDown(self):
        """각 테스트 후 정리"""
        self.window.close()
        
    def test_main_window_creation(self):
        """메인 윈도우 생성 테스트"""
        self.assertIsNotNone(self.window)
        self.assertEqual(self.window.windowTitle(), "TM Setter")
        self.assertEqual(self.window.size().width(), 900)
        self.assertEqual(self.window.size().height(), 700)
        
    def test_view_initialization(self):
        """뷰 초기화 테스트"""
        self.assertIsInstance(self.window.login_view, LoginView)
        self.assertIsInstance(self.window.db_code_view, DBCodeView)
        self.assertIsInstance(self.window.jira_issue_view, JiraIssueView)
        self.assertIsInstance(self.window.options_view, OptionsView)
        
    def test_initial_view(self):
        """초기 뷰 테스트"""
        # 첫 화면이 로그인 뷰인지 확인
        self.assertEqual(self.window.stack.currentWidget(), self.window.login_view)
        
    def test_view_navigation(self):
        """뷰 전환 테스트"""
        # DB Code 뷰로 전환
        self.window.show_view('db_code')
        self.assertEqual(self.window.stack.currentWidget(), self.window.db_code_view)
        
        # Jira Issue 뷰로 전환
        self.window.show_view('jira_issue')
        self.assertEqual(self.window.stack.currentWidget(), self.window.jira_issue_view)
        
        # Options 뷰로 전환
        self.window.show_view('options')
        self.assertEqual(self.window.stack.currentWidget(), self.window.options_view)
        
        # 다시 로그인 뷰로 전환
        self.window.show_view('login')
        self.assertEqual(self.window.stack.currentWidget(), self.window.login_view)
        
    def test_step_indicators(self):
        """스텝 인디케이터 테스트"""
        # 로그인 뷰일 때
        self.window.show_view('login')
        self.assertEqual(self.window.step_indicators['step1'].circle.objectName(), 'stepCircleActive')
        
        # DB Code 뷰일 때
        self.window.show_view('db_code')
        self.assertEqual(self.window.step_indicators['step1'].circle.objectName(), 'stepCircleCompleted')
        self.assertEqual(self.window.step_indicators['step2'].circle.objectName(), 'stepCircleActive')
        
    def test_login_view_components(self):
        """로그인 뷰 컴포넌트 테스트"""
        login_view = self.window.login_view
        
        # 입력 필드 확인
        self.assertIsNotNone(login_view.id_entry)
        self.assertIsNotNone(login_view.pw_entry)
        self.assertIsNotNone(login_view.url_entry)
        
        # 버튼 확인
        self.assertIsNotNone(login_view.login_button)
        self.assertTrue(login_view.login_button.isEnabled())
        
        # Jira 체크박스 확인
        self.assertIsNotNone(login_view.jira_checkbox)
        self.assertFalse(login_view.jira_checkbox.isChecked())
        
    def test_db_code_view_components(self):
        """DB Code 뷰 컴포넌트 테스트"""
        db_view = self.window.db_code_view
        
        # 콤보박스 확인
        self.assertIsNotNone(db_view.item1_combo)
        self.assertIsNotNone(db_view.item2_combo)
        self.assertIsNotNone(db_view.item3_combo)
        
        # 초기 상태 확인
        self.assertTrue(db_view.item1_combo.isEnabled())
        self.assertFalse(db_view.item2_combo.isEnabled())
        self.assertFalse(db_view.item3_combo.isEnabled())
        
        # 버튼 확인
        self.assertIsNotNone(db_view.next_button)
        self.assertFalse(db_view.next_button.isEnabled())
        
    def test_jira_issue_view_components(self):
        """Jira Issue 뷰 컴포넌트 테스트"""
        jira_view = self.window.jira_issue_view
        
        # 검색 입력 필드 확인
        self.assertIsNotNone(jira_view.search_input)
        self.assertIsNotNone(jira_view.search_button)
        
        # 테이블 확인
        self.assertIsNotNone(jira_view.issues_table)
        self.assertEqual(jira_view.issues_table.columnCount(), 6)
        
        # 버튼 확인
        self.assertIsNotNone(jira_view.next_button)
        self.assertFalse(jira_view.next_button.isEnabled())
        
    def test_options_view_components(self):
        """옵션 뷰 컴포넌트 테스트"""
        options_view = self.window.options_view
        
        # 체크박스 확인
        self.assertIsNotNone(options_view.auto_sync_checkbox)
        self.assertIsNotNone(options_view.notification_checkbox)
        self.assertIsNotNone(options_view.auto_backup_checkbox)
        
        # 초기 상태 확인
        self.assertTrue(options_view.auto_sync_checkbox.isChecked())
        self.assertTrue(options_view.notification_checkbox.isChecked())
        
        # 버튼 확인
        self.assertIsNotNone(options_view.finish_button)
        self.assertTrue(options_view.finish_button.isEnabled())


def run_tests():
    """테스트 실행"""
    print("PyQt5 GUI 테스트 시작...")
    print("-" * 50)
    
    # 테스트 로더
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPyQtGUI)
    
    # 테스트 러너
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("-" * 50)
    if result.wasSuccessful():
        print("✅ 모든 테스트 통과!")
    else:
        print(f"❌ 실패한 테스트: {len(result.failures)}")
        print(f"❌ 에러 발생: {len(result.errors)}")
        
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)