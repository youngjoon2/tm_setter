"""PyQt5 GUI 단위 테스트"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# 테스트를 위한 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# PyQt5 모듈 모킹 (GUI 없이 테스트)
sys.modules['PyQt5'] = MagicMock()
sys.modules['PyQt5.QtWidgets'] = MagicMock()
sys.modules['PyQt5.QtCore'] = MagicMock()
sys.modules['PyQt5.QtGui'] = MagicMock()


class TestAnimations(unittest.TestCase):
    """애니메이션 헬퍼 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        from utils.animations import AnimationHelper
        self.animation_helper = AnimationHelper()
        
    def test_fade_in_animation(self):
        """페이드 인 애니메이션 테스트"""
        widget = Mock()
        animation = self.animation_helper.fade_in(widget, duration=300)
        self.assertIsNotNone(animation)
        
    def test_fade_out_animation(self):
        """페이드 아웃 애니메이션 테스트"""
        widget = Mock()
        animation = self.animation_helper.fade_out(widget, duration=300)
        self.assertIsNotNone(animation)
        
    def test_slide_animation(self):
        """슬라이드 애니메이션 테스트"""
        widget = Mock()
        widget.geometry = Mock(return_value=Mock(width=Mock(return_value=100), 
                                               height=Mock(return_value=100),
                                               x=Mock(return_value=0),
                                               y=Mock(return_value=0)))
        widget.parent = Mock(return_value=Mock(width=Mock(return_value=800),
                                             height=Mock(return_value=600)))
        
        for direction in ['left', 'right', 'top', 'bottom']:
            animation = self.animation_helper.slide_in(widget, direction=direction)
            self.assertIsNotNone(animation)
            
    def test_bounce_animation(self):
        """바운스 애니메이션 테스트"""
        widget = Mock()
        widget.geometry = Mock(return_value=Mock(x=Mock(return_value=0),
                                               y=Mock(return_value=0),
                                               width=Mock(return_value=100),
                                               height=Mock(return_value=100)))
        animation = self.animation_helper.bounce(widget)
        self.assertIsNotNone(animation)
        
    def test_shake_animation(self):
        """흔들기 애니메이션 테스트"""
        widget = Mock()
        widget.pos = Mock(return_value=Mock(x=Mock(return_value=100),
                                          y=Mock(return_value=100)))
        animation = self.animation_helper.shake(widget, duration=500, amplitude=10)
        self.assertIsNotNone(animation)


class TestLoadingIndicator(unittest.TestCase):
    """로딩 인디케이터 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        with patch('widgets.loading_indicator.QWidget'):
            from widgets.loading_indicator import LoadingIndicator
            self.loading = LoadingIndicator()
            
    def test_show_loading(self):
        """로딩 표시 테스트"""
        self.loading.show_loading("테스트 중...", "상세 정보")
        self.loading.text_label.setText.assert_called_with("테스트 중...")
        self.loading.detail_label.setText.assert_called_with("상세 정보")
        self.loading.progress.start.assert_called_once()
        
    def test_hide_loading(self):
        """로딩 숨김 테스트"""
        self.loading.hide_loading()
        self.loading.progress.stop.assert_called_once()
        self.loading.hide.assert_called_once()


class TestMainWindow(unittest.TestCase):
    """메인 윈도우 테스트"""
    
    @patch('main_pyqt.QMainWindow')
    @patch('main_pyqt.Config')
    @patch('main_pyqt.SessionManager')
    def setUp(self, mock_session, mock_config, mock_window):
        """테스트 설정"""
        from main_pyqt import TMSetterMainWindow
        self.window = TMSetterMainWindow()
        
    def test_window_initialization(self):
        """윈도우 초기화 테스트"""
        self.assertIsNotNone(self.window.config)
        self.assertIsNotNone(self.window.session)
        self.assertIsNone(self.window.jira_credentials)
        
    def test_setup_shortcuts(self):
        """단축키 설정 테스트"""
        self.window.setup_shortcuts()
        # 단축키가 설정되었는지 확인
        
    def test_status_bar_update(self):
        """상태바 업데이트 테스트"""
        self.window.update_status_bar("테스트 메시지")
        self.window.status_bar.showMessage.assert_called_with("테스트 메시지", 5000)
        
    def test_connection_status_update(self):
        """연결 상태 업데이트 테스트"""
        # 연결됨
        self.window.update_connection_status(True)
        self.window.connection_label.setText.assert_called_with("● 연결됨")
        
        # 연결 안됨
        self.window.update_connection_status(False)
        self.window.connection_label.setText.assert_called_with("● 오프라인")
        
    def test_user_info_update(self):
        """사용자 정보 업데이트 테스트"""
        self.window.update_user_info("testuser")
        self.window.user_label.setText.assert_called_with("User: testuser")


class TestViews(unittest.TestCase):
    """뷰 컴포넌트 테스트"""
    
    @patch('pyqt_views.login_view.QWidget')
    def test_login_view_creation(self, mock_widget):
        """로그인 뷰 생성 테스트"""
        from pyqt_views.login_view import LoginView
        view = LoginView()
        self.assertIsNotNone(view)
        
    @patch('pyqt_views.db_code_view.QWidget')
    def test_db_code_view_creation(self, mock_widget):
        """DB Code 뷰 생성 테스트"""
        from pyqt_views.db_code_view import DBCodeView
        view = DBCodeView()
        self.assertIsNotNone(view)
        
    @patch('pyqt_views.jira_issue_view.QWidget')
    def test_jira_issue_view_creation(self, mock_widget):
        """Jira Issue 뷰 생성 테스트"""
        from pyqt_views.jira_issue_view import JiraIssueView
        view = JiraIssueView()
        self.assertIsNotNone(view)
        
    @patch('pyqt_views.options_view.QWidget')
    def test_options_view_creation(self, mock_widget):
        """Options 뷰 생성 테스트"""
        from pyqt_views.options_view import OptionsView
        view = OptionsView()
        self.assertIsNotNone(view)


class TestTheme(unittest.TestCase):
    """테마 테스트"""
    
    def test_dark_theme_colors(self):
        """다크 테마 색상 테스트"""
        from utils.pyqt_theme import PyQtDarkTheme
        
        # 색상 값 확인
        self.assertEqual(PyQtDarkTheme.BG_PRIMARY, "#1a1a1a")
        self.assertEqual(PyQtDarkTheme.BG_SECONDARY, "#2a2a2a")
        self.assertEqual(PyQtDarkTheme.ACCENT_PRIMARY, "#3498db")
        
    def test_stylesheet_generation(self):
        """스타일시트 생성 테스트"""
        from utils.pyqt_theme import PyQtDarkTheme
        
        stylesheet = PyQtDarkTheme.get_stylesheet()
        self.assertIsNotNone(stylesheet)
        self.assertIn("QMainWindow", stylesheet)
        self.assertIn("QPushButton", stylesheet)


if __name__ == '__main__':
    unittest.main()