"""TM Setter 메인 애플리케이션"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import Config, SessionManager
from utils.async_handler import AsyncHandler
from views.login_view import LoginView
from views.db_code_view import DBCodeView
from views.jira_issue_view import JiraIssueView
from views.options_view import OptionsView


class TMSetterApp:
    """메인 애플리케이션 클래스"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TM Setter")
        
        # 설정 및 세션 관리자
        self.config = Config()
        self.session = SessionManager()
        self.async_handler = AsyncHandler()
        
        # 윈도우 설정
        self._setup_window()
        
        # 스타일 설정
        self._setup_styles()
        
        # 현재 화면
        self.current_view = None
        self.views = {}
        
        # 상단 프레임 (헤더 + 스텝 인디케이터)
        self._create_header()
        
        # 메인 컨테이너
        self.main_container = tk.Frame(self.root, bg='white')
        self.main_container.pack(fill='both', expand=True)
        
        # 뷰 초기화
        self._init_views()
        
        # 첫 화면 표시
        self.show_view('login')
        
    def _setup_window(self):
        """윈도우 초기 설정"""
        # 크기 설정
        width = self.config.get('window.width', 600)
        height = self.config.get('window.height', 500)
        min_width = self.config.get('window.min_width', 500)
        min_height = self.config.get('window.min_height', 400)
        
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(min_width, min_height)
        
        # 화면 중앙 배치
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # 종료 이벤트
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def _setup_styles(self):
        """스타일 설정"""
        style = ttk.Style()
        
        # 색상 설정
        primary = self.config.get('theme.primary_color', '#667eea')
        secondary = self.config.get('theme.secondary_color', '#764ba2')
        
        # 버튼 스타일
        style.configure('Primary.TButton',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Secondary.TButton',
                       font=('Arial', 10))
        
    def _create_header(self):
        """헤더 및 스텝 인디케이터 생성"""
        # 헤더 프레임
        header_frame = tk.Frame(self.root, height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # 그라데이션 효과를 위한 캔버스
        self.header_canvas = tk.Canvas(header_frame, highlightthickness=0)
        self.header_canvas.pack(fill='both', expand=True)
        
        # 그라데이션 그리기
        self._draw_gradient(self.header_canvas, '#667eea', '#764ba2')
        
        # 타이틀
        title = tk.Label(self.header_canvas, text="TM Setter",
                        font=('Arial', 20, 'bold'),
                        fg='white', bg='#6d7dd6')
        self.header_canvas.create_window(300, 30, window=title)
        
        # 스텝 인디케이터 프레임
        step_frame = tk.Frame(self.root, bg='#f8f9fa', height=60)
        step_frame.pack(fill='x')
        step_frame.pack_propagate(False)
        
        # 스텝 인디케이터
        self.step_indicators = {}
        steps = [
            ('step1', '1', '로그인'),
            ('step2', '2', 'DB Code'),
            ('step3', '3', 'Jira Issue'),
            ('step4', '4', '옵션')
        ]
        
        step_container = tk.Frame(step_frame, bg='#f8f9fa')
        step_container.place(relx=0.5, rely=0.5, anchor='center')
        
        for i, (step_id, num, text) in enumerate(steps):
            # 스텝 컨테이너
            step_widget = tk.Frame(step_container, bg='#f8f9fa')
            step_widget.pack(side='left', padx=15)
            
            # 스텝 서클
            circle = tk.Label(step_widget, text=num, 
                            font=('Arial', 12, 'bold'),
                            fg='#6c757d', bg='#dee2e6',
                            width=3, height=1)
            circle.pack(side='left', padx=5)
            
            # 스텝 텍스트
            label = tk.Label(step_widget, text=text,
                           font=('Arial', 10),
                           fg='#6c757d', bg='#f8f9fa')
            label.pack(side='left')
            
            self.step_indicators[step_id] = {
                'circle': circle,
                'label': label
            }
            
    def _draw_gradient(self, canvas, color1, color2):
        """캔버스에 그라데이션 그리기"""
        canvas.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # 그라데이션 색상 계산
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        
        steps = height
        for i in range(steps):
            ratio = i / steps
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1)
            
    def _hex_to_rgb(self, hex_color):
        """HEX 색상을 RGB로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def _init_views(self):
        """뷰 초기화"""
        self.views = {
            'login': LoginView(self.main_container, self),
            'db_code': DBCodeView(self.main_container, self),
            'jira_issue': JiraIssueView(self.main_container, self),
            'options': OptionsView(self.main_container, self)
        }
        
    def show_view(self, view_name: str):
        """뷰 전환"""
        # 현재 뷰 숨기기
        if self.current_view:
            self.current_view.hide()
            
        # 새 뷰 표시
        if view_name in self.views:
            self.current_view = self.views[view_name]
            self.current_view.show()
            
            # 스텝 인디케이터 업데이트
            self._update_step_indicator(view_name)
            
    def _update_step_indicator(self, view_name: str):
        """스텝 인디케이터 업데이트"""
        # 모든 스텝 초기화
        for step in self.step_indicators.values():
            step['circle'].config(fg='#6c757d', bg='#dee2e6')
            step['label'].config(fg='#6c757d')
            
        # 현재 스텝과 완료된 스텝 표시
        step_map = {
            'login': ['step1'],
            'db_code': ['step1', 'step2'],
            'jira_issue': ['step1', 'step2', 'step3'],
            'options': ['step1', 'step2', 'step3', 'step4']
        }
        
        if view_name in step_map:
            steps = step_map[view_name]
            for i, step_id in enumerate(steps):
                if step_id in self.step_indicators:
                    indicator = self.step_indicators[step_id]
                    if i < len(steps) - 1:
                        # 완료된 스텝
                        indicator['circle'].config(fg='white', bg='#28a745')
                        indicator['label'].config(fg='#28a745')
                    else:
                        # 현재 스텝
                        indicator['circle'].config(fg='white', bg='#667eea')
                        indicator['label'].config(fg='#667eea')
                        
    def on_closing(self):
        """애플리케이션 종료"""
        if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
            # 비동기 핸들러 종료
            self.async_handler.stop()
            # 설정 저장
            self.config.save()
            # 프로그램 종료
            self.root.destroy()
            
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()


def main():
    """메인 함수"""
    app = TMSetterApp()
    app.run()


if __name__ == "__main__":
    main()