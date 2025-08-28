"""TM Setter PyQt5 메인 애플리케이션"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QPainter, QBrush

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import Config, SessionManager
from utils.pyqt_theme import PyQtDarkTheme
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


class GradientHeader(QFrame):
    """그라데이션 헤더 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        self.setObjectName("header")
        
    def paintEvent(self, event):
        """그라데이션 페인팅"""
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorStop(0, PyQtDarkTheme.ACCENT_PRIMARY)
        gradient.setColorStop(1, PyQtDarkTheme.ACCENT_ACTIVE)
        painter.fillRect(self.rect(), QBrush(gradient))
        
        # 타이틀 그리기
        painter.setPen(Qt.white)
        font = QFont(PyQtDarkTheme.FONT_FAMILY, PyQtDarkTheme.FONT_SIZE_2XL)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "TM Setter")


class TMSetterMainWindow(QMainWindow):
    """메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.session = SessionManager()
        self.jira_credentials = None
        self.setup_ui()
        self.setup_views()
        
    def setup_ui(self):
        """UI 설정"""
        self.setWindowTitle("TM Setter")
        self.setFixedSize(900, 700)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 헤더
        self.header = GradientHeader()
        main_layout.addWidget(self.header)
        
        # 스텝 인디케이터 프레임
        step_frame = QFrame()
        step_frame.setObjectName("stepFrame")
        step_frame.setFixedHeight(70)
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
        main_layout.addWidget(self.stack, 1)
        
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
        """뷰 전환"""
        view_map = {
            'login': (self.login_view, 0),
            'db_code': (self.db_code_view, 1),
            'jira_issue': (self.jira_issue_view, 2),
            'options': (self.options_view, 3)
        }
        
        if view_name in view_map:
            view, index = view_map[view_name]
            self.stack.setCurrentIndex(index)
            self.update_step_indicators(view_name)
            
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