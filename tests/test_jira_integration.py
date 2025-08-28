"""
Jira API 통합 테스트
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'atlassian_api'))

from controllers.jira_controller import JiraController
from controllers.auth_controller import AuthController


class TestJiraIntegration(unittest.TestCase):
    """Jira 통합 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        self.jira_controller = JiraController()
        self.auth_controller = AuthController()
    
    def test_jira_controller_initialization_without_api(self):
        """API 없이 Jira 컨트롤러 초기화 테스트"""
        controller = JiraController()
        self.assertIsNotNone(controller)
        self.assertFalse(controller.use_real_api)
        self.assertIsNone(controller.jira_client)
    
    @patch('controllers.jira_controller.JiraAPI')
    def test_jira_controller_initialization_with_api(self, mock_jira_api):
        """API 사용 시 Jira 컨트롤러 초기화 테스트"""
        # Mock 설정
        mock_instance = Mock()
        mock_instance.get_current_user.return_value = {
            'displayName': 'Test User',
            'emailAddress': 'test@example.com'
        }
        mock_jira_api.return_value = mock_instance
        
        # 컨트롤러 생성
        controller = JiraController(
            server_url="https://test.atlassian.net",
            user_id="test@example.com",
            password="test-token",
            use_real_api=True
        )
        
        # 검증
        self.assertTrue(controller.use_real_api)
        self.assertIsNotNone(controller.jira_client)
        mock_instance.get_current_user.assert_called_once()
    
    def test_search_issues_with_dummy_data(self):
        """더미 데이터로 이슈 검색 테스트"""
        controller = JiraController()
        issues = controller.search_issues("TM")
        
        self.assertIsInstance(issues, list)
        self.assertTrue(len(issues) > 0)
        
        # 필터링 테스트
        filtered = [i for i in issues if "TM" in i['summary']]
        self.assertTrue(len(filtered) > 0)
    
    @patch('controllers.jira_controller.JiraAPI')
    def test_search_issues_with_real_api(self, mock_jira_api_class):
        """실제 API 사용 시 이슈 검색 테스트"""
        # Mock 설정
        mock_instance = Mock()
        mock_instance.get_current_user.return_value = {'displayName': 'Test User'}
        mock_instance.search_issues.return_value = {
            'issues': [
                {
                    'key': 'TEST-123',
                    'fields': {
                        'summary': 'Test Issue',
                        'status': {'name': 'Open'},
                        'assignee': {'displayName': 'Test User'},
                        'priority': {'name': 'High'},
                        'created': '2024-01-01T10:00:00.000+0000',
                        'issuetype': {'name': 'Task'}
                    }
                }
            ]
        }
        mock_jira_api_class.return_value = mock_instance
        
        # 컨트롤러 생성 및 검색
        controller = JiraController(
            server_url="https://test.atlassian.net",
            user_id="test@example.com",
            password="test-token",
            use_real_api=True
        )
        
        issues = controller.search_issues("test", project="TEST")
        
        # 검증
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['key'], 'TEST-123')
        self.assertEqual(issues[0]['summary'], 'Test Issue')
    
    def test_get_issue_details_with_dummy_data(self):
        """더미 데이터로 이슈 상세 조회 테스트"""
        controller = JiraController()
        details = controller.get_issue_details("TM-101")
        
        self.assertEqual(details['key'], "TM-101")
        self.assertIn('summary', details)
        self.assertIn('description', details)
        self.assertIn('comments', details)
        self.assertIn('attachments', details)
    
    @patch('controllers.jira_controller.JiraAPI')
    def test_create_issue_with_real_api(self, mock_jira_api_class):
        """실제 API 사용 시 이슈 생성 테스트"""
        # Mock 설정
        mock_instance = Mock()
        mock_instance.get_current_user.return_value = {'displayName': 'Test User'}
        mock_instance.create_issue.return_value = {'key': 'TEST-999'}
        mock_jira_api_class.return_value = mock_instance
        
        # 컨트롤러 생성 및 이슈 생성
        controller = JiraController(
            server_url="https://test.atlassian.net",
            user_id="test@example.com",
            password="test-token",
            use_real_api=True
        )
        
        issue_key = controller.create_issue({
            'project': 'TEST',
            'summary': 'New Test Issue',
            'description': 'Test description'
        })
        
        # 검증
        self.assertEqual(issue_key, 'TEST-999')
        mock_instance.create_issue.assert_called_once()
    
    def test_auth_controller_with_jira(self):
        """Jira를 사용한 인증 컨트롤러 테스트"""
        # 로컬 인증 테스트
        result = self.auth_controller.authenticate('admin', 'admin')
        self.assertTrue(result['success'])
        self.assertEqual(result['user_info']['user_id'], 'admin')
    
    @patch('atlassian_api.JiraAPI')
    def test_auth_controller_with_jira_api(self, mock_jira_api_class):
        """Jira API를 사용한 인증 테스트"""
        # Mock 설정
        mock_instance = Mock()
        mock_instance.get_current_user.return_value = {
            'displayName': 'Test User',
            'emailAddress': 'test@example.com'
        }
        mock_jira_api_class.return_value = mock_instance
        
        # atlassian_api 모듈을 auth_controller에 주입
        with patch.dict('sys.modules', {'atlassian_api': Mock(JiraAPI=mock_jira_api_class)}):
            # Jira 인증 테스트
            result = self.auth_controller.authenticate(
                'test@example.com',
                'test-token',
                'https://test.atlassian.net'
            )
        
            # 검증
            self.assertTrue(result['success'])
            self.assertIn('jira_credentials', result)
            self.assertEqual(result['jira_credentials']['url'], 'https://test.atlassian.net')
    
    def test_validate_issue_key(self):
        """이슈 키 형식 검증 테스트"""
        controller = JiraController()
        
        # 유효한 키
        self.assertTrue(controller.validate_issue_key("TM-101"))
        self.assertTrue(controller.validate_issue_key("PROJ-1234"))
        
        # 무효한 키
        self.assertFalse(controller.validate_issue_key("invalid"))
        self.assertFalse(controller.validate_issue_key("TM_101"))
        self.assertFalse(controller.validate_issue_key("tm-101"))
    
    def test_get_issue_transitions(self):
        """이슈 상태 전환 옵션 조회 테스트"""
        controller = JiraController()
        transitions = controller.get_issue_transitions("TM-101")
        
        self.assertIsInstance(transitions, list)
        self.assertTrue(len(transitions) > 0)
        for transition in transitions:
            self.assertIn('id', transition)
            self.assertIn('name', transition)


class TestJiraViewIntegration(unittest.TestCase):
    """Jira View 통합 테스트"""
    
    @patch('tkinter.Frame')
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    def test_login_view_with_jira_option(self, mock_bool_var, mock_string_var, mock_frame):
        """로그인 뷰의 Jira 옵션 테스트"""
        from views.login_view import LoginView
        
        # Mock 앱 객체
        mock_app = Mock()
        mock_app.async_handler = Mock()
        mock_app.session = Mock()
        
        # 로그인 뷰 생성
        mock_parent = Mock()
        view = LoginView(mock_parent, mock_app)
        
        # Jira 관련 변수 확인
        self.assertIsNotNone(view.jira_url_var)
        self.assertIsNotNone(view.use_jira_auth)
    
    @patch('controllers.jira_controller.JiraController')
    def test_jira_issue_view_fetch_issues(self, mock_jira_controller_class):
        """Jira 이슈 뷰의 이슈 가져오기 테스트"""
        # Mock 설정
        mock_instance = Mock()
        mock_instance.search_issues.return_value = [
            {'key': 'TEST-1', 'summary': 'Test Issue 1'},
            {'key': 'TEST-2', 'summary': 'Test Issue 2'}
        ]
        mock_jira_controller_class.return_value = mock_instance
        
        # Mock 앱 객체
        mock_app = Mock()
        mock_app.jira_credentials = {
            'url': 'https://test.atlassian.net',
            'user_id': 'test@example.com',
            'password': 'test-token'
        }
        mock_app.session = Mock()
        mock_app.session.get.return_value = {'item1': 'TEST'}
        
        # tkinter 테스트 환경 설정
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 테스트용 루트 윈도우
        
        try:
            # 뷰 생성 및 이슈 가져오기
            from views.jira_issue_view import JiraIssueView
            view = JiraIssueView(root, mock_app)
            issues = view.fetch_issues()
            
            # 검증
            self.assertEqual(len(issues), 2)
            self.assertEqual(issues[0]['key'], 'TEST-1')
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()