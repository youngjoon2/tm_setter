"""Jira 컨트롤러 - Jira 이슈 관련 비즈니스 로직"""

import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

# atlassian_api 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'atlassian_api'))

try:
    from atlassian_api import JiraAPI
    JIRA_API_AVAILABLE = True
except ImportError:
    JIRA_API_AVAILABLE = False


class JiraController:
    """Jira 이슈 관련 비즈니스 로직 처리"""
    
    def __init__(self, server_url: str = None, user_id: str = None, password: str = None, use_real_api: bool = False):
        self.server_url = server_url or "https://jira.example.com"
        self.user_id = user_id
        self.password = password
        self.cache = {}
        self.use_real_api = use_real_api and JIRA_API_AVAILABLE
        self.jira_client = None
        
        # 실제 API 사용 시 Jira 클라이언트 초기화
        if self.use_real_api and user_id and password:
            try:
                self.jira_client = JiraAPI(
                    domain_url=self.server_url,
                    user_id=self.user_id,
                    password=self.password
                )
                # 연결 테스트
                self.jira_client.get_current_user()
                print(f"Jira API 연결 성공: {self.server_url}")
            except Exception as e:
                print(f"Jira API 연결 실패: {e}")
                self.use_real_api = False
                self.jira_client = None
    
    def search_issues(self, query: str, project: str = None, 
                     max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Jira 이슈 검색
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                jql = ""
                if query:
                    jql = f"text ~ '{query}'"
                if project:
                    jql += f" AND project = {project}" if jql else f"project = {project}"
                if not jql:
                    jql = "ORDER BY created DESC"
                    
                result = self.jira_client.search_issues(jql, max_results)
                
                # API 응답을 표준 형식으로 변환
                issues = []
                for issue in result.get('issues', []):
                    fields = issue.get('fields', {})
                    issues.append({
                        'key': issue.get('key'),
                        'summary': fields.get('summary'),
                        'status': fields.get('status', {}).get('name', 'Unknown'),
                        'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else 'Unassigned',
                        'priority': fields.get('priority', {}).get('name', 'None'),
                        'created': fields.get('created', '').split('T')[0] if fields.get('created') else '',
                        'type': fields.get('issuetype', {}).get('name', 'Task')
                    })
                return issues
                
            except Exception as e:
                print(f"Jira API 검색 실패: {e}")
                # 실패 시 더미 데이터로 폴백
        
        # 더미 데이터 사용 (API 사용 불가 시)
        dummy_issues = [
            {
                'key': 'TM-101',
                'summary': 'TM 설정 자동화 구현',
                'status': 'In Progress',
                'assignee': 'John Doe',
                'priority': 'High',
                'created': '2024-01-15',
                'type': 'Task'
            },
            {
                'key': 'TM-102',
                'summary': 'DB 연결 오류 수정',
                'status': 'Open',
                'assignee': 'Jane Smith',
                'priority': 'Critical',
                'created': '2024-01-16',
                'type': 'Bug'
            },
            {
                'key': 'TM-103',
                'summary': 'UI 개선 작업',
                'status': 'Done',
                'assignee': 'Bob Johnson',
                'priority': 'Medium',
                'created': '2024-01-14',
                'type': 'Improvement'
            }
        ]
        
        # 검색어로 필터링
        if query:
            filtered = []
            for issue in dummy_issues:
                if query.lower() in issue['summary'].lower():
                    filtered.append(issue)
            return filtered
        
        return dummy_issues
    
    def get_issue_details(self, issue_key: str) -> Dict[str, Any]:
        """
        이슈 상세 정보 조회
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                issue = self.jira_client.get_issue(issue_key, expand='changelog,comments,attachment')
                fields = issue.get('fields', {})
                
                # 코멘트 포맷팅
                comments = []
                for comment in fields.get('comment', {}).get('comments', []):
                    comments.append({
                        'author': comment.get('author', {}).get('displayName', 'Unknown'),
                        'body': comment.get('body', ''),
                        'created': comment.get('created', '').replace('T', ' ').split('.')[0]
                    })
                
                # 첨부파일 포맷팅
                attachments = []
                for attachment in fields.get('attachment', []):
                    attachments.append({
                        'filename': attachment.get('filename', ''),
                        'size': f"{attachment.get('size', 0) / 1024:.1f}KB",
                        'created': attachment.get('created', '').split('T')[0]
                    })
                
                return {
                    'key': issue.get('key'),
                    'summary': fields.get('summary', ''),
                    'description': fields.get('description', ''),
                    'status': fields.get('status', {}).get('name', 'Unknown'),
                    'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
                    'reporter': fields.get('reporter', {}).get('displayName', 'Unknown'),
                    'priority': fields.get('priority', {}).get('name', 'None'),
                    'comments': comments,
                    'attachments': attachments
                }
                
            except Exception as e:
                print(f"이슈 상세 조회 실패: {e}")
                # 실패 시 더미 데이터로 폴백
        
        # 더미 데이터 사용
        return {
            'key': issue_key,
            'summary': f'이슈 {issue_key} 상세 정보',
            'description': '이것은 테스트 이슈입니다.',
            'status': 'Open',
            'assignee': 'Current User',
            'reporter': 'Admin',
            'priority': 'High',
            'comments': [
                {'author': 'User1', 'body': '작업 시작했습니다.', 'created': '2024-01-15 10:00'},
                {'author': 'User2', 'body': '진행 상황 확인 부탁드립니다.', 'created': '2024-01-15 14:00'}
            ],
            'attachments': [
                {'filename': 'screenshot.png', 'size': '245KB', 'created': '2024-01-15'}
            ]
        }
    
    def create_issue(self, issue_data: Dict[str, Any]) -> str:
        """
        새 이슈 생성
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                result = self.jira_client.create_issue(
                    project_key=issue_data.get('project', 'TM'),
                    issue_type=issue_data.get('type', 'Task'),
                    summary=issue_data['summary'],
                    description=issue_data.get('description', ''),
                    priority=issue_data.get('priority', 'Medium'),
                    assignee=issue_data.get('assignee')
                )
                return result.get('key', '')
                
            except Exception as e:
                print(f"이슈 생성 실패: {e}")
                # 실패 시 더미 키 반환
        
        # 더미 구현
        return f"TM-{datetime.now().strftime('%H%M%S')}"
    
    def update_issue(self, issue_key: str, updates: Dict[str, Any]) -> bool:
        """
        이슈 업데이트
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                self.jira_client.update_issue(issue_key, updates)
                return True
                
            except Exception as e:
                print(f"이슈 업데이트 실패: {e}")
                return False
        
        # 더미 구현
        print(f"이슈 {issue_key} 업데이트: {updates}")
        return True
    
    def add_comment(self, issue_key: str, comment: str) -> bool:
        """
        이슈에 코멘트 추가
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                self.jira_client.add_comment(issue_key, comment)
                return True
                
            except Exception as e:
                print(f"코멘트 추가 실패: {e}")
                return False
        
        # 더미 구현
        print(f"이슈 {issue_key}에 코멘트 추가: {comment}")
        return True
    
    def attach_file(self, issue_key: str, file_path: str) -> bool:
        """
        이슈에 파일 첨부
        
        TODO: [파일 첨부]
        - 파일 크기 제한 확인
        - 파일 형식 검증
        """
        # TODO: 실제 구현
        # with open(file_path, 'rb') as file:
        #     self.jira_client.add_attachment(issue=issue_key, attachment=file)
        # return True
        
        # 임시 구현
        print(f"이슈 {issue_key}에 파일 첨부: {file_path}")
        return True
    
    def get_my_issues(self, user_id: str = None) -> List[Dict[str, Any]]:
        """
        내 이슈 목록 조회
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                jql = "assignee = currentUser() OR reporter = currentUser()"
                return self.search_issues("", max_results=100)
                
            except Exception as e:
                print(f"내 이슈 조회 실패: {e}")
                # 실패 시 더미 데이터로 폴백
        
        # 더미 구현
        return [
            {
                'key': 'TM-201',
                'summary': '내가 담당한 이슈 1',
                'status': 'In Progress',
                'priority': 'High'
            },
            {
                'key': 'TM-202',
                'summary': '내가 담당한 이슈 2',
                'status': 'Open',
                'priority': 'Medium'
            }
        ]
    
    def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        최근 이슈 목록 조회
        """
        # 실제 API 사용
        if self.use_real_api and self.jira_client:
            try:
                jql = "created >= -7d ORDER BY created DESC"
                result = self.jira_client.search_issues(jql, limit)
                issues = []
                for issue in result.get('issues', []):
                    fields = issue.get('fields', {})
                    issues.append({
                        'key': issue.get('key'),
                        'summary': fields.get('summary'),
                        'status': fields.get('status', {}).get('name', 'Unknown'),
                        'priority': fields.get('priority', {}).get('name', 'None')
                    })
                return issues
                
            except Exception as e:
                print(f"최근 이슈 조회 실패: {e}")
                # 실패 시 더미 데이터로 폴백
        
        # 더미 구현
        return self.search_issues("")[:limit]
    
    def validate_issue_key(self, issue_key: str) -> bool:
        """
        이슈 키 형식 검증
        
        TODO: [형식 검증]
        - 프로젝트 키 확인
        - 이슈 번호 확인
        """
        # Jira 이슈 키 패턴: PROJECT-123
        pattern = r'^[A-Z]{2,}-\d+$'
        return bool(re.match(pattern, issue_key))
    
    def get_issue_transitions(self, issue_key: str) -> List[Dict[str, str]]:
        """
        이슈 상태 전환 옵션 조회
        
        TODO: [워크플로우 조회]
        - 가능한 전환 목록
        - 권한 확인
        """
        # TODO: 실제 구현
        # transitions = self.jira_client.transitions(issue_key)
        # return [{'id': t['id'], 'name': t['name']} for t in transitions]
        
        # 임시 구현
        return [
            {'id': '1', 'name': 'Start Progress'},
            {'id': '2', 'name': 'Resolve Issue'},
            {'id': '3', 'name': 'Close Issue'}
        ]
    
    def transition_issue(self, issue_key: str, transition_id: str) -> bool:
        """
        이슈 상태 전환
        
        TODO: [상태 전환]
        - 전환 실행
        - 검증
        """
        # TODO: 실제 구현
        # self.jira_client.transition_issue(issue_key, transition_id)
        # return True
        
        # 임시 구현
        print(f"이슈 {issue_key} 상태 전환: {transition_id}")
        return True
    
    def _format_issue(self, issue: Any) -> Dict[str, Any]:
        """이슈 데이터 포맷팅 (내부 헬퍼)"""
        # TODO: 실제 Jira 객체 포맷팅
        return {
            'key': str(issue),
            'summary': 'Formatted issue',
            'status': 'Open'
        }
    
    def _format_comment(self, comment: Any) -> Dict[str, str]:
        """코멘트 데이터 포맷팅 (내부 헬퍼)"""
        # TODO: 실제 코멘트 객체 포맷팅
        return {
            'author': 'User',
            'body': 'Comment',
            'created': datetime.now().isoformat()
        }