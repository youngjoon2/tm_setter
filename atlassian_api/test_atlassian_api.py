"""
Atlassian API 클라이언트 테스트
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
from atlassian_api import JiraAPI, ConfluenceAPI, BitbucketAPI


class TestJiraAPI(unittest.TestCase):
    """JIRA API 클라이언트 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        self.jira = JiraAPI(
            domain_url="https://test.atlassian.net",
            user_id="test@example.com",
            password="test-token"
        )
    
    def test_initialization(self):
        """초기화 테스트"""
        self.assertEqual(self.jira.domain_url, "https://test.atlassian.net")
        self.assertEqual(self.jira.user_id, "test@example.com")
        self.assertEqual(self.jira.password, "test-token")
        self.assertEqual(self.jira.auth, ("test@example.com", "test-token"))
        self.assertEqual(self.jira.api_version, "/rest/api/3")
    
    @patch('requests.request')
    def test_get_issue(self, mock_request):
        """이슈 조회 테스트"""
        mock_response = Mock()
        mock_response.text = '{"key": "TEST-123", "fields": {"summary": "Test Issue"}}'
        mock_response.json.return_value = {"key": "TEST-123", "fields": {"summary": "Test Issue"}}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.jira.get_issue("TEST-123")
        
        self.assertEqual(result["key"], "TEST-123")
        mock_request.assert_called_once_with(
            "GET",
            "https://test.atlassian.net/rest/api/3/issue/TEST-123",
            auth=("test@example.com", "test-token"),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            params=None
        )
    
    @patch('requests.request')
    def test_create_issue(self, mock_request):
        """이슈 생성 테스트"""
        mock_response = Mock()
        mock_response.text = '{"id": "10001", "key": "TEST-124"}'
        mock_response.json.return_value = {"id": "10001", "key": "TEST-124"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.jira.create_issue(
            project_key="TEST",
            issue_type="Task",
            summary="New Test Issue",
            description="Test description"
        )
        
        self.assertEqual(result["key"], "TEST-124")
        
        # 호출 인자 확인
        call_args = mock_request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertIn("/issue", call_args[0][1])
        self.assertIn("json", call_args[1])
        
        # 전송된 데이터 확인
        sent_data = call_args[1]["json"]
        self.assertEqual(sent_data["fields"]["project"]["key"], "TEST")
        self.assertEqual(sent_data["fields"]["summary"], "New Test Issue")
    
    @patch('requests.request')
    def test_search_issues(self, mock_request):
        """JQL 검색 테스트"""
        mock_response = Mock()
        mock_response.text = '{"issues": [{"key": "TEST-1"}, {"key": "TEST-2"}], "total": 2}'
        mock_response.json.return_value = {"issues": [{"key": "TEST-1"}, {"key": "TEST-2"}], "total": 2}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.jira.search_issues("project = TEST", max_results=10)
        
        self.assertEqual(result["total"], 2)
        self.assertEqual(len(result["issues"]), 2)
        
        # 파라미터 확인
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["params"]["jql"], "project = TEST")
        self.assertEqual(call_args[1]["params"]["maxResults"], 10)
    
    @patch('requests.request')
    def test_request_error_handling(self, mock_request):
        """에러 처리 테스트"""
        mock_request.side_effect = requests.exceptions.RequestException("Connection error")
        
        with self.assertRaises(Exception) as context:
            self.jira.get_issue("TEST-123")
        
        self.assertIn("JIRA API 요청 실패", str(context.exception))


class TestConfluenceAPI(unittest.TestCase):
    """Confluence API 클라이언트 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        self.confluence = ConfluenceAPI(
            domain_url="https://test.atlassian.net",
            user_id="test@example.com",
            password="test-token"
        )
    
    def test_initialization(self):
        """초기화 테스트"""
        # /wiki 자동 추가 테스트
        self.assertEqual(self.confluence.domain_url, "https://test.atlassian.net/wiki")
        self.assertEqual(self.confluence.user_id, "test@example.com")
        self.assertEqual(self.confluence.password, "test-token")
        
        # 이미 /wiki가 있는 경우
        confluence2 = ConfluenceAPI(
            domain_url="https://test.atlassian.net/wiki",
            user_id="test@example.com",
            password="test-token"
        )
        self.assertEqual(confluence2.domain_url, "https://test.atlassian.net/wiki")
    
    @patch('requests.request')
    def test_get_page_by_id(self, mock_request):
        """페이지 ID로 조회 테스트"""
        mock_response = Mock()
        mock_response.text = '{"id": "12345", "title": "Test Page", "version": {"number": 1}}'
        mock_response.json.return_value = {"id": "12345", "title": "Test Page", "version": {"number": 1}}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.confluence.get_page_by_id("12345")
        
        self.assertEqual(result["id"], "12345")
        self.assertEqual(result["title"], "Test Page")
        
        # expand 파라미터 확인
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["params"]["expand"], "body.storage,version")
    
    @patch('requests.request')
    def test_create_page(self, mock_request):
        """페이지 생성 테스트"""
        mock_response = Mock()
        mock_response.text = '{"id": "67890", "title": "New Page"}'
        mock_response.json.return_value = {"id": "67890", "title": "New Page"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.confluence.create_page(
            space_key="TEST",
            title="New Page",
            content="<p>Page content</p>",
            parent_id="12345"
        )
        
        self.assertEqual(result["id"], "67890")
        
        # 전송 데이터 확인
        call_args = mock_request.call_args
        sent_data = call_args[1]["json"]
        self.assertEqual(sent_data["type"], "page")
        self.assertEqual(sent_data["title"], "New Page")
        self.assertEqual(sent_data["space"]["key"], "TEST")
        self.assertEqual(sent_data["ancestors"][0]["id"], "12345")
    
    @patch('requests.request')
    def test_search_content(self, mock_request):
        """CQL 검색 테스트"""
        mock_response = Mock()
        mock_response.text = '{"results": [{"id": "1", "title": "Page 1"}], "size": 1}'
        mock_response.json.return_value = {"results": [{"id": "1", "title": "Page 1"}], "size": 1}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.confluence.search_content("space=TEST and type=page", limit=50)
        
        self.assertEqual(len(result["results"]), 1)
        
        # CQL 파라미터 확인
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["params"]["cql"], "space=TEST and type=page")
        self.assertEqual(call_args[1]["params"]["limit"], 50)
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b"file content")
    @patch('requests.post')
    def test_upload_attachment(self, mock_post, mock_open):
        """첨부파일 업로드 테스트"""
        mock_response = Mock()
        mock_response.text = '{"results": [{"id": "att123", "title": "test.pdf"}]}'
        mock_response.json.return_value = {"results": [{"id": "att123", "title": "test.pdf"}]}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = self.confluence.upload_attachment("12345", "/path/to/test.pdf")
        
        self.assertIn("results", result)
        
        # multipart 업로드 확인
        call_args = mock_post.call_args
        self.assertIn("files", call_args[1])
        self.assertEqual(call_args[1]["headers"]["X-Atlassian-Token"], "nocheck")


class TestBitbucketAPI(unittest.TestCase):
    """Bitbucket API 클라이언트 테스트"""
    
    def setUp(self):
        """테스트 초기화"""
        # Cloud 버전
        self.bitbucket_cloud = BitbucketAPI(
            domain_url="https://api.bitbucket.org",
            user_id="username",
            password="app-password"
        )
        
        # Server 버전
        self.bitbucket_server = BitbucketAPI(
            domain_url="https://bitbucket.company.com",
            user_id="username",
            password="password"
        )
    
    def test_initialization(self):
        """초기화 테스트"""
        # Cloud 버전
        self.assertEqual(self.bitbucket_cloud.domain_url, "https://api.bitbucket.org")
        self.assertEqual(self.bitbucket_cloud.api_version, "/2.0")
        self.assertTrue(self.bitbucket_cloud.is_cloud)
        
        # Server 버전
        self.assertEqual(self.bitbucket_server.domain_url, "https://bitbucket.company.com")
        self.assertEqual(self.bitbucket_server.api_version, "/rest/api/1.0")
        self.assertFalse(self.bitbucket_server.is_cloud)
    
    @patch('requests.request')
    def test_get_repositories_cloud(self, mock_request):
        """저장소 목록 조회 테스트 (Cloud)"""
        mock_response = Mock()
        mock_response.text = '{"values": [{"name": "repo1", "slug": "repo1"}]}'
        mock_response.json.return_value = {"values": [{"name": "repo1", "slug": "repo1"}]}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.bitbucket_cloud.get_repositories("workspace")
        
        self.assertIn("values", result)
        
        # URL 확인
        call_args = mock_request.call_args
        self.assertIn("/2.0/repositories/workspace", call_args[0][1])
    
    @patch('requests.request')
    def test_get_repositories_server(self, mock_request):
        """저장소 목록 조회 테스트 (Server)"""
        mock_response = Mock()
        mock_response.text = '{"values": [{"name": "repo1", "slug": "repo1"}]}'
        mock_response.json.return_value = {"values": [{"name": "repo1", "slug": "repo1"}]}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.bitbucket_server.get_repositories("PROJECT")
        
        self.assertIn("values", result)
        
        # URL 확인
        call_args = mock_request.call_args
        self.assertIn("/rest/api/1.0/projects", call_args[0][1])
    
    @patch('requests.request')
    def test_create_pull_request_cloud(self, mock_request):
        """Pull Request 생성 테스트 (Cloud)"""
        mock_response = Mock()
        mock_response.text = '{"id": 1, "title": "Test PR"}'
        mock_response.json.return_value = {"id": 1, "title": "Test PR"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.bitbucket_cloud.create_pull_request(
            workspace="workspace",
            repo_slug="repo1",
            title="Test PR",
            source_branch="feature",
            destination_branch="main",
            description="Test description"
        )
        
        self.assertEqual(result["id"], 1)
        
        # 데이터 확인
        call_args = mock_request.call_args
        sent_data = call_args[1]["json"]
        self.assertEqual(sent_data["title"], "Test PR")
        self.assertEqual(sent_data["source"]["branch"]["name"], "feature")
        self.assertEqual(sent_data["destination"]["branch"]["name"], "main")
    
    @patch('requests.request')
    def test_get_commits(self, mock_request):
        """커밋 목록 조회 테스트"""
        mock_response = Mock()
        mock_response.text = '{"values": [{"hash": "abc123", "message": "commit 1"}]}'
        mock_response.json.return_value = {"values": [{"hash": "abc123", "message": "commit 1"}]}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.bitbucket_cloud.get_commits("workspace", "repo1", branch="main")
        
        self.assertIn("values", result)
        
        # 브랜치 파라미터 확인
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]["params"]["branch"], "main")
    
    @patch('requests.request')
    def test_create_webhook(self, mock_request):
        """웹훅 생성 테스트"""
        mock_response = Mock()
        mock_response.text = '{"uuid": "webhook-123", "url": "https://example.com/hook"}'
        mock_response.json.return_value = {"uuid": "webhook-123", "url": "https://example.com/hook"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        
        result = self.bitbucket_cloud.create_webhook(
            workspace="workspace",
            repo_slug="repo1",
            url="https://example.com/hook",
            events=["repo:push", "pullrequest:created"]
        )
        
        self.assertEqual(result["url"], "https://example.com/hook")
        
        # 이벤트 확인
        call_args = mock_request.call_args
        sent_data = call_args[1]["json"]
        self.assertIn("repo:push", sent_data["events"])
        self.assertIn("pullrequest:created", sent_data["events"])


class TestIntegration(unittest.TestCase):
    """통합 테스트"""
    
    @patch('builtins.input')
    @patch('atlassian_api.JiraAPI')
    def test_main_jira_flow(self, mock_jira_class, mock_input):
        """메인 함수 JIRA 플로우 테스트"""
        # Mock 입력 설정
        mock_input.side_effect = [
            "1",  # JIRA 선택
            "https://test.atlassian.net",
            "test@example.com",
            "test-token"
        ]
        
        # Mock JIRA 인스턴스
        mock_jira_instance = Mock()
        mock_jira_instance.get_current_user.return_value = {
            "displayName": "Test User",
            "emailAddress": "test@example.com"
        }
        mock_jira_class.return_value = mock_jira_instance
        
        # 메인 함수 임포트 및 실행
        from atlassian_api import main
        
        # 출력 캡처를 위한 패치
        with patch('builtins.print') as mock_print:
            main()
        
        # JIRA 클래스 생성 확인
        mock_jira_class.assert_called_once_with(
            "https://test.atlassian.net",
            "test@example.com",
            "test-token"
        )
        
        # get_current_user 호출 확인
        mock_jira_instance.get_current_user.assert_called_once()


if __name__ == "__main__":
    unittest.main()