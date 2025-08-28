"""데이터베이스 작업 컨트롤러"""

from typing import List, Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.database import DatabaseManager

class DBController:
    """데이터베이스 작업 관리 컨트롤러"""
    
    def __init__(self, db_path: str = None):
        self.db_manager = DatabaseManager(db_path)
    
    def get_db_codes(self) -> Dict[str, List[Dict[str, Any]]]:
        """DB Code를 카테고리별로 정리하여 반환"""
        try:
            # 모든 카테고리 가져오기
            categories = self.db_manager.get_db_code_categories()
            
            # 카테고리별로 코드 정리
            result = {}
            for category in categories:
                codes = self.db_manager.get_db_codes(category=category)
                # 코드와 설명을 결합한 형태로 변환
                result[category] = [
                    {
                        'code': code['code'],
                        'description': code['description'],
                        'display': f"{code['code']} - {code['description']}"
                    }
                    for code in codes
                ]
            
            # 카테고리가 없는 경우 샘플 데이터 반환
            if not result:
                result = self.get_sample_db_codes()
            
            return result
            
        except Exception as e:
            print(f"DB Code 조회 실패: {e}")
            # 에러 발생 시 샘플 데이터 반환
            return self.get_sample_db_codes()
    
    def get_sample_db_codes(self) -> Dict[str, List[Dict[str, Any]]]:
        """샘플 DB Code 데이터"""
        return {
            "Production": [
                {'code': 'DB001', 'description': 'Production Database', 
                 'display': 'DB001 - Production Database'},
                {'code': 'DB002', 'description': 'Production Backup', 
                 'display': 'DB002 - Production Backup'},
            ],
            "Development": [
                {'code': 'DB003', 'description': 'Development Database', 
                 'display': 'DB003 - Development Database'},
                {'code': 'DB004', 'description': 'Development Test', 
                 'display': 'DB004 - Development Test'},
            ],
            "Testing": [
                {'code': 'DB005', 'description': 'Testing Database', 
                 'display': 'DB005 - Testing Database'},
                {'code': 'DB006', 'description': 'QA Database', 
                 'display': 'DB006 - QA Database'},
            ]
        }
    
    def save_session(self, user_id: str, db_codes: Dict[str, Any], 
                    selected_issue: str, options: Dict[str, Any]) -> bool:
        """세션 정보를 데이터베이스에 저장"""
        try:
            # 사용자 생성 또는 업데이트
            if not self.db_manager.get_user(user_id):
                self.db_manager.create_user(user_id, user_id)  # 임시로 user_id를 name으로 사용
            
            # 세션 저장
            session_id = self.db_manager.create_session(
                user_id=user_id,
                db_codes=db_codes,
                selected_issue=selected_issue,
                options=options
            )
            
            return session_id > 0
            
        except Exception as e:
            print(f"세션 저장 실패: {e}")
            return False
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """사용자의 최근 작업 이력 조회"""
        try:
            sessions = self.db_manager.get_user_sessions(user_id, limit)
            return sessions
        except Exception as e:
            print(f"사용자 이력 조회 실패: {e}")
            return []
    
    def cache_jira_issues(self, issues: List[Dict[str, Any]]):
        """Jira 이슈를 캐시에 저장"""
        try:
            for issue in issues:
                self.db_manager.cache_jira_issue(
                    issue_key=issue.get('key', ''),
                    summary=issue.get('summary', ''),
                    status=issue.get('status', ''),
                    assignee=issue.get('assignee', ''),
                    issue_type=issue.get('type', ''),
                    data=issue
                )
        except Exception as e:
            print(f"Jira 이슈 캐싱 실패: {e}")
    
    def get_cached_jira_issues(self, max_age_minutes: int = 60) -> List[Dict[str, Any]]:
        """캐시된 Jira 이슈 조회"""
        try:
            cached_issues = self.db_manager.get_cached_issues(max_age_minutes)
            # 필요한 형태로 변환
            issues = []
            for cached in cached_issues:
                issue = cached['data'] if cached['data'] else {}
                issue.update({
                    'key': cached['issue_key'],
                    'summary': cached['summary'],
                    'status': cached['status'],
                    'assignee': cached['assignee'],
                    'type': cached['issue_type']
                })
                issues.append(issue)
            return issues
        except Exception as e:
            print(f"캐시된 Jira 이슈 조회 실패: {e}")
            return []
    
    def get_settings(self) -> Dict[str, Any]:
        """애플리케이션 설정 조회"""
        try:
            settings = {
                'sw_versions': self.db_manager.get_setting('sw_versions', [
                    "v1.0.0", "v1.1.0", "v1.2.0", "v2.0.0"
                ]),
                'recent_repos': self.db_manager.get_setting('recent_repos', []),
                'theme': self.db_manager.get_setting('theme', 'dark'),
                'auto_login': self.db_manager.get_setting('auto_login', False),
            }
            return settings
        except Exception as e:
            print(f"설정 조회 실패: {e}")
            return {
                'sw_versions': ["v1.0.0", "v1.1.0", "v1.2.0", "v2.0.0"],
                'recent_repos': [],
                'theme': 'dark',
                'auto_login': False
            }
    
    def save_settings(self, settings: Dict[str, Any]):
        """애플리케이션 설정 저장"""
        try:
            for key, value in settings.items():
                self.db_manager.set_setting(key, value)
        except Exception as e:
            print(f"설정 저장 실패: {e}")
    
    def close(self):
        """데이터베이스 연결 종료"""
        self.db_manager.close()