"""
Atlassian API Clients for JIRA, Confluence, and Bitbucket
"""

import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin
import json


class JiraAPI:
    """JIRA REST API Client"""
    
    def __init__(self, domain_url: str, user_id: str, password: str):
        """
        Initialize JIRA API client
        
        Args:
            domain_url: JIRA domain URL (e.g., https://yourdomain.atlassian.net)
            user_id: User email or username
            password: API token or password
        """
        self.domain_url: str = domain_url.rstrip('/')
        self.user_id: str = user_id
        self.password: str = password
        self.auth = (user_id, password)
        self.headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.api_version: str = "/rest/api/3"
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make HTTP request to JIRA API"""
        url: str = f"{self.domain_url}{self.api_version}{endpoint}"
        
        kwargs: Dict[str, Any] = {
            "auth": self.auth,
            "headers": self.headers,
            "params": params
        }
        
        if data and method in ["POST", "PUT", "PATCH"]:
            kwargs["json"] = data
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.text:
                return response.json()
            return {}
        except requests.exceptions.RequestException as e:
            raise Exception(f"JIRA API 요청 실패: {str(e)}")
    
    # Issue 관련 메서드
    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """이슈 조회"""
        return self._request("GET", f"/issue/{issue_key}")
    
    def create_issue(self, project_key: str, issue_type: str, summary: str, description: str = "", **kwargs) -> Dict[str, Any]:
        """이슈 생성"""
        data: Dict[str, Any] = {
            "fields": {
                "project": {"key": project_key},
                "issuetype": {"name": issue_type},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                }
            }
        }
        
        # 추가 필드 병합
        if kwargs:
            data["fields"].update(kwargs)
        
        return self._request("POST", "/issue", data)
    
    def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """이슈 업데이트"""
        data: Dict[str, Any] = {"fields": fields}
        return self._request("PUT", f"/issue/{issue_key}", data)
    
    def delete_issue(self, issue_key: str) -> None:
        """이슈 삭제"""
        self._request("DELETE", f"/issue/{issue_key}")
    
    def add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """이슈에 댓글 추가"""
        data: Dict[str, Any] = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }
        return self._request("POST", f"/issue/{issue_key}/comment", data)
    
    # 프로젝트 관련 메서드
    def get_projects(self) -> List[Dict[str, Any]]:
        """모든 프로젝트 조회"""
        return self._request("GET", "/project")
    
    def get_project(self, project_key: str) -> Dict[str, Any]:
        """특정 프로젝트 조회"""
        return self._request("GET", f"/project/{project_key}")
    
    # 검색 관련 메서드
    def search_issues(self, jql: str, max_results: int = 50, start_at: int = 0) -> Dict[str, Any]:
        """JQL로 이슈 검색"""
        params: Dict[str, Any] = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at
        }
        return self._request("GET", "/search", params=params)
    
    # 사용자 관련 메서드
    def get_current_user(self) -> Dict[str, Any]:
        """현재 사용자 정보 조회"""
        return self._request("GET", "/myself")


class ConfluenceAPI:
    """Confluence REST API Client"""
    
    def __init__(self, domain_url: str, user_id: str, password: str):
        """
        Initialize Confluence API client
        
        Args:
            domain_url: Confluence domain URL (e.g., https://yourdomain.atlassian.net/wiki)
            user_id: User email or username
            password: API token or password
        """
        self.domain_url: str = domain_url.rstrip('/')
        if not self.domain_url.endswith('/wiki'):
            self.domain_url += '/wiki'
        
        self.user_id: str = user_id
        self.password: str = password
        self.auth = (user_id, password)
        self.headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.api_version: str = "/rest/api"
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make HTTP request to Confluence API"""
        url: str = f"{self.domain_url}{self.api_version}{endpoint}"
        
        kwargs: Dict[str, Any] = {
            "auth": self.auth,
            "headers": self.headers,
            "params": params
        }
        
        if data and method in ["POST", "PUT", "PATCH"]:
            kwargs["json"] = data
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.text:
                return response.json()
            return {}
        except requests.exceptions.RequestException as e:
            raise Exception(f"Confluence API 요청 실패: {str(e)}")
    
    # 페이지 관련 메서드
    def get_page_by_id(self, page_id: str, expand: str = "body.storage,version") -> Dict[str, Any]:
        """페이지 ID로 조회"""
        params: Dict[str, str] = {"expand": expand}
        return self._request("GET", f"/content/{page_id}", params=params)
    
    def get_page_by_title(self, space_key: str, title: str) -> Dict[str, Any]:
        """페이지 제목으로 조회"""
        params: Dict[str, str] = {
            "spaceKey": space_key,
            "title": title,
            "expand": "body.storage,version"
        }
        response = self._request("GET", "/content", params=params)
        
        if response.get("results"):
            return response["results"][0]
        return {}
    
    def create_page(self, space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """페이지 생성"""
        data: Dict[str, Any] = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        
        if parent_id:
            data["ancestors"] = [{"id": parent_id}]
        
        return self._request("POST", "/content", data)
    
    def update_page(self, page_id: str, title: str, content: str, version: int) -> Dict[str, Any]:
        """페이지 업데이트"""
        data: Dict[str, Any] = {
            "type": "page",
            "title": title,
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            },
            "version": {"number": version + 1}
        }
        return self._request("PUT", f"/content/{page_id}", data)
    
    def delete_page(self, page_id: str) -> None:
        """페이지 삭제"""
        self._request("DELETE", f"/content/{page_id}")
    
    # Space 관련 메서드
    def get_spaces(self, limit: int = 25) -> Dict[str, Any]:
        """모든 Space 조회"""
        params: Dict[str, int] = {"limit": limit}
        return self._request("GET", "/space", params=params)
    
    def get_space(self, space_key: str) -> Dict[str, Any]:
        """특정 Space 조회"""
        return self._request("GET", f"/space/{space_key}")
    
    # 검색 관련 메서드
    def search_content(self, cql: str, limit: int = 25) -> Dict[str, Any]:
        """CQL로 콘텐츠 검색"""
        params: Dict[str, Any] = {
            "cql": cql,
            "limit": limit
        }
        return self._request("GET", "/content/search", params=params)
    
    # 첨부파일 관련 메서드
    def get_attachments(self, page_id: str) -> Dict[str, Any]:
        """페이지 첨부파일 조회"""
        return self._request("GET", f"/content/{page_id}/child/attachment")
    
    def upload_attachment(self, page_id: str, file_path: str) -> Dict[str, Any]:
        """첨부파일 업로드"""
        # 파일 업로드는 multipart/form-data 필요
        url: str = f"{self.domain_url}{self.api_version}/content/{page_id}/child/attachment"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {"X-Atlassian-Token": "nocheck"}
            response = requests.post(url, auth=self.auth, files=files, headers=headers)
            response.raise_for_status()
            return response.json()


class BitbucketAPI:
    """Bitbucket REST API Client"""
    
    def __init__(self, domain_url: str, user_id: str, password: str):
        """
        Initialize Bitbucket API client
        
        Args:
            domain_url: Bitbucket domain URL (e.g., https://api.bitbucket.org for cloud or https://bitbucket.company.com for server)
            user_id: Username or email
            password: App password or API token
        """
        self.domain_url: str = domain_url.rstrip('/')
        self.user_id: str = user_id
        self.password: str = password
        self.auth = (user_id, password)
        self.headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Cloud vs Server API 버전 구분
        if "bitbucket.org" in domain_url:
            self.api_version: str = "/2.0"
            self.is_cloud: bool = True
        else:
            self.api_version: str = "/rest/api/1.0"
            self.is_cloud: bool = False
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make HTTP request to Bitbucket API"""
        url: str = f"{self.domain_url}{self.api_version}{endpoint}"
        
        kwargs: Dict[str, Any] = {
            "auth": self.auth,
            "headers": self.headers,
            "params": params
        }
        
        if data and method in ["POST", "PUT", "PATCH"]:
            kwargs["json"] = data
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.text:
                return response.json()
            return {}
        except requests.exceptions.RequestException as e:
            raise Exception(f"Bitbucket API 요청 실패: {str(e)}")
    
    # 저장소 관련 메서드
    def get_repositories(self, workspace: str) -> Dict[str, Any]:
        """작업공간의 모든 저장소 조회 (Cloud)"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}")
        else:
            return self._request("GET", "/projects")
    
    def get_repository(self, workspace: str, repo_slug: str) -> Dict[str, Any]:
        """특정 저장소 조회"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}")
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}")
    
    def create_repository(self, workspace: str, repo_slug: str, is_private: bool = True, description: str = "") -> Dict[str, Any]:
        """저장소 생성"""
        data: Dict[str, Any] = {
            "slug": repo_slug,
            "is_private": is_private,
            "description": description
        }
        
        if self.is_cloud:
            data["scm"] = "git"
            return self._request("POST", f"/repositories/{workspace}/{repo_slug}", data)
        else:
            data["name"] = repo_slug
            return self._request("POST", f"/projects/{workspace}/repos", data)
    
    def delete_repository(self, workspace: str, repo_slug: str) -> None:
        """저장소 삭제"""
        if self.is_cloud:
            self._request("DELETE", f"/repositories/{workspace}/{repo_slug}")
        else:
            self._request("DELETE", f"/projects/{workspace}/repos/{repo_slug}")
    
    # 브랜치 관련 메서드
    def get_branches(self, workspace: str, repo_slug: str) -> Dict[str, Any]:
        """저장소의 모든 브랜치 조회"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/refs/branches")
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/branches")
    
    def get_branch(self, workspace: str, repo_slug: str, branch_name: str) -> Dict[str, Any]:
        """특정 브랜치 조회"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}")
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/branches?filterText={branch_name}")
    
    def create_branch(self, workspace: str, repo_slug: str, branch_name: str, target_hash: str) -> Dict[str, Any]:
        """브랜치 생성"""
        data: Dict[str, Any] = {
            "name": branch_name,
            "target": {"hash": target_hash}
        }
        
        if self.is_cloud:
            return self._request("POST", f"/repositories/{workspace}/{repo_slug}/refs/branches", data)
        else:
            data = {
                "name": branch_name,
                "startPoint": target_hash
            }
            return self._request("POST", f"/projects/{workspace}/repos/{repo_slug}/branches", data)
    
    # Pull Request 관련 메서드
    def get_pull_requests(self, workspace: str, repo_slug: str, state: str = "OPEN") -> Dict[str, Any]:
        """Pull Request 목록 조회"""
        if self.is_cloud:
            params: Dict[str, str] = {"state": state}
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/pullrequests", params=params)
        else:
            params: Dict[str, str] = {"state": state}
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/pull-requests", params=params)
    
    def get_pull_request(self, workspace: str, repo_slug: str, pr_id: int) -> Dict[str, Any]:
        """특정 Pull Request 조회"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}")
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/pull-requests/{pr_id}")
    
    def create_pull_request(self, workspace: str, repo_slug: str, title: str, source_branch: str, 
                          destination_branch: str, description: str = "") -> Dict[str, Any]:
        """Pull Request 생성"""
        if self.is_cloud:
            data: Dict[str, Any] = {
                "title": title,
                "description": description,
                "source": {"branch": {"name": source_branch}},
                "destination": {"branch": {"name": destination_branch}}
            }
            return self._request("POST", f"/repositories/{workspace}/{repo_slug}/pullrequests", data)
        else:
            data: Dict[str, Any] = {
                "title": title,
                "description": description,
                "fromRef": {
                    "id": f"refs/heads/{source_branch}",
                    "repository": {
                        "slug": repo_slug,
                        "project": {"key": workspace}
                    }
                },
                "toRef": {
                    "id": f"refs/heads/{destination_branch}",
                    "repository": {
                        "slug": repo_slug,
                        "project": {"key": workspace}
                    }
                }
            }
            return self._request("POST", f"/projects/{workspace}/repos/{repo_slug}/pull-requests", data)
    
    def merge_pull_request(self, workspace: str, repo_slug: str, pr_id: int) -> Dict[str, Any]:
        """Pull Request 병합"""
        if self.is_cloud:
            return self._request("POST", f"/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/merge")
        else:
            return self._request("POST", f"/projects/{workspace}/repos/{repo_slug}/pull-requests/{pr_id}/merge")
    
    # 커밋 관련 메서드
    def get_commits(self, workspace: str, repo_slug: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """커밋 목록 조회"""
        params: Dict[str, str] = {}
        if branch:
            params["branch"] = branch
        
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/commits", params=params)
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/commits", params=params)
    
    def get_commit(self, workspace: str, repo_slug: str, commit_hash: str) -> Dict[str, Any]:
        """특정 커밋 조회"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/commit/{commit_hash}")
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/commits/{commit_hash}")
    
    # 웹훅 관련 메서드
    def get_webhooks(self, workspace: str, repo_slug: str) -> Dict[str, Any]:
        """웹훅 목록 조회"""
        if self.is_cloud:
            return self._request("GET", f"/repositories/{workspace}/{repo_slug}/hooks")
        else:
            return self._request("GET", f"/projects/{workspace}/repos/{repo_slug}/webhooks")
    
    def create_webhook(self, workspace: str, repo_slug: str, url: str, events: List[str]) -> Dict[str, Any]:
        """웹훅 생성"""
        data: Dict[str, Any] = {
            "url": url,
            "active": True,
            "events": events
        }
        
        if self.is_cloud:
            data["description"] = "Webhook"
            return self._request("POST", f"/repositories/{workspace}/{repo_slug}/hooks", data)
        else:
            data["name"] = "Webhook"
            return self._request("POST", f"/projects/{workspace}/repos/{repo_slug}/webhooks", data)


# 사용 예제를 위한 메인 함수
def main():
    """API 클라이언트 사용 예제"""
    
    # 사용자 입력 받기
    print("=== Atlassian API 클라이언트 ===")
    print("1. JIRA")
    print("2. Confluence")
    print("3. Bitbucket")
    
    choice = input("사용할 서비스를 선택하세요 (1-3): ").strip()
    
    domain_url = input("도메인 URL을 입력하세요: ").strip()
    user_id = input("사용자 ID (이메일 또는 username)를 입력하세요: ").strip()
    password = input("패스워드 (API 토큰 또는 앱 패스워드)를 입력하세요: ").strip()
    
    try:
        if choice == "1":
            # JIRA 예제
            jira = JiraAPI(domain_url, user_id, password)
            print("\n현재 사용자 정보:")
            user_info = jira.get_current_user()
            print(f"이름: {user_info.get('displayName')}")
            print(f"이메일: {user_info.get('emailAddress')}")
            
        elif choice == "2":
            # Confluence 예제
            confluence = ConfluenceAPI(domain_url, user_id, password)
            print("\nSpace 목록:")
            spaces = confluence.get_spaces()
            for space in spaces.get("results", [])[:5]:
                print(f"- {space.get('name')} ({space.get('key')})")
                
        elif choice == "3":
            # Bitbucket 예제
            bitbucket = BitbucketAPI(domain_url, user_id, password)
            workspace = input("Workspace 또는 Project Key를 입력하세요: ").strip()
            print(f"\n{workspace}의 저장소 목록:")
            repos = bitbucket.get_repositories(workspace)
            
            if bitbucket.is_cloud:
                for repo in repos.get("values", [])[:5]:
                    print(f"- {repo.get('name')} ({repo.get('slug')})")
            else:
                for repo in repos.get("values", [])[:5]:
                    print(f"- {repo.get('name')} ({repo.get('slug')})")
        else:
            print("잘못된 선택입니다.")
            
    except Exception as e:
        print(f"오류 발생: {str(e)}")


if __name__ == "__main__":
    main()