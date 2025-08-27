"""로그인 화면 뷰"""

import tkinter as tk
from tkinter import ttk, messagebox
import time


class LoginView:
    """로그인 화면"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg='white')
        
        # UI 요소들
        self.user_id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너
        container = tk.Frame(self.frame, bg='white')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # 타이틀
        title = tk.Label(container, text="로그인",
                        font=('Arial', 24, 'bold'),
                        fg='#333333', bg='white')
        title.pack(pady=(0, 30))
        
        # ID 입력
        id_frame = tk.Frame(container, bg='white')
        id_frame.pack(pady=10, fill='x')
        
        id_label = tk.Label(id_frame, text="사용자 ID",
                           font=('Arial', 11),
                           fg='#495057', bg='white')
        id_label.pack(anchor='w')
        
        self.id_entry = tk.Entry(id_frame, 
                                textvariable=self.user_id_var,
                                font=('Arial', 11),
                                width=30)
        self.id_entry.pack(pady=5)
        
        # Password 입력
        pw_frame = tk.Frame(container, bg='white')
        pw_frame.pack(pady=10, fill='x')
        
        pw_label = tk.Label(pw_frame, text="비밀번호",
                           font=('Arial', 11),
                           fg='#495057', bg='white')
        pw_label.pack(anchor='w')
        
        self.pw_entry = tk.Entry(pw_frame,
                                textvariable=self.password_var,
                                font=('Arial', 11),
                                show='*',
                                width=30)
        self.pw_entry.pack(pady=5)
        
        # 에러 메시지
        self.error_label = tk.Label(container,
                                  text="",
                                  font=('Arial', 10),
                                  fg='#dc3545', bg='white')
        self.error_label.pack(pady=5)
        
        # 로그인 버튼
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=20)
        
        self.login_button = tk.Button(button_frame,
                                     text="로그인",
                                     font=('Arial', 11, 'bold'),
                                     bg='#667eea',
                                     fg='white',
                                     width=25,
                                     height=2,
                                     cursor='hand2',
                                     command=self.on_login)
        self.login_button.pack()
        
        # Enter 키 바인딩
        self.id_entry.bind('<Return>', lambda e: self.pw_entry.focus())
        self.pw_entry.bind('<Return>', lambda e: self.on_login())
        
        # 테스트용 자동 입력 힌트
        hint = tk.Label(container,
                       text="테스트: ID='admin', PW='admin'",
                       font=('Arial', 9),
                       fg='#6c757d', bg='white')
        hint.pack(pady=10)
        
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
        self.login_button.config(state='disabled', text='인증 중...')
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
        # 실제 API 호출 시뮬레이션
        time.sleep(1.5)  # 네트워크 지연 시뮬레이션
        
        # 테스트용 하드코딩된 인증
        if user_id == 'admin' and password == 'admin':
            return {
                'success': True,
                'user_id': user_id,
                'user_name': 'Administrator',
                'token': 'test_token_123'
            }
        else:
            raise ValueError("ID 또는 비밀번호가 올바르지 않습니다.")
            
    def on_login_success(self, result: dict):
        """로그인 성공 처리"""
        # UI 스레드에서 실행되도록 예약
        self.frame.after(0, self._handle_login_success, result)
        
    def _handle_login_success(self, result: dict):
        """로그인 성공 UI 처리"""
        # 세션에 정보 저장
        self.app.session.login(
            user_id=result['user_id'],
            user_name=result.get('user_name'),
            token=result.get('token')
        )
        
        # 버튼 복원
        self.login_button.config(state='normal', text='로그인')
        
        # 다음 화면으로 이동
        self.app.show_view('db_code')
        
        # 입력 필드 초기화
        self.user_id_var.set("")
        self.password_var.set("")
        self.error_label.config(text="")
        
    def on_login_error(self, error: Exception):
        """로그인 실패 처리"""
        # UI 스레드에서 실행되도록 예약
        self.frame.after(0, self._handle_login_error, str(error))
        
    def _handle_login_error(self, error_msg: str):
        """로그인 실패 UI 처리"""
        self.show_error(error_msg)
        self.login_button.config(state='normal', text='로그인')
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