# TM Setter GUI 상호작용 로직 가이드

## 📌 개요
이 문서는 TM Setter GUI의 각 화면에서 구현해야 할 상호작용 로직을 정리한 가이드입니다.
각 섹션에는 TODO 주석 형태로 구현해야 할 기능이 표시되어 있습니다.

---

## 1. 🔐 로그인 화면 (login_view.py)

### 1.1 입력 필드 상호작용
```python
# TODO: [입력 필드 포커스 관리]
# - Tab 키로 필드 간 이동
# - 자동 포커스 이동 (ID 입력 후 Enter → 비밀번호 필드)
# - 비밀번호 표시/숨김 토글 버튼 추가

# TODO: [입력 유효성 실시간 검증]
# - ID 형식 검증 (이메일, 사번 등)
#   예: if not re.match(r'^[a-zA-Z0-9_]+$', user_id)
# - 비밀번호 강도 표시기
# - 입력 중 실시간 피드백 제공
```

### 1.2 로그인 버튼 클릭
```python
def on_login(self):
    # TODO: [로그인 전 검증]
    # 1. SQL Injection 방지
    #    - 특수문자 필터링/이스케이프
    # 2. XSS 공격 방지
    #    - HTML 태그 제거
    # 3. 로그인 시도 제한
    #    - 5회 실패 시 30분 계정 잠금
    #    - IP별 요청 제한 (Rate limiting)
    # 4. CAPTCHA 처리
    #    - 3회 실패 후 CAPTCHA 표시
```

### 1.3 인증 처리
```python
def authenticate(self, user_id: str, password: str):
    # TODO: [실제 인증 로직]
    # 1. REST API 호출
    #    response = requests.post('https://api.example.com/auth',
    #                            json={'username': user_id, 'password': hashed_password})
    
    # 2. LDAP/Active Directory 연동
    #    ldap_conn = ldap.initialize('ldap://ldap.example.com')
    #    ldap_conn.simple_bind_s(f'uid={user_id},ou=users,dc=example,dc=com', password)
    
    # 3. OAuth2/SAML 처리
    #    oauth_token = oauth_client.get_access_token(user_id, password)
    
    # 4. 다단계 인증 (MFA)
    #    otp_code = send_otp_to_phone(user_phone)
    #    if verify_otp(user_input_code, otp_code):
    #        return authenticated
```

### 1.4 로그인 성공 후
```python
def _handle_login_success(self, result: dict):
    # TODO: [로그인 후처리]
    # 1. 사용자 권한 확인
    #    user_role = result.get('role')
    #    enable_features_by_role(user_role)
    
    # 2. 로그인 이력 기록
    #    log_entry = {
    #        'user_id': user_id,
    #        'login_time': datetime.now(),
    #        'ip_address': get_client_ip(),
    #        'device_info': get_device_info()
    #    }
    #    save_login_history(log_entry)
    
    # 3. 세션 토큰 저장
    #    - 로컬 저장소에 암호화하여 저장
    #    - 토큰 만료 시간 관리
    
    # 4. 사용자 설정 불러오기
    #    settings = load_user_preferences(user_id)
    #    apply_theme(settings['theme'])
    #    set_language(settings['language'])
```

---

## 2. 📊 DB Code 선택 화면 (db_code_view.py)

### 2.1 ComboBox 상호작용
```python
def on_selection_change(self, event):
    # TODO: [선택 항목 연동]
    # 1. 계층적 선택 (1번 선택 → 2번 옵션 변경)
    #    if self.item1_var.get() == 'Database A':
    #        self.item2_combo['values'] = get_schemas_for_db('Database A')
    
    # 2. 실시간 데이터 로드
    #    - 선택 시 서버에서 최신 데이터 가져오기
    #    options = fetch_from_server('/api/db-codes', 
    #                               params={'parent': selected_value})
    
    # 3. 선택 내역 캐싱
    #    cache_selection(user_id, selected_items)
    
    # 4. 자동완성 기능
    #    - 타이핑 시 추천 항목 표시
```

### 2.2 데이터 로드
```python
def load_options(self):
    # TODO: [동적 데이터 로드]
    # 1. 데이터베이스 연결
    #    conn = create_db_connection()
    #    options = conn.execute("SELECT code, name FROM db_codes WHERE active=1")
    
    # 2. REST API 호출
    #    response = requests.get('/api/db-codes',
    #                           headers={'Authorization': f'Bearer {token}'})
    
    # 3. 권한별 필터링
    #    - 사용자 권한에 따라 보이는 옵션 제한
    #    filtered_options = filter_by_permission(options, user_role)
    
    # 4. 최근 사용 항목 우선 표시
    #    recent_items = get_recent_selections(user_id, limit=5)
    #    sorted_options = recent_items + other_options
```

### 2.3 다음 버튼
```python
def on_next(self):
    # TODO: [선택 검증 및 저장]
    # 1. 비즈니스 규칙 검증
    #    - 특정 조합 금지
    #    - 필수 항목 확인
    #    if not validate_combination(item1, item2, item3):
    #        show_error("이 조합은 허용되지 않습니다")
    
    # 2. 서버에 선택 내용 전송
    #    response = requests.post('/api/selections',
    #                            json={'selections': db_codes})
    
    # 3. 로컬 저장
    #    - 임시 파일에 저장 (작업 중단 시 복구용)
    #    save_to_temp_file(selections)
```

---

## 3. 🎫 Jira Issue 화면 (jira_issue_view.py)

### 3.1 검색 기능
```python
def on_search(self, event):
    # TODO: [실시간 검색]
    # 1. 디바운싱 적용 (타이핑 중단 후 300ms 대기)
    #    self.search_timer.cancel()
    #    self.search_timer = Timer(0.3, self.perform_search)
    
    # 2. Jira API 검색
    #    jql = f"project=PROJ AND summary~'{search_text}'"
    #    issues = jira_client.search_issues(jql, maxResults=50)
    
    # 3. 퍼지 매칭
    #    - 유사한 단어도 검색 결과에 포함
    #    from fuzzywuzzy import fuzz
    #    matches = [i for i in issues if fuzz.ratio(search, i.summary) > 70]
    
    # 4. 검색 히스토리
    #    save_search_history(user_id, search_text)
```

### 3.2 이슈 목록 표시
```python
def load_issues(self):
    # TODO: [Jira 이슈 로드]
    # 1. Jira REST API 호출
    #    jira = JIRA(server='https://jira.example.com',
    #               basic_auth=(username, api_token))
    #    issues = jira.search_issues('assignee=currentUser()')
    
    # 2. 페이지네이션
    #    - 스크롤 시 추가 로드 (무한 스크롤)
    #    if scroll_position > 80%:
    #        load_next_page()
    
    # 3. 이슈 필터링
    #    - 상태별 (Open, In Progress, Resolved)
    #    - 우선순위별 (Critical, High, Medium, Low)
    #    - 담당자별
    
    # 4. 이슈 정렬
    #    - 최신순, 우선순위순, 마감일순
```

### 3.3 이슈 선택
```python
def on_issue_click(self, issue_id):
    # TODO: [이슈 상세 정보]
    # 1. 이슈 상세 정보 표시
    #    issue = jira.issue(issue_id, expand='changelog')
    #    show_issue_details(issue)
    
    # 2. 관련 이슈 표시
    #    linked_issues = issue.fields.issuelinks
    #    show_related_issues(linked_issues)
    
    # 3. 첨부파일 다운로드
    #    for attachment in issue.fields.attachment:
    #        download_button.enable()
    
    # 4. 코멘트 표시
    #    comments = jira.comments(issue_id)
    #    display_comments(comments)
```

### 3.4 이슈 생성
```python
def create_new_issue(self):
    # TODO: [새 이슈 생성]
    # 1. 이슈 생성 다이얼로그
    #    dialog = IssueCreationDialog()
    #    if dialog.result:
    #        new_issue = jira.create_issue(
    #            project='PROJ',
    #            summary=dialog.summary,
    #            description=dialog.description,
    #            issuetype={'name': 'Task'}
    #        )
    
    # 2. 템플릿 적용
    #    template = load_issue_template(issue_type)
    #    apply_template(new_issue, template)
```

---

## 4. ⚙️ 옵션 화면 (options_view.py)

### 4.1 Repository Name 입력
```python
def on_repo_name_change(self, event):
    # TODO: [Repository 유효성 검증]
    # 1. Git 저장소 존재 확인
    #    if git_client.check_repo_exists(repo_name):
    #        show_status("✓ 저장소 확인됨")
    
    # 2. 접근 권한 확인
    #    if not git_client.has_access(repo_name, user_token):
    #        show_error("저장소 접근 권한이 없습니다")
    
    # 3. 자동완성
    #    suggestions = git_client.search_repos(partial_name)
    #    show_autocomplete(suggestions)
```

### 4.2 SW 버전 선택
```python
def load_sw_versions(self):
    # TODO: [버전 목록 로드]
    # 1. 빌드 서버에서 버전 목록 가져오기
    #    versions = jenkins_client.get_build_versions(project_name)
    
    # 2. 태그된 버전만 표시
    #    git_tags = git_client.get_tags(repo_name)
    #    versions = [t for t in git_tags if t.startswith('v')]
    
    # 3. 최신 버전 자동 선택
    #    latest = get_latest_stable_version(versions)
    #    self.version_combo.set(latest)
```

### 4.3 설정 저장
```python
def on_save_options(self):
    # TODO: [설정 저장 및 적용]
    # 1. 설정 파일 저장
    #    config = {
    #        'repository': repo_name,
    #        'version': sw_version,
    #        'timestamp': datetime.now()
    #    }
    #    save_to_json('config.json', config)
    
    # 2. 환경 변수 설정
    #    os.environ['TM_REPO'] = repo_name
    #    os.environ['TM_VERSION'] = sw_version
    
    # 3. 원격 저장소 동기화
    #    sync_settings_to_cloud(user_id, config)
```

### 4.4 완료 버튼
```python
def on_finish(self):
    # TODO: [최종 처리]
    # 1. 모든 선택 사항 검증
    #    final_data = {
    #        'login': self.app.session.get_user(),
    #        'db_codes': self.app.session.get('db_codes'),
    #        'jira_issue': self.app.session.get('selected_issue'),
    #        'options': get_current_options()
    #    }
    
    # 2. 작업 실행
    #    - TM 설정 작업 시작
    #    task_id = start_tm_setter_task(final_data)
    #    
    # 3. 진행 상황 표시
    #    progress_dialog = ProgressDialog()
    #    progress_dialog.track_task(task_id)
    
    # 4. 결과 리포트
    #    result = wait_for_completion(task_id)
    #    generate_report(result)
    #    send_email_notification(user_email, result)
```

---

## 5. 🎮 공통 상호작용 패턴

### 5.1 키보드 단축키
```python
# TODO: [전역 단축키]
# - Ctrl+S: 저장
# - Ctrl+Q: 종료
# - F1: 도움말
# - Esc: 취소/뒤로가기
# - Tab/Shift+Tab: 포커스 이동

self.root.bind('<Control-s>', lambda e: self.save_current_state())
self.root.bind('<Control-q>', lambda e: self.quit_application())
self.root.bind('<F1>', lambda e: self.show_help())
```

### 5.2 드래그 앤 드롭
```python
# TODO: [파일 드래그 앤 드롭]
def on_drop(self, event):
    files = event.data
    # 파일 형식 검증
    # 파일 업로드 처리
    # 진행 상황 표시
```

### 5.3 컨텍스트 메뉴
```python
# TODO: [우클릭 메뉴]
def create_context_menu(self):
    menu = tk.Menu(self, tearoff=0)
    menu.add_command(label="복사", command=self.copy)
    menu.add_command(label="붙여넣기", command=self.paste)
    menu.add_separator()
    menu.add_command(label="새로고침", command=self.refresh)
```

### 5.4 툴팁
```python
# TODO: [도움말 툴팁]
def create_tooltip(widget, text):
    # 마우스 호버 시 도움말 표시
    tooltip = Tooltip(widget, text)
    widget.bind('<Enter>', lambda e: tooltip.show())
    widget.bind('<Leave>', lambda e: tooltip.hide())
```

### 5.5 에러 처리
```python
# TODO: [전역 에러 처리]
def handle_error(self, error):
    # 1. 에러 로깅
    logger.error(f"Error occurred: {error}", exc_info=True)
    
    # 2. 사용자 친화적 메시지
    user_message = get_user_friendly_message(error)
    messagebox.showerror("오류", user_message)
    
    # 3. 복구 옵션 제공
    if can_recover(error):
        if messagebox.askyesno("복구", "다시 시도하시겠습니까?"):
            retry_operation()
    
    # 4. 에러 리포트 전송
    send_error_report(error, user_context)
```

---

## 6. 🔧 컨트롤러 구현 예시

### 6.1 AuthController
```python
class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        self.session_manager = SessionManager()
    
    def login(self, username: str, password: str) -> dict:
        # TODO: 실제 인증 서비스 호출
        # 1. 비밀번호 해싱
        # 2. API 호출
        # 3. 토큰 관리
        pass
    
    def logout(self):
        # TODO: 로그아웃 처리
        # 1. 토큰 무효화
        # 2. 세션 정리
        # 3. 캐시 삭제
        pass
```

### 6.2 JiraController
```python
class JiraController:
    def __init__(self, jira_url: str, auth_token: str):
        self.jira_client = JIRA(server=jira_url, token_auth=auth_token)
    
    def search_issues(self, query: str) -> list:
        # TODO: Jira 이슈 검색
        pass
    
    def create_issue(self, issue_data: dict) -> str:
        # TODO: 새 이슈 생성
        pass
```

---

## 📝 구현 우선순위

1. **필수 (Phase 1)**
   - 기본 인증 로직
   - 데이터 로드 및 저장
   - 화면 간 데이터 전달

2. **중요 (Phase 2)**
   - API 연동 (Jira, Git, DB)
   - 에러 처리
   - 로깅

3. **선택 (Phase 3)**
   - 키보드 단축키
   - 툴팁 및 도움말
   - 드래그 앤 드롭
   - 고급 검색 기능

---

## 🚀 다음 단계

1. 각 TODO 항목을 실제 코드로 구현
2. 단위 테스트 작성
3. 통합 테스트
4. 문서화
5. 배포

---

*이 문서는 개발 진행에 따라 지속적으로 업데이트됩니다.*