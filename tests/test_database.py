"""데이터베이스 기능 테스트"""

import unittest
import os
import sys
import tempfile
import json
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.database import DatabaseManager
from controllers.db_controller import DBController

class TestDatabaseManager(unittest.TestCase):
    """DatabaseManager 테스트"""
    
    def setUp(self):
        """테스트 환경 설정"""
        # 임시 데이터베이스 파일 생성
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # DatabaseManager 인스턴스 생성
        self.db_manager = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """테스트 정리"""
        # 데이터베이스 연결 종료
        if hasattr(self, 'db_manager'):
            self.db_manager.close()
        
        # 임시 파일 삭제
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_database_initialization(self):
        """데이터베이스 초기화 테스트"""
        # 테이블 존재 확인
        with self.db_manager.connect() as conn:
            cursor = conn.cursor()
            
            # 테이블 목록 조회
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # 필요한 테이블이 모두 있는지 확인
            required_tables = ['users', 'db_codes', 'jira_issues_cache', 'sessions', 'settings']
            for table in required_tables:
                self.assertIn(table, tables)
    
    def test_user_operations(self):
        """사용자 관련 작업 테스트"""
        # 사용자 생성
        user_id = self.db_manager.create_user('test_user', 'Test User')
        self.assertIsNotNone(user_id)
        
        # 사용자 조회
        user = self.db_manager.get_user('test_user')
        self.assertIsNotNone(user)
        self.assertEqual(user['user_id'], 'test_user')
        self.assertEqual(user['user_name'], 'Test User')
    
    def test_db_codes_operations(self):
        """DB Code 관련 작업 테스트"""
        # DB Code 추가
        code_id = self.db_manager.add_db_code('TEST001', 'Test Database', 'Testing')
        self.assertIsNotNone(code_id)
        
        # DB Code 조회
        codes = self.db_manager.get_db_codes()
        self.assertGreater(len(codes), 0)
        
        # 카테고리별 조회
        test_codes = self.db_manager.get_db_codes(category='Testing')
        self.assertTrue(any(code['code'] == 'TEST001' for code in test_codes))
        
        # 카테고리 목록 조회
        categories = self.db_manager.get_db_code_categories()
        self.assertIn('Testing', categories)
    
    def test_jira_cache_operations(self):
        """Jira Issue 캐시 작업 테스트"""
        # Issue 캐싱
        issue_data = {
            'key': 'TEST-123',
            'summary': 'Test Issue',
            'status': 'Open',
            'assignee': 'test_user',
            'type': 'Bug',
            'description': 'Test description'
        }
        
        self.db_manager.cache_jira_issue(
            issue_key='TEST-123',
            summary='Test Issue',
            status='Open',
            assignee='test_user',
            issue_type='Bug',
            data=issue_data
        )
        
        # 캐시된 Issue 조회
        cached_issues = self.db_manager.get_cached_issues(max_age_minutes=60)
        self.assertGreater(len(cached_issues), 0)
        
        # 캐시된 데이터 확인
        cached_issue = next((i for i in cached_issues if i['issue_key'] == 'TEST-123'), None)
        self.assertIsNotNone(cached_issue)
        self.assertEqual(cached_issue['summary'], 'Test Issue')
        self.assertEqual(cached_issue['data']['description'], 'Test description')
    
    def test_session_operations(self):
        """세션 관련 작업 테스트"""
        # 사용자 생성
        self.db_manager.create_user('session_user', 'Session User')
        
        # 세션 생성
        db_codes = {'item1': 'DB001', 'item2': 'DB002', 'item3': 'DB003'}
        options = {'repo_name': 'test-repo', 'sw_version': 'v1.0.0'}
        
        session_id = self.db_manager.create_session(
            user_id='session_user',
            db_codes=db_codes,
            selected_issue='TEST-456',
            options=options
        )
        self.assertIsNotNone(session_id)
        
        # 세션 조회
        sessions = self.db_manager.get_user_sessions('session_user', limit=10)
        self.assertGreater(len(sessions), 0)
        
        # 세션 데이터 확인
        session = sessions[0]
        self.assertEqual(session['user_id'], 'session_user')
        self.assertEqual(session['selected_issue'], 'TEST-456')
        self.assertEqual(session['db_codes']['item1'], 'DB001')
        self.assertEqual(session['options']['repo_name'], 'test-repo')
    
    def test_settings_operations(self):
        """설정 관련 작업 테스트"""
        # 설정 저장
        test_setting = ['v1.0.0', 'v1.1.0', 'v2.0.0']
        self.db_manager.set_setting('sw_versions', test_setting)
        
        # 설정 조회
        retrieved_setting = self.db_manager.get_setting('sw_versions')
        self.assertEqual(retrieved_setting, test_setting)
        
        # 존재하지 않는 설정 조회 (기본값 반환)
        default_value = ['default']
        result = self.db_manager.get_setting('non_existent', default=default_value)
        self.assertEqual(result, default_value)

class TestDBController(unittest.TestCase):
    """DBController 테스트"""
    
    def setUp(self):
        """테스트 환경 설정"""
        # 임시 데이터베이스 파일 생성
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # DBController 인스턴스 생성
        self.db_controller = DBController(self.db_path)
    
    def tearDown(self):
        """테스트 정리"""
        # 데이터베이스 연결 종료
        if hasattr(self, 'db_controller'):
            self.db_controller.close()
        
        # 임시 파일 삭제
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_get_db_codes(self):
        """DB Code 조회 테스트"""
        db_codes = self.db_controller.get_db_codes()
        
        # 결과가 딕셔너리인지 확인
        self.assertIsInstance(db_codes, dict)
        
        # 각 카테고리의 값이 리스트인지 확인
        for category, codes in db_codes.items():
            self.assertIsInstance(codes, list)
            
            # 각 코드가 필요한 필드를 가지고 있는지 확인
            for code in codes:
                self.assertIn('code', code)
                self.assertIn('description', code)
                self.assertIn('display', code)
    
    def test_save_and_get_session(self):
        """세션 저장 및 조회 테스트"""
        # 세션 저장
        saved = self.db_controller.save_session(
            user_id='test_user',
            db_codes={'item1': 'DB001', 'item2': 'DB002'},
            selected_issue='TEST-789',
            options={'repo_name': 'my-repo', 'sw_version': 'v1.2.0'}
        )
        self.assertTrue(saved)
        
        # 세션 이력 조회
        history = self.db_controller.get_user_history('test_user', limit=5)
        self.assertGreater(len(history), 0)
        
        # 저장된 데이터 확인
        recent_session = history[0]
        self.assertEqual(recent_session['user_id'], 'test_user')
        self.assertEqual(recent_session['selected_issue'], 'TEST-789')
    
    def test_jira_cache(self):
        """Jira Issue 캐싱 테스트"""
        # Issue 목록 캐싱
        issues = [
            {'key': 'CACHE-001', 'summary': 'Cache Test 1', 'status': 'Open', 
             'assignee': 'user1', 'type': 'Task'},
            {'key': 'CACHE-002', 'summary': 'Cache Test 2', 'status': 'Done',
             'assignee': 'user2', 'type': 'Bug'}
        ]
        
        self.db_controller.cache_jira_issues(issues)
        
        # 캐시된 Issue 조회
        cached = self.db_controller.get_cached_jira_issues(max_age_minutes=60)
        self.assertGreaterEqual(len(cached), 2)
        
        # 캐시된 데이터 확인
        cached_keys = [issue['key'] for issue in cached]
        self.assertIn('CACHE-001', cached_keys)
        self.assertIn('CACHE-002', cached_keys)
    
    def test_settings(self):
        """설정 관리 테스트"""
        # 설정 조회 (기본값 포함)
        settings = self.db_controller.get_settings()
        self.assertIn('sw_versions', settings)
        self.assertIn('theme', settings)
        self.assertIn('auto_login', settings)
        
        # 설정 저장
        new_settings = {
            'sw_versions': ['v3.0.0', 'v3.1.0'],
            'theme': 'dark',
            'auto_login': True
        }
        self.db_controller.save_settings(new_settings)
        
        # 저장된 설정 확인
        retrieved = self.db_controller.get_settings()
        self.assertEqual(retrieved['sw_versions'], ['v3.0.0', 'v3.1.0'])
        self.assertTrue(retrieved['auto_login'])

if __name__ == '__main__':
    unittest.main()