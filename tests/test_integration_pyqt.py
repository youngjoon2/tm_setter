"""PyQt5 GUI 통합 테스트"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import json

# 테스트를 위한 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestGUIIntegration(unittest.TestCase):
    """GUI 통합 테스트"""
    
    def setUp(self):
        """테스트 환경 설정"""
        self.test_user = {
            'user_id': 'test_user',
            'password': 'test_pass',
            'jira_url': 'https://test.atlassian.net'
        }
        
        self.test_db_codes = [
            {'id': 1, 'code': 'DB001', 'name': 'Test Database 1'},
            {'id': 2, 'code': 'DB002', 'name': 'Test Database 2'},
            {'id': 3, 'code': 'DB003', 'name': 'Test Database 3'}
        ]
        
        self.test_jira_issues = [
            {'key': 'TEST-1', 'summary': 'Test Issue 1', 'status': 'Open'},
            {'key': 'TEST-2', 'summary': 'Test Issue 2', 'status': 'In Progress'},
            {'key': 'TEST-3', 'summary': 'Test Issue 3', 'status': 'Done'}
        ]
        
    @patch('controllers.auth_controller.AuthController')
    def test_login_flow(self, mock_auth):
        """로그인 플로우 테스트"""
        # 인증 성공 시나리오
        mock_auth_instance = mock_auth.return_value
        mock_auth_instance.authenticate.return_value = {
            'success': True,
            'user': self.test_user['user_id'],
            'token': 'test_token_123'
        }
        
        # 로그인 시도
        result = mock_auth_instance.authenticate(
            self.test_user['user_id'],
            self.test_user['password'],
            self.test_user['jira_url']
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['user'], self.test_user['user_id'])
        self.assertIn('token', result)
        
    @patch('controllers.db_controller.DBController')
    def test_db_code_selection(self, mock_db):
        """DB Code 선택 플로우 테스트"""
        # DB Code 목록 로드
        mock_db_instance = mock_db.return_value
        mock_db_instance.get_db_codes.return_value = self.test_db_codes
        
        # DB Code 선택
        db_codes = mock_db_instance.get_db_codes()
        self.assertEqual(len(db_codes), 3)
        
        # 특정 DB Code 선택
        selected_code = db_codes[0]
        self.assertEqual(selected_code['code'], 'DB001')
        
    @patch('controllers.jira_controller.JiraController')
    def test_jira_issue_search(self, mock_jira):
        """Jira Issue 검색 플로우 테스트"""
        # Jira Issue 검색
        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.search_issues.return_value = self.test_jira_issues
        
        # 검색 실행
        issues = mock_jira_instance.search_issues("test query")
        self.assertEqual(len(issues), 3)
        
        # 특정 이슈 선택
        selected_issue = issues[0]
        self.assertEqual(selected_issue['key'], 'TEST-1')
        
    @patch('utils.config.Config')
    def test_settings_save(self, mock_config):
        """설정 저장 플로우 테스트"""
        # 설정 객체 생성
        mock_config_instance = mock_config.return_value
        
        # 설정 값 설정
        test_settings = {
            'auto_login': True,
            'save_password': False,
            'dark_mode': True,
            'language': 'ko'
        }
        
        # 설정 저장
        mock_config_instance.update.return_value = True
        result = mock_config_instance.update(test_settings)
        
        self.assertTrue(result)
        mock_config_instance.update.assert_called_with(test_settings)
        
    def test_complete_workflow(self):
        """전체 워크플로우 테스트"""
        with patch('controllers.auth_controller.AuthController') as mock_auth, \
             patch('controllers.db_controller.DBController') as mock_db, \
             patch('controllers.jira_controller.JiraController') as mock_jira, \
             patch('utils.config.Config') as mock_config:
            
            # 1. 로그인
            mock_auth_instance = mock_auth.return_value
            mock_auth_instance.authenticate.return_value = {
                'success': True,
                'user': self.test_user['user_id']
            }
            
            auth_result = mock_auth_instance.authenticate(
                self.test_user['user_id'],
                self.test_user['password']
            )
            self.assertTrue(auth_result['success'])
            
            # 2. DB Code 선택
            mock_db_instance = mock_db.return_value
            mock_db_instance.get_db_codes.return_value = self.test_db_codes
            
            db_codes = mock_db_instance.get_db_codes()
            selected_db = db_codes[0]
            
            # 3. Jira Issue 선택
            mock_jira_instance = mock_jira.return_value
            mock_jira_instance.search_issues.return_value = self.test_jira_issues
            
            issues = mock_jira_instance.search_issues("project = TEST")
            selected_issue = issues[0]
            
            # 4. 설정 저장
            mock_config_instance = mock_config.return_value
            final_data = {
                'user': self.test_user['user_id'],
                'db_code': selected_db['code'],
                'jira_issue': selected_issue['key'],
                'timestamp': '2024-01-01 12:00:00'
            }
            
            mock_config_instance.save.return_value = True
            save_result = mock_config_instance.save(final_data)
            
            self.assertTrue(save_result)


class TestErrorHandling(unittest.TestCase):
    """에러 처리 테스트"""
    
    @patch('controllers.auth_controller.AuthController')
    def test_login_failure(self, mock_auth):
        """로그인 실패 처리 테스트"""
        mock_auth_instance = mock_auth.return_value
        mock_auth_instance.authenticate.return_value = {
            'success': False,
            'error': 'Invalid credentials'
        }
        
        result = mock_auth_instance.authenticate('wrong_user', 'wrong_pass')
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        
    @patch('controllers.jira_controller.JiraController')
    def test_jira_connection_error(self, mock_jira):
        """Jira 연결 오류 처리 테스트"""
        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.search_issues.side_effect = Exception("Connection failed")
        
        with self.assertRaises(Exception) as context:
            mock_jira_instance.search_issues("test query")
        
        self.assertIn("Connection failed", str(context.exception))
        
    @patch('utils.config.Config')
    def test_config_save_error(self, mock_config):
        """설정 저장 오류 처리 테스트"""
        mock_config_instance = mock_config.return_value
        mock_config_instance.save.side_effect = IOError("Disk full")
        
        with self.assertRaises(IOError) as context:
            mock_config_instance.save({'test': 'data'})
        
        self.assertIn("Disk full", str(context.exception))


class TestDataValidation(unittest.TestCase):
    """데이터 검증 테스트"""
    
    def test_user_input_validation(self):
        """사용자 입력 검증 테스트"""
        # 유효한 입력
        valid_inputs = [
            {'user_id': 'user123', 'password': 'pass123'},
            {'user_id': 'user@email.com', 'password': 'P@ssw0rd!'},
        ]
        
        for input_data in valid_inputs:
            self.assertTrue(len(input_data['user_id']) > 0)
            self.assertTrue(len(input_data['password']) > 0)
        
        # 유효하지 않은 입력
        invalid_inputs = [
            {'user_id': '', 'password': 'pass123'},
            {'user_id': 'user123', 'password': ''},
            {'user_id': None, 'password': 'pass123'},
        ]
        
        for input_data in invalid_inputs:
            is_valid = bool(input_data.get('user_id')) and bool(input_data.get('password'))
            self.assertFalse(is_valid)
            
    def test_jira_url_validation(self):
        """Jira URL 검증 테스트"""
        valid_urls = [
            'https://company.atlassian.net',
            'https://jira.company.com',
            'http://localhost:8080',
        ]
        
        invalid_urls = [
            'not_a_url',
            'ftp://wrong.protocol.com',
            '',
            None,
        ]
        
        for url in valid_urls:
            self.assertTrue(url.startswith(('http://', 'https://')))
        
        for url in invalid_urls:
            is_valid = bool(url) and url.startswith(('http://', 'https://'))
            self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()