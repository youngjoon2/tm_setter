"""Jira Issue 선택 화면 뷰"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import DarkTheme


class JiraIssueView:
    """Jira Issue 선택 화면"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.theme = DarkTheme
        self.frame = tk.Frame(parent, **self.theme.get_frame_style('primary'))
        
        # 선택된 이슈
        self.selected_issue = None
        self.search_var = tk.StringVar()
        
        # 더미 데이터
        self.issues = []
        self.filtered_issues = []
        
        self._create_widgets()
        
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너 (카드 스타일)
        container = tk.Frame(self.frame, 
                           bg=self.theme.BG_CARD,
                           width=600,
                           height=500,
                           highlightthickness=1,
                           highlightbackground=self.theme.BORDER_COLOR)
        container.place(relx=0.5, rely=0.45, anchor='center')
        container.pack_propagate(False)
        
        # 내부 패딩
        inner_container = tk.Frame(container, bg=self.theme.BG_CARD)
        inner_container.pack(padx=40, pady=40, fill='both', expand=True)
        
        # 타이틀
        title = tk.Label(container, text="Jira Issue 선택",
                        font=('Arial', 24, 'bold'),
                        fg='#333333', bg='white')
        title.pack(pady=(0, 20))
        
        # 검색 박스
        search_frame = tk.Frame(container, bg='white')
        search_frame.pack(fill='x', pady=10)
        
        search_label = tk.Label(search_frame, text="🔍",
                               font=('Arial', 12),
                               fg='#6c757d', bg='white')
        search_label.pack(side='left', padx=5)
        
        self.search_entry = tk.Entry(search_frame,
                                    textvariable=self.search_var,
                                    font=('Arial', 11))
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Issue 리스트 프레임
        list_frame = tk.Frame(container, bg='white')
        list_frame.pack(fill='both', expand=True, pady=10)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox 대신 Frame과 Canvas 사용 (더 나은 스타일링)
        self.canvas = tk.Canvas(list_frame, bg='white', highlightthickness=1,
                              highlightbackground='#dee2e6')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)
        
        # Issue 아이템을 담을 프레임
        self.issues_frame = tk.Frame(self.canvas, bg='white')
        self.canvas_window = self.canvas.create_window(0, 0, anchor='nw', window=self.issues_frame)
        
        # Canvas 크기 조정
        self.issues_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # 버튼들
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=20)
        
        self.prev_button = tk.Button(button_frame,
                                    text="이전",
                                    font=('Arial', 11),
                                    bg='#6c757d',
                                    fg='white',
                                    width=12,
                                    height=2,
                                    cursor='hand2',
                                    command=self.on_previous)
        self.prev_button.pack(side='left', padx=5)
        
        self.next_button = tk.Button(button_frame,
                                    text="다음",
                                    font=('Arial', 11, 'bold'),
                                    bg='#667eea',
                                    fg='white',
                                    width=12,
                                    height=2,
                                    cursor='hand2',
                                    state='disabled',
                                    command=self.on_next)
        self.next_button.pack(side='left', padx=5)
        
    def load_issues(self):
        """이슈 로드 (비동기)"""
        # 로딩 표시
        loading_label = tk.Label(self.issues_frame, 
                               text="이슈를 불러오는 중...",
                               font=('Arial', 11),
                               fg='#6c757d', bg='white')
        loading_label.pack(pady=50)
        
        # 비동기로 이슈 로드
        self.app.async_handler.run_async(
            self.fetch_issues,
            callback=self.on_issues_loaded
        )
        
    def fetch_issues(self):
        """이슈 가져오기 (백그라운드)"""
        from controllers.jira_controller import JiraController
        
        # Jira 컨트롤러 초기화
        jira_credentials = getattr(self.app, 'jira_credentials', None)
        if jira_credentials:
            jira = JiraController(
                server_url=jira_credentials.get('url'),
                user_id=jira_credentials.get('user_id'),
                password=jira_credentials.get('password'),
                use_real_api=True
            )
        else:
            jira = JiraController()
        
        # DB Code에서 선택한 정보 또는 세션에서 가져오기
        db_codes = self.app.session.get('db_codes', {})
        project = db_codes.get('item1', '')
        
        # 이슈 검색
        issues = jira.search_issues(query="", project=project if project else None, max_results=50)
        
        # 기본 포맷 맞추기
        formatted_issues = []
        for issue in issues:
            formatted_issues.append({
                'key': issue.get('key', ''),
                'summary': issue.get('summary', ''),
                'status': issue.get('status', ''),
                'assignee': issue.get('assignee', ''),
                'priority': issue.get('priority', '')
            })
        
        if not formatted_issues:
            # 이슈가 없는 경우 기본 샘플 데이터
            formatted_issues = [
                {'key': 'SAMPLE-001', 'summary': '샘플 이슈 1', 'status': 'Open'},
                {'key': 'SAMPLE-002', 'summary': '샘플 이슈 2', 'status': 'In Progress'}
            ]
        
        return formatted_issues
        
    def on_issues_loaded(self, issues):
        """이슈 로드 완료"""
        self.frame.after(0, self._display_issues, issues)
        
    def _display_issues(self, issues):
        """이슈 표시"""
        # 기존 위젯 제거
        for widget in self.issues_frame.winfo_children():
            widget.destroy()
            
        self.issues = issues
        self.filtered_issues = issues.copy()
        
        # 이슈 아이템 생성
        for issue in self.filtered_issues:
            self.create_issue_item(issue)
            
    def create_issue_item(self, issue):
        """이슈 아이템 위젯 생성"""
        # 아이템 프레임
        item_frame = tk.Frame(self.issues_frame, bg='white', relief='flat')
        item_frame.pack(fill='x', padx=5, pady=2)
        
        # 호버 효과를 위한 배경
        def on_enter(e):
            if item_frame.cget('relief') != 'solid':
                item_frame.config(bg='#f8f9fa')
                for child in item_frame.winfo_children():
                    child.config(bg='#f8f9fa')
                    
        def on_leave(e):
            if item_frame.cget('relief') != 'solid':
                item_frame.config(bg='white')
                for child in item_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='white')
                        
        def on_click(e):
            self.select_issue(issue, item_frame)
            
        item_frame.bind('<Enter>', on_enter)
        item_frame.bind('<Leave>', on_leave)
        item_frame.bind('<Button-1>', on_click)
        
        # Issue Key
        key_label = tk.Label(item_frame, text=issue['key'],
                           font=('Arial', 11, 'bold'),
                           fg='#667eea', bg='white',
                           cursor='hand2')
        key_label.pack(anchor='w', padx=10, pady=(5, 0))
        key_label.bind('<Button-1>', on_click)
        
        # Issue Summary
        summary_label = tk.Label(item_frame, text=issue['summary'],
                               font=('Arial', 10),
                               fg='#495057', bg='white',
                               cursor='hand2')
        summary_label.pack(anchor='w', padx=10, pady=(0, 5))
        summary_label.bind('<Button-1>', on_click)
        
        # 구분선
        separator = tk.Frame(self.issues_frame, height=1, bg='#dee2e6')
        separator.pack(fill='x', padx=5)
        
        # 아이템에 참조 저장
        item_frame.issue = issue
        
    def select_issue(self, issue, item_frame):
        """이슈 선택"""
        # 이전 선택 제거
        for child in self.issues_frame.winfo_children():
            if isinstance(child, tk.Frame) and hasattr(child, 'issue'):
                child.config(relief='flat', bg='white')
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg='white')
                        
        # 새 선택 표시
        item_frame.config(relief='solid', bd=2, bg='#e7f1ff')
        for widget in item_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg='#e7f1ff')
                
        self.selected_issue = issue
        self.next_button.config(state='normal')
        
    def on_search(self, event=None):
        """검색 처리"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.filtered_issues = self.issues.copy()
        else:
            self.filtered_issues = [
                issue for issue in self.issues
                if search_term in issue['key'].lower() or
                   search_term in issue['summary'].lower()
            ]
            
        # 리스트 다시 그리기
        for widget in self.issues_frame.winfo_children():
            widget.destroy()
            
        if self.filtered_issues:
            for issue in self.filtered_issues:
                self.create_issue_item(issue)
        else:
            no_result = tk.Label(self.issues_frame,
                               text="검색 결과가 없습니다.",
                               font=('Arial', 11),
                               fg='#6c757d', bg='white')
            no_result.pack(pady=50)
            
    def on_frame_configure(self, event):
        """프레임 크기 변경 시 스크롤 영역 업데이트"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def on_canvas_configure(self, event):
        """캔버스 크기 변경 시 프레임 너비 조정"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
    def on_previous(self):
        """이전 버튼 클릭"""
        self.app.show_view('db_code')
        # 선택 초기화
        self.selected_issue = None
        self.search_var.set("")
        
    def on_next(self):
        """다음 버튼 클릭"""
        if self.selected_issue:
            # 선택된 이슈 저장
            self.app.session.set('selected_issue', self.selected_issue)
            # 다음 화면으로
            self.app.show_view('options')
            
    def show(self):
        """화면 표시"""
        self.frame.pack(fill='both', expand=True)
        # 이슈 로드
        self.load_issues()
        # 검색 필드에 포커스
        self.search_entry.focus()
        
    def hide(self):
        """화면 숨기기"""
        self.frame.pack_forget()