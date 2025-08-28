"""DB Code 선택 화면 뷰"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.theme import DarkTheme


class DBCodeView:
    """DB Code 선택 화면"""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.theme = DarkTheme
        self.frame = tk.Frame(parent, **self.theme.get_frame_style('primary'))
        
        # 선택된 값들
        self.item1_var = tk.StringVar()
        self.item2_var = tk.StringVar()
        self.item3_var = tk.StringVar()
        
        self._create_widgets()
        
    def _create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너 (카드 스타일)
        container = tk.Frame(self.frame, 
                           bg=self.theme.BG_CARD,
                           highlightthickness=1,
                           highlightbackground=self.theme.BORDER_COLOR)
        container.place(relx=0.5, rely=0.45, anchor='center')
        
        # 내부 패딩
        inner_container = tk.Frame(container, bg=self.theme.BG_CARD)
        inner_container.pack(padx=40, pady=40)
        
        # 타이틀
        title = tk.Label(inner_container, text="DB Code 선택",
                        font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_2XL, 'bold'),
                        fg=self.theme.TEXT_PRIMARY, bg=self.theme.BG_CARD)
        title.pack(pady=(0, 15))
        
        # 설명
        desc = tk.Label(inner_container, 
                       text="아래 세 가지 항목을 선택해주세요.",
                       font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_MD),
                       fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        desc.pack(pady=(0, 30))
        
        # 선택 항목들
        selectors_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        selectors_frame.pack(pady=10)
        
        # 첫 번째 항목
        item1_frame = tk.Frame(selectors_frame, bg=self.theme.BG_CARD)
        item1_frame.pack(pady=(0, 20), fill='x')
        
        item1_label = tk.Label(item1_frame, text="첫 번째 항목",
                              font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                              fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        item1_label.pack(anchor='w', pady=(0, 8))
        
        # 콤보박스 프레임
        combo1_frame = tk.Frame(item1_frame, bg=self.theme.BG_INPUT,
                               highlightthickness=2,
                               highlightbackground=self.theme.BORDER_COLOR,
                               highlightcolor=self.theme.BORDER_FOCUS)
        combo1_frame.pack(fill='x')
        
        self.item1_combo = ttk.Combobox(combo1_frame,
                                       textvariable=self.item1_var,
                                       font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_MD),
                                       width=35,
                                       state='readonly')
        self.item1_combo.pack(padx=5, pady=5)
        self.item1_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # 두 번째 항목
        item2_frame = tk.Frame(selectors_frame, bg=self.theme.BG_CARD)
        item2_frame.pack(pady=(0, 20), fill='x')
        
        item2_label = tk.Label(item2_frame, text="두 번째 항목",
                              font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                              fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        item2_label.pack(anchor='w', pady=(0, 8))
        
        # 콤보박스 프레임
        combo2_frame = tk.Frame(item2_frame, bg=self.theme.BG_INPUT,
                               highlightthickness=2,
                               highlightbackground=self.theme.BORDER_COLOR,
                               highlightcolor=self.theme.BORDER_FOCUS)
        combo2_frame.pack(fill='x')
        
        self.item2_combo = ttk.Combobox(combo2_frame,
                                       textvariable=self.item2_var,
                                       font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_MD),
                                       width=35,
                                       state='readonly')
        self.item2_combo.pack(padx=5, pady=5)
        self.item2_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # 세 번째 항목
        item3_frame = tk.Frame(selectors_frame, bg=self.theme.BG_CARD)
        item3_frame.pack(fill='x')
        
        item3_label = tk.Label(item3_frame, text="세 번째 항목",
                              font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SM, 'bold'),
                              fg=self.theme.TEXT_SECONDARY, bg=self.theme.BG_CARD)
        item3_label.pack(anchor='w', pady=(0, 8))
        
        # 콤보박스 프레임
        combo3_frame = tk.Frame(item3_frame, bg=self.theme.BG_INPUT,
                               highlightthickness=2,
                               highlightbackground=self.theme.BORDER_COLOR,
                               highlightcolor=self.theme.BORDER_FOCUS)
        combo3_frame.pack(fill='x')
        
        self.item3_combo = ttk.Combobox(combo3_frame,
                                       textvariable=self.item3_var,
                                       font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_MD),
                                       width=35,
                                       state='readonly')
        self.item3_combo.pack(padx=5, pady=5)
        self.item3_combo.bind('<<ComboboxSelected>>', self.on_selection_change)
        
        # 버튼들
        button_frame = tk.Frame(inner_container, bg=self.theme.BG_CARD)
        button_frame.pack(pady=(30, 0))
        
        self.prev_button = tk.Button(button_frame,
                                    text="이전",
                                    **self.theme.get_button_style('secondary'),
                                    width=12,
                                    height=2,
                                    command=self.on_previous)
        self.prev_button.pack(side='left', padx=5)
        
        self.next_button = tk.Button(button_frame,
                                    text="다음",
                                    **self.theme.get_button_style('primary'),
                                    width=12,
                                    height=2,
                                    state='disabled',
                                    command=self.on_next)
        self.next_button.pack(side='left', padx=5)
        
        # 버튼 호버 효과
        self.prev_button.bind('<Enter>', lambda e: self.prev_button.config(bg=self.theme.BG_HOVER))
        self.prev_button.bind('<Leave>', lambda e: self.prev_button.config(bg=self.theme.BG_CARD))
        self.next_button.bind('<Enter>', lambda e: self.next_button.config(
            bg=self.theme.ACCENT_HOVER if self.next_button['state'] == 'normal' else self.theme.ACCENT_PRIMARY))
        self.next_button.bind('<Leave>', lambda e: self.next_button.config(bg=self.theme.ACCENT_PRIMARY))
        
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