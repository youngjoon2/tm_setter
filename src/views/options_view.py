"""옵션 설정 화면 뷰"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import DarkTheme


class OptionsView:
    """옵션 설정 화면"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.theme = DarkTheme
        self.frame = tk.Frame(parent, **self.theme.get_frame_style('primary'))
        
        # 옵션 값들
        self.repo_name_var = tk.StringVar()
        self.sw_version_var = tk.StringVar()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너 (카드 스타일)
        container = tk.Frame(self.frame, 
                           bg=self.theme.BG_CARD,
                           width=600,
                           height=450,
                           highlightthickness=1,
                           highlightbackground=self.theme.BORDER_COLOR)
        container.place(relx=0.5, rely=0.45, anchor='center')
        container.pack_propagate(False)
        
        # 내부 패딩
        inner_container = tk.Frame(container, bg=self.theme.BG_CARD)
        inner_container.pack(padx=40, pady=40)
        
        # 타이틀
        title = tk.Label(inner_container, text="옵션 설정",
                        font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_2XL, 'bold'),
                        fg=self.theme.TEXT_PRIMARY, bg=self.theme.BG_CARD)
        title.pack(pady=(0, 10))
        
        # 부제목
        subtitle = tk.Label(inner_container, text="(선택사항)",
                          font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BASE),
                          fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        subtitle.pack(pady=(0, 30))
        
        # 옵션 프레임
        options_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        options_frame.pack(pady=10)
        
        # Repository Name
        repo_frame = tk.Frame(options_frame, bg=self.theme.BG_CARD)
        repo_frame.pack(pady=15, fill='x')
        
        repo_label = tk.Label(repo_frame, text="Repository Name",
                             font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                             fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        repo_label.pack(anchor='w', pady=(0, 8))
        
        repo_entry_frame = tk.Frame(repo_frame, bg=self.theme.BG_INPUT,
                                   highlightthickness=2,
                                   highlightbackground=self.theme.BORDER_COLOR,
                                   highlightcolor=self.theme.BORDER_FOCUS)
        repo_entry_frame.pack(fill='x')
        
        self.repo_entry = tk.Entry(repo_entry_frame,
                                  textvariable=self.repo_name_var,
                                  **self.theme.get_entry_style(),
                                  bd=0,
                                  width=35)
        self.repo_entry.pack(padx=10, pady=10)
        
        repo_hint = tk.Label(repo_frame, text="예: my-project-repo",
                           font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_XS),
                           fg=self.theme.TEXT_MUTED, bg=self.theme.BG_CARD)
        repo_hint.pack(anchor='w', pady=(4, 0))
        
        # SW Version
        version_frame = tk.Frame(options_frame, bg=self.theme.BG_CARD)
        version_frame.pack(pady=15, fill='x')
        
        version_label = tk.Label(version_frame, text="바이너리 SW 버전",
                               font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                               fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        version_label.pack(anchor='w', pady=(0, 8))
        
        # Combobox 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TCombobox',
                       fieldbackground=self.theme.BG_INPUT,
                       background=self.theme.BG_INPUT,
                       foreground=self.theme.TEXT_PRIMARY,
                       bordercolor=self.theme.BORDER_COLOR,
                       arrowcolor=self.theme.TEXT_SECONDARY)
        
        self.version_combo = ttk.Combobox(version_frame,
                                         textvariable=self.sw_version_var,
                                         style='Dark.TCombobox',
                                         font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BASE),
                                         width=33,
                                         state='readonly')
        self.version_combo.pack()
        
        # 버튼들
        button_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        button_frame.pack(pady=30)
        
        self.prev_button = tk.Button(button_frame,
                                    text="이전",
                                    **self.theme.get_button_style('secondary'),
                                    width=10,
                                    height=2,
                                    command=self.on_previous)
        self.prev_button.pack(side='left', padx=5)
        
        # 이전 버튼 호버 효과
        self.prev_button.bind('<Enter>', lambda e: self.prev_button.config(bg=self.theme.BG_HOVER))
        self.prev_button.bind('<Leave>', lambda e: self.prev_button.config(bg=self.theme.BG_SECONDARY))
        
        self.skip_button = tk.Button(button_frame,
                                    text="건너뛰기",
                                    font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BASE),
                                    bg=self.theme.BG_CARD,
                                    fg=self.theme.TEXT_SECONDARY,
                                    width=10,
                                    height=2,
                                    relief='solid',
                                    bd=2,
                                    cursor='hand2',
                                    command=self.on_skip)
        self.skip_button.pack(side='left', padx=5)
        
        # 건너뛰기 버튼 호버 효과
        self.skip_button.bind('<Enter>', lambda e: self.skip_button.config(bg=self.theme.BG_HOVER))
        self.skip_button.bind('<Leave>', lambda e: self.skip_button.config(bg=self.theme.BG_CARD))
        
        self.complete_button = tk.Button(button_frame,
                                        text="완료",
                                        **self.theme.get_button_style('primary'),
                                        width=10,
                                        height=2,
                                        command=self.on_complete)
        self.complete_button.pack(side='left', padx=5)
        
        # 완료 버튼 호버 효과
        self.complete_button.bind('<Enter>', lambda e: self.complete_button.config(bg=self.theme.ACCENT_HOVER))
        self.complete_button.bind('<Leave>', lambda e: self.complete_button.config(bg=self.theme.ACCENT_PRIMARY))
        
        # 진행 상태 표시
        status_label = tk.Label(button_frame, text="(4/4 단계)",
                               font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_XS),
                               fg=self.theme.TEXT_MUTED, bg=self.theme.BG_CARD)
        status_label.pack(side='left', padx=20)
        
    def load_options(self):
        """옵션 로드"""
        # SW 버전 목록 로드
        versions = self.app.config.get('sw_versions', [])
        self.version_combo['values'] = versions
        
        # 기본값 설정
        self.version_combo.set("선택하세요")
        self.repo_name_var.set("")
        
    def on_previous(self):
        """이전 버튼 클릭"""
        self.app.show_view('jira_issue')
        
    def on_skip(self):
        """건너뛰기 버튼 클릭"""
        if messagebox.askyesno("확인", "옵션 설정을 건너뛰시겠습니까?"):
            self.process_completion(skip=True)
            
    def on_complete(self):
        """완료 버튼 클릭"""
        # 옵션 값 저장
        options = {
            'repo_name': self.repo_name_var.get().strip(),
            'sw_version': self.sw_version_var.get()
        }
        
        if options['sw_version'] == "선택하세요":
            options['sw_version'] = ""
            
        self.app.session.set('options', options)
        self.process_completion(skip=False)
        
    def process_completion(self, skip: bool):
        """작업 완료 처리"""
        # 버튼 비활성화
        self.prev_button.config(state='disabled')
        self.skip_button.config(state='disabled')
        self.complete_button.config(state='disabled', text='처리 중...')
        
        # 비동기로 최종 처리
        self.app.async_handler.run_async(
            self.final_process,
            args=(skip,),
            callback=self.on_process_complete
        )
        
    def final_process(self, skip: bool):
        """최종 처리 (백그라운드)"""
        # 실제 작업 처리 시뮬레이션
        time.sleep(2)
        
        # 세션에서 모든 데이터 수집
        result = {
            'user_id': self.app.session.user_id,
            'db_codes': self.app.session.get('db_codes', {}),
            'selected_issue': self.app.session.get('selected_issue', {}),
            'options': self.app.session.get('options', {}) if not skip else {},
            'skipped_options': skip
        }
        
        return result
        
    def on_process_complete(self, result):
        """처리 완료"""
        self.frame.after(0, self._show_completion, result)
        
    def _show_completion(self, result):
        """완료 메시지 표시"""
        message = "작업이 완료되었습니다!\n\n"
        message += f"사용자: {result['user_id']}\n"
        message += f"DB Codes: {result['db_codes']}\n"
        message += f"선택된 Issue: {result['selected_issue'].get('key', '')}\n"
        
        if not result['skipped_options']:
            message += f"Repository: {result['options'].get('repo_name', '없음')}\n"
            message += f"SW 버전: {result['options'].get('sw_version', '없음')}"
        else:
            message += "옵션: 건너뜀"
            
        messagebox.showinfo("완료", message)
        
        # 초기화 및 로그인 화면으로
        self.reset_all()
        
    def reset_all(self):
        """전체 초기화"""
        # 세션 초기화
        self.app.session.logout()
        
        # 모든 화면 초기화
        for view in self.app.views.values():
            if hasattr(view, 'reset'):
                view.reset()
                
        # 버튼 복원
        self.prev_button.config(state='normal')
        self.skip_button.config(state='normal')
        self.complete_button.config(state='normal', text='완료')
        
        # 입력 필드 초기화
        self.repo_name_var.set("")
        self.version_combo.set("선택하세요")
        
        # 로그인 화면으로
        self.app.show_view('login')
        
    def reset(self):
        """화면 초기화"""
        self.repo_name_var.set("")
        self.version_combo.set("선택하세요")
        
    def show(self):
        """화면 표시"""
        self.frame.pack(fill='both', expand=True)
        # 옵션 로드
        self.load_options()
        # 첫 번째 입력 필드에 포커스
        self.repo_entry.focus()
        
    def hide(self):
        """화면 숨기기"""
        self.frame.pack_forget()