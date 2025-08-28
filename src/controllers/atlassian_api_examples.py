"""Atlassian API (Jira, Confluence, Bitbucket) 사용 예제"""

import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Any, Optional
import json
from datetime import datetime


class JiraAPI:
    """Jira REST API 클라이언트"""
    
    def __init__(self, server_url: str, email: str, api_token: str):
        """
        Jira API 초기화
        
        Args:
            server_url: Jira 서버 URL (예: https://yourcompany.atlassian.net)
            email: 사용자 이메일
            api_token: API 토큰 (https://id.atlassian.com/manage/api-tokens 에서 생성)
        """
        self.server_url = server_url.rstrip('/')
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    # ========== 이슈 검색 ==========
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """
        JQL로 이슈 검색
        
        Example:
            jql = "project = PROJ AND status = 'In Progress'"
        """
        url = f"{self.server_url}/rest/api/3/search"
        
        params = {
            'jql': jql,
            'maxResults': max_results,
            'fields': 'summary,status,assignee,priority,created,updated,description'
        }
        
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data['issues']
    
    # ========== 이슈 생성 ==========
    def create_issue(self, project_key: str, summary: str, 
                    issue_type: str = 'Task', description: str = None) -> str:
        """
        새 이슈 생성
        
        Example:
            issue_key = create_issue('PROJ', '새로운 작업', 'Bug', '버그 설명')
        """
        url = f"{self.server_url}/rest/api/3/issue"
        
        issue_data = {
            'fields': {
                'project': {'key': project_key},
                'summary': summary,
                'issuetype': {'name': issue_type},
            }
        }
        
        if description:
            # Atlassian Document Format (ADF) 사용
            issue_data['fields']['description'] = {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': description
                            }
                        ]
                    }
                ]
            }
        
        response = requests.post(url, auth=self.auth, headers=self.headers, 
                                json=issue_data)
        response.raise_for_status()
        
        return response.json()['key']
    
    # ========== 이슈 업데이트 ==========
    def update_issue(self, issue_key: str, fields: Dict) -> bool:
        """
        이슈 업데이트
        
        Example:
            update_issue('PROJ-123', {'summary': '수정된 제목', 'priority': {'name': 'High'}})
        """
        url = f"{self.server_url}/rest/api/3/issue/{issue_key}"
        
        update_data = {'fields': fields}
        
        response = requests.put(url, auth=self.auth, headers=self.headers,
                               json=update_data)
        response.raise_for_status()
        
        return response.status_code == 204
    
    # ========== 코멘트 추가 ==========
    def add_comment(self, issue_key: str, comment_text: str) -> bool:
        """
        이슈에 코멘트 추가
        """
        url = f"{self.server_url}/rest/api/3/issue/{issue_key}/comment"
        
        comment_data = {
            'body': {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': comment_text
                            }
                        ]
                    }
                ]
            }
        }
        
        response = requests.post(url, auth=self.auth, headers=self.headers,
                                json=comment_data)
        response.raise_for_status()
        
        return response.status_code == 201
    
    # ========== 워크플로우 전환 ==========
    def transition_issue(self, issue_key: str, transition_name: str) -> bool:
        """
        이슈 상태 변경 (예: To Do -> In Progress)
        """
        # 가능한 전환 조회
        transitions_url = f"{self.server_url}/rest/api/3/issue/{issue_key}/transitions"
        response = requests.get(transitions_url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        transitions = response.json()['transitions']
        
        # 원하는 전환 찾기
        transition_id = None
        for t in transitions:
            if t['name'].lower() == transition_name.lower():
                transition_id = t['id']
                break
        
        if not transition_id:
            raise ValueError(f"전환 '{transition_name}'을 찾을 수 없습니다.")
        
        # 전환 실행
        transition_data = {'transition': {'id': transition_id}}
        response = requests.post(transitions_url, auth=self.auth, headers=self.headers,
                                json=transition_data)
        response.raise_for_status()
        
        return response.status_code == 204
    
    # ========== 첨부파일 업로드 ==========
    def add_attachment(self, issue_key: str, file_path: str) -> bool:
        """
        이슈에 파일 첨부
        """
        url = f"{self.server_url}/rest/api/3/issue/{issue_key}/attachments"
        
        headers = {
            'X-Atlassian-Token': 'no-check'  # XSRF 체크 비활성화
        }
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f)}
            response = requests.post(url, auth=self.auth, headers=headers, files=files)
        
        response.raise_for_status()
        return response.status_code == 200
    
    # ========== 사용자 검색 ==========
    def search_users(self, query: str) -> List[Dict]:
        """
        사용자 검색
        """
        url = f"{self.server_url}/rest/api/3/user/search"
        params = {'query': query}
        
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()


class ConfluenceAPI:
    """Confluence REST API 클라이언트"""
    
    def __init__(self, server_url: str, email: str, api_token: str):
        self.server_url = server_url.rstrip('/')
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    # ========== 페이지 생성 ==========
    def create_page(self, space_key: str, title: str, content: str, 
                   parent_id: str = None) -> str:
        """
        Confluence 페이지 생성
        
        Example:
            page_id = create_page('DEV', '기술 문서', '<h1>내용</h1>')
        """
        url = f"{self.server_url}/rest/api/content"
        
        page_data = {
            'type': 'page',
            'title': title,
            'space': {'key': space_key},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }
        
        if parent_id:
            page_data['ancestors'] = [{'id': parent_id}]
        
        response = requests.post(url, auth=self.auth, headers=self.headers,
                                json=page_data)
        response.raise_for_status()
        
        return response.json()['id']
    
    # ========== 페이지 검색 ==========
    def search_content(self, cql: str, limit: int = 25) -> List[Dict]:
        """
        CQL(Confluence Query Language)로 컨텐츠 검색
        
        Example:
            cql = "space = DEV AND type = page AND text ~ 'api'"
        """
        url = f"{self.server_url}/rest/api/content/search"
        params = {
            'cql': cql,
            'limit': limit
        }
        
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()['results']
    
    # ========== 페이지 업데이트 ==========
    def update_page(self, page_id: str, title: str, content: str, version: int) -> bool:
        """
        페이지 업데이트 (버전 번호 필요)
        """
        url = f"{self.server_url}/rest/api/content/{page_id}"
        
        update_data = {
            'version': {'number': version + 1},
            'title': title,
            'type': 'page',
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }
        
        response = requests.put(url, auth=self.auth, headers=self.headers,
                               json=update_data)
        response.raise_for_status()
        
        return response.status_code == 200
    
    # ========== 첨부파일 업로드 ==========
    def attach_file_to_page(self, page_id: str, file_path: str) -> bool:
        """
        페이지에 파일 첨부
        """
        url = f"{self.server_url}/rest/api/content/{page_id}/child/attachment"
        
        headers = {
            'X-Atlassian-Token': 'no-check'
        }
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f)}
            response = requests.post(url, auth=self.auth, headers=headers, files=files)
        
        response.raise_for_status()
        return response.status_code == 200


class BitbucketAPI:
    """Bitbucket REST API 클라이언트"""
    
    def __init__(self, workspace: str, username: str, app_password: str):
        """
        Bitbucket API 초기화
        
        Args:
            workspace: 워크스페이스 이름
            username: Bitbucket 사용자명
            app_password: 앱 비밀번호 (https://bitbucket.org/account/settings/app-passwords/)
        """
        self.base_url = "https://api.bitbucket.org/2.0"
        self.workspace = workspace
        self.auth = HTTPBasicAuth(username, app_password)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    # ========== 저장소 목록 ==========
    def list_repositories(self) -> List[Dict]:
        """
        워크스페이스의 저장소 목록 조회
        """
        url = f"{self.base_url}/repositories/{self.workspace}"
        
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        return response.json()['values']
    
    # ========== Pull Request 생성 ==========
    def create_pull_request(self, repo_slug: str, title: str, 
                          source_branch: str, dest_branch: str = 'main',
                          description: str = None) -> str:
        """
        Pull Request 생성
        
        Example:
            pr_id = create_pull_request('my-repo', 'Feature 추가', 
                                       'feature-branch', 'main')
        """
        url = f"{self.base_url}/repositories/{self.workspace}/{repo_slug}/pullrequests"
        
        pr_data = {
            'title': title,
            'source': {
                'branch': {'name': source_branch}
            },
            'destination': {
                'branch': {'name': dest_branch}
            }
        }
        
        if description:
            pr_data['description'] = description
        
        response = requests.post(url, auth=self.auth, headers=self.headers,
                                json=pr_data)
        response.raise_for_status()
        
        return response.json()['id']
    
    # ========== 브랜치 생성 ==========
    def create_branch(self, repo_slug: str, branch_name: str, 
                     from_branch: str = 'main') -> bool:
        """
        새 브랜치 생성
        """
        url = f"{self.base_url}/repositories/{self.workspace}/{repo_slug}/refs/branches"
        
        branch_data = {
            'name': branch_name,
            'target': {
                'hash': from_branch  # 브랜치명 또는 커밋 해시
            }
        }
        
        response = requests.post(url, auth=self.auth, headers=self.headers,
                                json=branch_data)
        response.raise_for_status()
        
        return response.status_code == 201
    
    # ========== 커밋 목록 ==========
    def get_commits(self, repo_slug: str, branch: str = 'main', limit: int = 30) -> List[Dict]:
        """
        커밋 목록 조회
        """
        url = f"{self.base_url}/repositories/{self.workspace}/{repo_slug}/commits/{branch}"
        params = {'pagelen': limit}
        
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()['values']
    
    # ========== 파일 내용 조회 ==========
    def get_file_content(self, repo_slug: str, file_path: str, 
                        branch: str = 'main') -> str:
        """
        저장소의 파일 내용 조회
        """
        url = f"{self.base_url}/repositories/{self.workspace}/{repo_slug}/src/{branch}/{file_path}"
        
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        
        return response.text
    
    # ========== 이슈 생성 (Bitbucket Issues) ==========
    def create_issue(self, repo_slug: str, title: str, 
                    kind: str = 'bug', priority: str = 'major',
                    content: str = None) -> int:
        """
        Bitbucket 이슈 생성
        
        Args:
            kind: bug, enhancement, proposal, task
            priority: trivial, minor, major, critical, blocker
        """
        url = f"{self.base_url}/repositories/{self.workspace}/{repo_slug}/issues"
        
        issue_data = {
            'title': title,
            'kind': kind,
            'priority': priority
        }
        
        if content:
            issue_data['content'] = {'raw': content}
        
        response = requests.post(url, auth=self.auth, headers=self.headers,
                                json=issue_data)
        response.raise_for_status()
        
        return response.json()['id']
    
    # ========== 파이프라인 트리거 ==========
    def trigger_pipeline(self, repo_slug: str, branch: str = 'main') -> str:
        """
        CI/CD 파이프라인 실행
        """
        url = f"{self.base_url}/repositories/{self.workspace}/{repo_slug}/pipelines"
        
        pipeline_data = {
            'target': {
                'ref_type': 'branch',
                'type': 'pipeline_ref_target',
                'ref_name': branch
            }
        }
        
        response = requests.post(url, auth=self.auth, headers=self.headers,
                                json=pipeline_data)
        response.raise_for_status()
        
        return response.json()['uuid']


# ========== 통합 사용 예제 ==========
class AtlassianIntegration:
    """Atlassian 제품군 통합 사용 예제"""
    
    def __init__(self, email: str, jira_token: str, confluence_token: str,
                bitbucket_user: str, bitbucket_password: str):
        self.jira = JiraAPI('https://yourcompany.atlassian.net', email, jira_token)
        self.confluence = ConfluenceAPI('https://yourcompany.atlassian.net', 
                                       email, confluence_token)
        self.bitbucket = BitbucketAPI('yourworkspace', bitbucket_user, bitbucket_password)
    
    def create_feature_workflow(self, feature_name: str, description: str):
        """
        기능 개발 워크플로우 전체 자동화
        
        1. Jira 이슈 생성
        2. Bitbucket 브랜치 생성
        3. Confluence 문서 페이지 생성
        """
        # 1. Jira 이슈 생성
        issue_key = self.jira.create_issue(
            project_key='PROJ',
            summary=f"Feature: {feature_name}",
            issue_type='Story',
            description=description
        )
        print(f"✅ Jira 이슈 생성: {issue_key}")
        
        # 2. Bitbucket 브랜치 생성
        branch_name = f"feature/{issue_key}-{feature_name.lower().replace(' ', '-')}"
        self.bitbucket.create_branch(
            repo_slug='main-repo',
            branch_name=branch_name,
            from_branch='develop'
        )
        print(f"✅ Git 브랜치 생성: {branch_name}")
        
        # 3. Confluence 문서 생성
        doc_content = f"""
        <h1>{feature_name} 기술 명세</h1>
        <p><strong>Jira Issue:</strong> <a href='https://yourcompany.atlassian.net/browse/{issue_key}'>{issue_key}</a></p>
        <p><strong>Git Branch:</strong> {branch_name}</p>
        <h2>개요</h2>
        <p>{description}</p>
        <h2>기술 스펙</h2>
        <p>TODO: 상세 내용 작성</p>
        """
        
        page_id = self.confluence.create_page(
            space_key='DEV',
            title=f"{feature_name} - Technical Specification",
            content=doc_content
        )
        print(f"✅ Confluence 문서 생성: {page_id}")
        
        # 4. Jira 이슈에 링크 추가
        self.jira.add_comment(
            issue_key=issue_key,
            comment_text=f"관련 문서 및 브랜치가 생성되었습니다:\n"
                        f"- Git Branch: {branch_name}\n"
                        f"- Confluence: https://yourcompany.atlassian.net/wiki/pages/{page_id}"
        )
        
        return {
            'jira_issue': issue_key,
            'git_branch': branch_name,
            'confluence_page': page_id
        }


# ========== 사용 예제 ==========
if __name__ == "__main__":
    # Jira 사용 예제
    jira = JiraAPI(
        server_url='https://yourcompany.atlassian.net',
        email='your.email@company.com',
        api_token='your_api_token_here'
    )
    
    # 이슈 검색
    issues = jira.search_issues("project = PROJ AND status = 'In Progress'")
    for issue in issues:
        print(f"{issue['key']}: {issue['fields']['summary']}")
    
    # 이슈 생성
    new_issue = jira.create_issue(
        project_key='PROJ',
        summary='API로 생성된 이슈',
        issue_type='Task',
        description='Python에서 생성한 이슈입니다.'
    )
    print(f"새 이슈 생성됨: {new_issue}")
    
    # Confluence 사용 예제
    confluence = ConfluenceAPI(
        server_url='https://yourcompany.atlassian.net',
        email='your.email@company.com',
        api_token='your_api_token_here'
    )
    
    # 페이지 검색
    pages = confluence.search_content("space = DEV AND text ~ 'python'")
    for page in pages:
        print(f"Page: {page['title']}")
    
    # Bitbucket 사용 예제
    bitbucket = BitbucketAPI(
        workspace='yourworkspace',
        username='your_username',
        app_password='your_app_password'
    )
    
    # 저장소 목록
    repos = bitbucket.list_repositories()
    for repo in repos:
        print(f"Repository: {repo['name']}")