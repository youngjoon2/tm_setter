"""TM Setter PyQt5 메인 애플리케이션"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QStackedWidget, QMessageBox, QStatusBar,
    QShortcut, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject, QTimer
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QPainter, QBrush, QKeySequence, QColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import Config, SessionManager
from utils.pyqt_theme import PyQtDarkTheme
from utils.animations import AnimationHelper
from widgets.loading_indicator import LoadingIndicator
from pyqt_views.login_view import LoginView
from pyqt_views.db_code_view import DBCodeView
from pyqt_views.jira_issue_view import JiraIssueView
from pyqt_views.options_view import OptionsView


class StepIndicator(QWidget):
    """스텝 인디케이터 위젯"""
    
    def __init__(self, number: str, text: str, parent=None):
        super().__init__(parent)
        self.number = number
        self.text = text
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        
        # 스텝 서클
        self.circle = QLabel(self.number)
        self.circle.setObjectName("stepCircle")
        self.circle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.circle)
        
        # 스텝 텍스트
        self.label = QLabel(self.text)
        self.label.setObjectName("stepText")
        layout.addWidget(self.label)
        
    def set_state(self, state: str):
        """스텝 상태 설정 (pending, active, completed)"""
        if state == "active":
            self.circle.setObjectName("stepCircleActive")
            self.label.setObjectName("stepTextActive")
        elif state == "completed":
            self.circle.setObjectName("stepCircleCompleted")
            self.label.setObjectName("stepTextCompleted")
        else:
            self.circle.setObjectName("stepCircle")
            self.label.setObjectName("stepText")
            
        # 스타일 재적용
        self.circle.setStyle(self.circle.style())
        self.label.setStyle(self.label.style())


class MinimalHeader(QFrame):
    """미니멀한 헤더 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(45)  # 최소 높이
        self.setMaximumHeight(50)  # 최대 높이
        self.setObjectName("header")
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # 타이틀 레이블 (왼쪽 정렬)
        title = QLabel("TM Setter")
        title.setStyleSheet(f"""
            QLabel {{
                color: #95a5a6;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 1px;
            }}
        """)
        layout.addWidget(title)
        
        # 오른쪽 공간 채우기
        layout.addStretch()
        
        # 배경색 설정
        self.setStyleSheet(f"""
            #header {{
                background-color: #1e1e1e;
                border-bottom: 1px solid #2d3436;
            }}
        """)


class TMSetterMainWindow(QMainWindow):
    """메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.session = SessionManager()
        self.jira_credentials = None
        self.animation_helper = AnimationHelper()
        self.first_load = True  # 초기 로드 플래그
        self.setup_ui()
        self.setup_views()
        self.setup_shortcuts()
        self.setup_status_bar()
        
    def setup_ui(self):
        """UI 설정"""
        self.setWindowTitle("TM Setter")
        self.setMinimumSize(800, 600)  # 최소 크기 설정
        self.resize(900, 700)  # 기본 크기
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setStretch(2, 1)  # 컨텐츠 영역이 늘어나도록 설정
        
        # 헤더
        self.header = MinimalHeader()
        main_layout.addWidget(self.header)
        
        # 스텝 인디케이터 프레임
        step_frame = QFrame()
        step_frame.setObjectName("stepFrame")
        step_frame.setMinimumHeight(70)
        step_frame.setMaximumHeight(80)
        main_layout.addWidget(step_frame)
        
        # 스텝 인디케이터 레이아웃
        step_layout = QHBoxLayout(step_frame)
        step_layout.setAlignment(Qt.AlignCenter)
        
        # 스텝 인디케이터들
        self.step_indicators = {}
        steps = [
            ('step1', '1', '로그인'),
            ('step2', '2', 'DB Code'),
            ('step3', '3', 'Jira Issue'),
            ('step4', '4', '옵션')
        ]
        
        for i, (step_id, num, text) in enumerate(steps):
            # 연결선 (첫 번째 스텝 제외)
            if i > 0:
                line = QFrame()
                line.setObjectName("line")
                line.setFixedWidth(40)
                line.setFixedHeight(2)
                line.setStyleSheet(f"background-color: {PyQtDarkTheme.BORDER_COLOR};")
                step_layout.addWidget(line)
            
            # 스텝 인디케이터
            indicator = StepIndicator(num, text)
            step_layout.addWidget(indicator)
            self.step_indicators[step_id] = indicator
        
        # 컨텐츠 영역 (스택 위젯)
        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.stack, 1)  # stretch factor 1
        
        # 로딩 인디케이터
        self.loading_indicator = LoadingIndicator(central_widget)
        self.loading_indicator.hide()
        
        # 테마 적용
        self.setStyleSheet(PyQtDarkTheme.get_stylesheet())
        
    def setup_views(self):
        """뷰 설정"""
        # 뷰 생성
        self.login_view = LoginView(self)
        self.db_code_view = DBCodeView(self)
        self.jira_issue_view = JiraIssueView(self)
        self.options_view = OptionsView(self)
        
        # 스택에 추가
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.db_code_view)
        self.stack.addWidget(self.jira_issue_view)
        self.stack.addWidget(self.options_view)
        
        # 시그널 연결
        self.login_view.login_success.connect(lambda: self.show_view('db_code'))
        self.db_code_view.next_clicked.connect(lambda: self.show_view('jira_issue'))
        self.db_code_view.back_clicked.connect(lambda: self.show_view('login'))
        self.jira_issue_view.next_clicked.connect(lambda: self.show_view('options'))
        self.jira_issue_view.back_clicked.connect(lambda: self.show_view('db_code'))
        self.options_view.finish_clicked.connect(self.on_finish)
        self.options_view.back_clicked.connect(lambda: self.show_view('jira_issue'))
        
        # 첫 화면 표시
        self.show_view('login')
        
    def show_view(self, view_name: str):
        """뷰 전환 (애니메이션 포함)"""
        print(f"[DEBUG] show_view called with: {view_name}")
        
        view_map = {
            'login': (self.login_view, 0),
            'db_code': (self.db_code_view, 1),
            'jira_issue': (self.jira_issue_view, 2),
            'options': (self.options_view, 3)
        }
        
        if view_name in view_map:
            view, index = view_map[view_name]
            print(f"[DEBUG] Switching to view: {view}, index: {index}")
            
            # 현재 위젯이 있을 때만 페이드 아웃 (초기 로드 시에는 없음)
            current_widget = self.stack.currentWidget()
            if current_widget and self.stack.currentIndex() >= 0 and not self.first_load:
                # 페이드 애니메이션 효과
                self.animation_helper.fade_out(current_widget)
                QTimer.singleShot(150, lambda: self.switch_view(index, view_name))
            else:
                # 초기 로드 시에는 애니메이션 없이 바로 전환
                self.switch_view(index, view_name)
    
    def switch_view(self, index: int, view_name: str):
        """실제 뷰 전환"""
        self.stack.setCurrentIndex(index)
        
        # 초기 로드가 아닐 때만 페이드 인 애니메이션 적용
        if not self.first_load:
            self.animation_helper.fade_in(self.stack.currentWidget())
        else:
            self.first_load = False
            
        self.update_step_indicators(view_name)
        self.update_status_bar(f"{view_name.replace('_', ' ').title()} 화면")
            
    def update_step_indicators(self, view_name: str):
        """스텝 인디케이터 업데이트"""
        # 모든 스텝 초기화
        for indicator in self.step_indicators.values():
            indicator.set_state("pending")
        
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
                    if i < len(steps) - 1:
                        self.step_indicators[step_id].set_state("completed")
                    else:
                        self.step_indicators[step_id].set_state("active")
                        
    def on_finish(self):
        """완료 처리"""
        reply = QMessageBox.question(
            self,
            "완료",
            "설정을 저장하고 종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config.save()
            self.close()
            
    def closeEvent(self, event):
        """창 닫기 이벤트"""
        reply = QMessageBox.question(
            self,
            "종료",
            "프로그램을 종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config.save()
            event.accept()
        else:
            event.ignore()
    
    def setup_shortcuts(self):
        """키보드 단축키 설정"""
        # Alt+1,2,3,4로 화면 전환
        QShortcut(QKeySequence("Alt+1"), self, lambda: self.show_view('login'))
        QShortcut(QKeySequence("Alt+2"), self, lambda: self.show_view('db_code'))
        QShortcut(QKeySequence("Alt+3"), self, lambda: self.show_view('jira_issue'))
        QShortcut(QKeySequence("Alt+4"), self, lambda: self.show_view('options'))
        
        # Ctrl+Q로 종료
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
        # F1로 도움말
        QShortcut(QKeySequence("F1"), self, self.show_help)
        
        # F5로 새로고침
        QShortcut(QKeySequence("F5"), self, self.refresh_current_view)
    
    def setup_status_bar(self):
        """상태바 설정"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("준비 완료")
        
        # 현재 사용자 표시
        self.user_label = QLabel("Guest")
        self.status_bar.addPermanentWidget(self.user_label)
        
        # 연결 상태 표시
        self.connection_label = QLabel("● 오프라인")
        self.connection_label.setStyleSheet("color: #e74c3c;")
        self.status_bar.addPermanentWidget(self.connection_label)
    
    def update_status_bar(self, message: str):
        """상태바 메시지 업데이트"""
        self.status_bar.showMessage(message, 5000)  # 5초간 표시
    
    def update_connection_status(self, connected: bool):
        """연결 상태 업데이트"""
        if connected:
            self.connection_label.setText("● 연결됨")
            self.connection_label.setStyleSheet("color: #27ae60;")
        else:
            self.connection_label.setText("● 오프라인")
            self.connection_label.setStyleSheet("color: #e74c3c;")
    
    def update_user_info(self, username: str):
        """사용자 정보 업데이트"""
        self.user_label.setText(f"User: {username}")
    
    def show_help(self):
        """도움말 표시"""
        help_text = """
        <h3>TM Setter 도움말</h3>
        <p><b>키보드 단축키:</b></p>
        <ul>
            <li>Alt+1~4: 화면 이동</li>
            <li>Ctrl+Q: 프로그램 종료</li>
            <li>F1: 도움말</li>
            <li>F5: 현재 화면 새로고침</li>
        </ul>
        <p><b>문의:</b> support@example.com</p>
        """
        QMessageBox.information(self, "도움말", help_text)
    
    def refresh_current_view(self):
        """현재 화면 새로고침"""
        current_widget = self.stack.currentWidget()
        if hasattr(current_widget, 'refresh'):
            current_widget.refresh()
            self.update_status_bar("화면을 새로고침했습니다.")
        else:
            self.update_status_bar("새로고침할 내용이 없습니다.")


class AsyncWorker(QThread):
    """비동기 작업 워커"""
    
    finished = pyqtSignal(object)
    error = pyqtSignal(Exception)
    
    def __init__(self, func, args=None, kwargs=None):
        super().__init__()
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}
        
    def run(self):
        """워커 실행"""
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Fusion 스타일 사용
    
    window = TMSetterMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()