"""로그인 화면 뷰"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import DarkTheme


class LoginView:
    """로그인 화면"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.theme = DarkTheme
        self.frame = tk.Frame(parent, **self.theme.get_frame_style('primary'))
        
        # UI 요소들
        self.jira_url_var = tk.StringVar(value="https://")
        self.user_id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.use_jira_auth = tk.BooleanVar(value=False)
        
        self._create_widgets()
        
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너 (카드 스타일)
        container = tk.Frame(self.frame, 
                           bg=self.theme.BG_CARD,
                           width=500,
                           height=500,
                           highlightthickness=1,
                           highlightbackground=self.theme.BORDER_COLOR)
        container.place(relx=0.5, rely=0.5, anchor='center')
        container.pack_propagate(False)
        
        # 내부 패딩
        inner_container = tk.Frame(container, bg=self.theme.BG_CARD)
        inner_container.pack(padx=40, pady=40)
        
        # 로고 아이콘과 타이틀 컨테이너
        title_container = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        title_container.pack(pady=(0, 30))
        
        # 사용자 아이콘 (원 모양)
        icon_frame = tk.Frame(title_container, bg=self.theme.ACCENT_PRIMARY, width=60, height=60)
        icon_frame.pack(pady=(0, 15))
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(icon_frame, text="☺", 
                            font=(self.theme.FONT_FAMILY, 30),
                            fg=self.theme.TEXT_PRIMARY, 
                            bg=self.theme.ACCENT_PRIMARY)
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # 타이틀
        title = tk.Label(title_container, text="로그인",
                        font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_2XL, 'bold'),
                        fg=self.theme.TEXT_PRIMARY, bg=self.theme.BG_CARD)
        title.pack()
        
        subtitle = tk.Label(title_container, text="TM Setter에 접속하세요",
                          font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM),
                          fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        subtitle.pack(pady=(5, 0))
        
        # Jira 인증 체크박스
        jira_check_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        jira_check_frame.pack(pady=(15, 10), fill='x')
        
        self.jira_checkbox = tk.Checkbutton(jira_check_frame,
                                           text="Jira 인증 사용",
                                           variable=self.use_jira_auth,
                                           font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM),
                                           fg=self.theme.TEXT_SECONDARY,
                                           bg=self.theme.BG_CARD,
                                           selectcolor=self.theme.BG_INPUT,
                                           activebackground=self.theme.BG_CARD,
                                           command=self.toggle_jira_url)
        self.jira_checkbox.pack(anchor='w')
        
        # Jira URL 입력 (기본적으로 숨김)
        self.url_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        # url_frame은 처음에 표시하지 않음
        
        url_label = tk.Label(self.url_frame, text="Jira URL",
                           font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                           fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        url_label.pack(anchor='w', pady=(0, 8))
        
        url_entry_frame = tk.Frame(self.url_frame, bg=self.theme.BG_INPUT,
                                 highlightthickness=2,
                                 highlightbackground=self.theme.BORDER_COLOR,
                                 highlightcolor=self.theme.BORDER_FOCUS)
        url_entry_frame.pack(fill='x')
        
        self.url_entry = tk.Entry(url_entry_frame,
                                textvariable=self.jira_url_var,
                                **self.theme.get_entry_style(),
                                bd=0,
                                width=30)
        self.url_entry.pack(padx=10, pady=10)
        
        # ID 입력
        id_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        id_frame.pack(pady=(0, 20), fill='x')
        
        id_label = tk.Label(id_frame, text="사용자 ID",
                           font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                           fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        id_label.pack(anchor='w', pady=(0, 8))
        
        id_entry_frame = tk.Frame(id_frame, bg=self.theme.BG_INPUT, 
                                highlightthickness=2, 
                                highlightbackground=self.theme.BORDER_COLOR,
                                highlightcolor=self.theme.BORDER_FOCUS)
        id_entry_frame.pack(fill='x')
        
        self.id_entry = tk.Entry(id_entry_frame, 
                                textvariable=self.user_id_var,
                                **self.theme.get_entry_style(),
                                bd=0,
                                width=30)
        self.id_entry.pack(padx=10, pady=10)
        
        # Password 입력
        pw_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        pw_frame.pack(pady=(0, 15), fill='x')
        
        pw_label = tk.Label(pw_frame, text="비밀번호",
                           font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                           fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        pw_label.pack(anchor='w', pady=(0, 8))
        
        pw_entry_frame = tk.Frame(pw_frame, bg=self.theme.BG_INPUT,
                                highlightthickness=2,
                                highlightbackground=self.theme.BORDER_COLOR,
                                highlightcolor=self.theme.BORDER_FOCUS)
        pw_entry_frame.pack(fill='x')
        
        self.pw_entry = tk.Entry(pw_entry_frame,
                                textvariable=self.password_var,
                                **self.theme.get_entry_style(),
                                show='•',  # 점 문자로 비밀번호 표시
                                bd=0,
                                width=30)
        self.pw_entry.pack(padx=10, pady=10)
        
        # 에러 메시지
        self.error_label = tk.Label(inner_container,
                                  text="",
                                  font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM),
                                  fg=self.theme.ERROR, bg=self.theme.BG_CARD)
        self.error_label.pack(pady=(5, 10))
        
        # 로그인 버튼
        button_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        button_frame.pack(pady=(10, 0), fill='x')
        
        self.login_button = tk.Button(button_frame,
                                     text="로그인",
                                     **self.theme.get_button_style('primary'),
                                     width=25,
                                     height=2,
                                     command=self.on_login)
        self.login_button.pack(fill='x')
        
        # 버튼 호버 효과
        self.login_button.bind('<Enter>', lambda e: self.login_button.config(bg=self.theme.ACCENT_HOVER))
        self.login_button.bind('<Leave>', lambda e: self.login_button.config(bg=self.theme.ACCENT_PRIMARY))
        
        # Enter 키 바인딩
        self.id_entry.bind('<Return>', lambda e: self.pw_entry.focus())
        self.pw_entry.bind('<Return>', lambda e: self.on_login())
        
        # 구분선
        separator = tk.Frame(inner_container, bg=self.theme.BORDER_COLOR, height=1)
        separator.pack(fill='x', pady=(20, 15))
        
        # 테스트용 자동 입력 힌트
        hint_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        hint_frame.pack()
        
        hint_icon = tk.Label(hint_frame, text="ℹ",
                           font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM),
                           fg=self.theme.INFO, bg=self.theme.BG_CARD)
        hint_icon.pack(side='left', padx=(0, 5))
        
        hint = tk.Label(hint_frame,
                       text="로컬: ID='admin', PW='admin' | Jira: 실제 계정 사용",
                       font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_XS),
                       fg=self.theme.TEXT_MUTED, bg=self.theme.BG_CARD)
        hint.pack(side='left')
        
    def toggle_jira_url(self):
        """Jira URL 입력 필드 표시/숨김 토글"""
        if self.use_jira_auth.get():
            self.url_frame.pack(after=self.jira_checkbox.master, pady=(0, 20), fill='x')
            self.url_entry.focus()
        else:
            self.url_frame.pack_forget()
        
    def on_login(self):
        """로그인 버튼 클릭 처리"""
        user_id = self.user_id_var.get().strip()
        password = self.password_var.get().strip()
        
        # 입력 검증
        if not user_id:
            self.show_error("사용자 ID를 입력해주세요.")
            self.id_entry.focus()
            return
            
        if not password:
            self.show_error("비밀번호를 입력해주세요.")
            self.pw_entry.focus()
            return
            
        # 로딩 표시
        self.login_button.config(state='disabled', text='인증 중...', bg=self.theme.BG_HOVER)
        self.error_label.config(text="")
        
        # 비동기로 인증 처리
        self.app.async_handler.run_async(
            self.authenticate,
            args=(user_id, password),
            callback=self.on_login_success,
            error_callback=self.on_login_error
        )
        
    def authenticate(self, user_id: str, password: str) -> dict:
        """인증 처리 (백그라운드에서 실행)"""
        from controllers.auth_controller import AuthController
        auth_controller = AuthController()
        
        # Jira 인증 사용 여부 확인
        jira_url = None
        if self.use_jira_auth.get():
            jira_url = self.jira_url_var.get().strip()
            if not jira_url or jira_url == "https://":
                raise ValueError("Jira URL을 입력해주세요.")
        
        # 인증 수행
        result = auth_controller.authenticate(user_id, password, jira_url)
        
        if result['success']:
            # Jira 인증 정보 저장
            if 'jira_credentials' in result:
                self.app.jira_credentials = result['jira_credentials']
            return result
        else:
            raise ValueError(result.get('error', 'ID 또는 비밀번호가 올바르지 않습니다.'))
            
    def on_login_success(self, result: dict):
        """로그인 성공 처리"""
        # UI 스레드에서 실행되도록 예약
        self.frame.after(0, self._handle_login_success, result)
        
    def _handle_login_success(self, result: dict):
        """로그인 성공 UI 처리"""
        # 세션에 정보 저장
        user_info = result.get('user_info', {})
        self.app.session.login(
            user_id=user_info.get('user_id', result.get('user_id')),
            user_name=user_info.get('user_name', result.get('user_name')),
            token=result.get('token')
        )
        
        # 버튼 복원
        self.login_button.config(state='normal', text='로그인', bg=self.theme.ACCENT_PRIMARY)
        
        # 다음 화면으로 이동
        self.app.show_view('db_code')
        
        # 입력 필드 초기화
        self.user_id_var.set("")
        self.password_var.set("")
        self.jira_url_var.set("https://")
        self.use_jira_auth.set(False)
        self.toggle_jira_url()
        self.error_label.config(text="")
        
    def on_login_error(self, error: Exception):
        """로그인 실패 처리"""
        # UI 스레드에서 실행되도록 예약
        self.frame.after(0, self._handle_login_error, str(error))
        
    def _handle_login_error(self, error_msg: str):
        """로그인 실패 UI 처리"""
        self.show_error(error_msg)
        self.login_button.config(state='normal', text='로그인', bg=self.theme.ACCENT_PRIMARY)
        self.pw_entry.focus()
        self.password_var.set("")
        
    def show_error(self, message: str):
        """에러 메시지 표시"""
        self.error_label.config(text=message)
        
    def show(self):
        """화면 표시"""
        self.frame.pack(fill='both', expand=True)
        self.id_entry.focus()
        
    def hide(self):
        """화면 숨기기"""
        self.frame.pack_forget()