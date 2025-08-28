"""PyQt5 로그인 화면 뷰"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pyqt_theme import PyQtDarkTheme
from controllers.auth_controller import AuthController


class AuthWorker(QThread):
    """인증 작업 워커 스레드"""
    
    success = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, user_id: str, password: str, jira_url: str = None):
        super().__init__()
        self.user_id = user_id
        self.password = password
        self.jira_url = jira_url
        
    def run(self):
        """인증 실행"""
        try:
            auth_controller = AuthController()
            result = auth_controller.authenticate(self.user_id, self.password, self.jira_url)
            
            if result['success']:
                self.success.emit(result)
            else:
                self.error.emit(result.get('error', 'ID 또는 비밀번호가 올바르지 않습니다.'))
        except Exception as e:
            self.error.emit(str(e))


class LoginView(QWidget):
    """PyQt5 로그인 화면"""
    
    login_success = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.auth_worker = None
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 카드 컨테이너
        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedSize(500, 550)
        card.setStyleSheet(f"""
            QFrame#loginCard {{
                background-color: {PyQtDarkTheme.BG_CARD};
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        main_layout.addWidget(card)
        
        # 카드 내부 레이아웃
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        
        # 아이콘과 타이틀
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setAlignment(Qt.AlignCenter)
        
        # 사용자 아이콘
        icon_frame = QFrame()
        icon_frame.setFixedSize(60, 60)
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {PyQtDarkTheme.ACCENT_PRIMARY};
                border-radius: 30px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_label = QLabel("☺")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 30px;
                background: transparent;
            }}
        """)
        icon_layout.addWidget(icon_label)
        title_layout.addWidget(icon_frame, alignment=Qt.AlignCenter)
        
        # 타이틀
        title = QLabel("로그인")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        subtitle = QLabel("TM Setter에 접속하세요")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        card_layout.addWidget(title_container)
        
        # Jira 인증 체크박스
        self.jira_checkbox = QCheckBox("Jira 인증 사용")
        self.jira_checkbox.toggled.connect(self.toggle_jira_url)
        card_layout.addWidget(self.jira_checkbox)
        
        # Jira URL 입력 (기본 숨김)
        self.url_container = QWidget()
        url_layout = QVBoxLayout(self.url_container)
        url_layout.setContentsMargins(0, 0, 0, 0)
        
        url_label = QLabel("Jira URL")
        url_label.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_SECONDARY}; font-weight: bold;")
        url_layout.addWidget(url_label)
        
        self.url_entry = QLineEdit()
        self.url_entry.setText("https://")
        self.url_entry.setPlaceholderText("예: https://your-domain.atlassian.net")
        url_layout.addWidget(self.url_entry)
        
        self.url_container.setVisible(False)
        card_layout.addWidget(self.url_container)
        
        # ID 입력
        id_container = QWidget()
        id_layout = QVBoxLayout(id_container)
        id_layout.setContentsMargins(0, 0, 0, 0)
        
        id_label = QLabel("사용자 ID")
        id_label.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_SECONDARY}; font-weight: bold;")
        id_layout.addWidget(id_label)
        
        self.id_entry = QLineEdit()
        self.id_entry.setPlaceholderText("ID를 입력하세요")
        id_layout.addWidget(self.id_entry)
        
        card_layout.addWidget(id_container)
        
        # 비밀번호 입력
        pw_container = QWidget()
        pw_layout = QVBoxLayout(pw_container)
        pw_layout.setContentsMargins(0, 0, 0, 0)
        
        pw_label = QLabel("비밀번호")
        pw_label.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_SECONDARY}; font-weight: bold;")
        pw_layout.addWidget(pw_label)
        
        self.pw_entry = QLineEdit()
        self.pw_entry.setEchoMode(QLineEdit.Password)
        self.pw_entry.setPlaceholderText("비밀번호를 입력하세요")
        pw_layout.addWidget(self.pw_entry)
        
        card_layout.addWidget(pw_container)
        
        # 에러 메시지
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)
        
        # 로그인 버튼
        self.login_button = QPushButton("로그인")
        self.login_button.setFixedHeight(45)
        self.login_button.clicked.connect(self.on_login)
        card_layout.addWidget(self.login_button)
        
        # 구분선
        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        card_layout.addWidget(line)
        
        # 힌트
        hint_container = QWidget()
        hint_layout = QHBoxLayout(hint_container)
        hint_layout.setAlignment(Qt.AlignCenter)
        
        hint_icon = QLabel("ℹ")
        hint_icon.setStyleSheet(f"color: {PyQtDarkTheme.INFO};")
        hint_layout.addWidget(hint_icon)
        
        hint_text = QLabel("로컬: ID='admin', PW='admin' | Jira: 실제 계정 사용")
        hint_text.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_MUTED}; font-size: {PyQtDarkTheme.FONT_SIZE_XS}px;")
        hint_layout.addWidget(hint_text)
        
        card_layout.addWidget(hint_container)
        
        # 스페이서
        card_layout.addStretch()
        
        # Enter 키 바인딩
        self.id_entry.returnPressed.connect(self.pw_entry.setFocus)
        self.pw_entry.returnPressed.connect(self.on_login)
        
    def toggle_jira_url(self, checked: bool):
        """Jira URL 입력 필드 표시/숨김"""
        self.url_container.setVisible(checked)
        if checked:
            self.url_entry.setFocus()
            
    def on_login(self):
        """로그인 처리"""
        user_id = self.id_entry.text().strip()
        password = self.pw_entry.text().strip()
        
        # 입력 검증
        if not user_id:
            self.show_error("사용자 ID를 입력해주세요.")
            self.id_entry.setFocus()
            return
            
        if not password:
            self.show_error("비밀번호를 입력해주세요.")
            self.pw_entry.setFocus()
            return
            
        # Jira URL 확인
        jira_url = None
        if self.jira_checkbox.isChecked():
            jira_url = self.url_entry.text().strip()
            if not jira_url or jira_url == "https://":
                self.show_error("Jira URL을 입력해주세요.")
                self.url_entry.setFocus()
                return
        
        # 로딩 상태
        self.login_button.setEnabled(False)
        self.login_button.setText("인증 중...")
        self.error_label.setText("")
        
        # 비동기 인증
        self.auth_worker = AuthWorker(user_id, password, jira_url)
        self.auth_worker.success.connect(self.on_login_success)
        self.auth_worker.error.connect(self.on_login_error)
        self.auth_worker.start()
        
    def on_login_success(self, result: dict):
        """로그인 성공 처리"""
        # 세션 저장
        user_info = result.get('user_info', {})
        if self.parent_window:
            self.parent_window.session.login(
                user_id=user_info.get('user_id', result.get('user_id')),
                user_name=user_info.get('user_name', result.get('user_name')),
                token=result.get('token')
            )
            
            # Jira 인증 정보 저장
            if 'jira_credentials' in result:
                self.parent_window.jira_credentials = result['jira_credentials']
        
        # UI 복원
        self.login_button.setEnabled(True)
        self.login_button.setText("로그인")
        
        # 입력 필드 초기화
        self.id_entry.clear()
        self.pw_entry.clear()
        self.url_entry.setText("https://")
        self.jira_checkbox.setChecked(False)
        self.error_label.setText("")
        
        # 다음 화면으로 이동
        self.login_success.emit()
        
    def on_login_error(self, error_msg: str):
        """로그인 실패 처리"""
        self.show_error(error_msg)
        self.login_button.setEnabled(True)
        self.login_button.setText("로그인")
        self.pw_entry.clear()
        self.pw_entry.setFocus()
        
    def show_error(self, message: str):
        """에러 메시지 표시"""
        self.error_label.setText(message)