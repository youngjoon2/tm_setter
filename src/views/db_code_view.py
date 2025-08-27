"""DB Code 선택 화면 뷰"""

import tkinter as tk
from tkinter import ttk, messagebox
import time


class DBCodeView:
    """DB Code 선택 화면"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg='white')
        
        # 선택된 값들
        self.item1_var = tk.StringVar()
        self.item2_var = tk.StringVar()
        self.item3_var = tk.StringVar()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너
        container = tk.Frame(self.frame, bg='white')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # 타이틀
        title = tk.Label(container, text="DB Code 선택",
                        font=('Arial', 24, 'bold'),
                        fg='#333333', bg='white')
        title.pack(pady=(0, 30))
        
        # 설명
        desc = tk.Label(container, 
                       text="아래 세 가지 항목을 선택해주세요.",
                       font=('Arial', 11),
                       fg='#6c757d', bg='white')
        desc.pack(pady=(0, 20))
        
        # 선택 항목들
        selectors_frame = tk.Frame(container, bg='white')
        selectors_frame.pack(pady=10)
        
        # 첫 번째 항목
        item1_frame = tk.Frame(selectors_frame, bg='white')
        item1_frame.pack(pady=10, fill='x')
        
        item1_label = tk.Label(item1_frame, text="첫 번째 항목",
                              font=('Arial', 11),
                              fg='#495057', bg='white')
        item1_label.pack(anchor='w')
        
        self.item1_combo = ttk.Combobox(item1_frame,
                                       textvariable=self.item1_var,
                                       font=('Arial', 11),
                                       width=35,
                                       state='readonly')
        self.item1_combo.pack(pady=5)
        self.item1_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # 두 번째 항목
        item2_frame = tk.Frame(selectors_frame, bg='white')
        item2_frame.pack(pady=10, fill='x')
        
        item2_label = tk.Label(item2_frame, text="두 번째 항목",
                              font=('Arial', 11),
                              fg='#495057', bg='white')
        item2_label.pack(anchor='w')
        
        self.item2_combo = ttk.Combobox(item2_frame,
                                       textvariable=self.item2_var,
                                       font=('Arial', 11),
                                       width=35,
                                       state='readonly')
        self.item2_combo.pack(pady=5)
        self.item2_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # 세 번째 항목
        item3_frame = tk.Frame(selectors_frame, bg='white')
        item3_frame.pack(pady=10, fill='x')
        
        item3_label = tk.Label(item3_frame, text="세 번째 항목",
                              font=('Arial', 11),
                              fg='#495057', bg='white')
        item3_label.pack(anchor='w')
        
        self.item3_combo = ttk.Combobox(item3_frame,
                                       textvariable=self.item3_var,
                                       font=('Arial', 11),
                                       width=35,
                                       state='readonly')
        self.item3_combo.pack(pady=5)
        self.item3_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # 버튼들
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=30)
        
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
        
    def load_options(self):
        """옵션 로드"""
        # 설정에서 옵션 가져오기
        item1_options = self.app.config.get('db_codes.item1_options', [])
        item2_options = self.app.config.get('db_codes.item2_options', [])
        item3_options = self.app.config.get('db_codes.item3_options', [])
        
        # 콤보박스에 설정
        self.item1_combo['values'] = item1_options
        self.item2_combo['values'] = item2_options
        self.item3_combo['values'] = item3_options
        
        # 기본값 설정 (선택 안함)
        self.item1_combo.set("선택하세요")
        self.item2_combo.set("선택하세요")
        self.item3_combo.set("선택하세요")
        
    def on_selection_change(self, event=None):
        """선택 변경 시 처리"""
        # 모든 항목이 선택되었는지 확인
        item1 = self.item1_var.get()
        item2 = self.item2_var.get()
        item3 = self.item3_var.get()
        
        if (item1 and item1 != "선택하세요" and
            item2 and item2 != "선택하세요" and
            item3 and item3 != "선택하세요"):
            self.next_button.config(state='normal')
        else:
            self.next_button.config(state='disabled')
            
    def on_previous(self):
        """이전 버튼 클릭"""
        # 로그아웃 확인
        if messagebox.askyesno("확인", "로그인 화면으로 돌아가시겠습니까?"):
            self.app.session.logout()
            self.app.show_view('login')
            # 선택 초기화
            self.item1_combo.set("선택하세요")
            self.item2_combo.set("선택하세요")
            self.item3_combo.set("선택하세요")
            
    def on_next(self):
        """다음 버튼 클릭"""
        # 선택된 값 저장
        db_codes = {
            'item1': self.item1_var.get(),
            'item2': self.item2_var.get(),
            'item3': self.item3_var.get()
        }
        
        # 세션에 저장
        self.app.session.set('db_codes', db_codes)
        
        # 다음 화면으로
        self.app.show_view('jira_issue')
        
    def show(self):
        """화면 표시"""
        self.frame.pack(fill='both', expand=True)
        # 옵션 로드
        self.load_options()
        # 첫 번째 콤보박스에 포커스
        self.item1_combo.focus()
        
    def hide(self):
        """화면 숨기기"""
        self.frame.pack_forget()