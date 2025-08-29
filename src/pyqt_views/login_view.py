"""PyQt5 로그인 화면 뷰"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QFrame, QMessageBox, QGraphicsDropShadowEffect,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator, QColor
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pyqt_theme import PyQtDarkTheme
from utils.animations import AnimationHelper
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
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 상단 스페이서
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 카드 컨테이너 (화면 크기에 맞게 조정)
        card = QFrame()
        card.setObjectName("loginCard")
        card.setMinimumSize(380, 420)  # 최소 크기
        card.setMaximumSize(500, 550)  # 최대 크기
        card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        card.setStyleSheet("""
            QFrame#loginCard {
                background-color: #3e4547;
                border: 2px solid #5a6c73;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(card)
        
        # 하단 스페이서
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 카드 내부 레이아웃
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 20)  # 여백 조정
        card_layout.setSpacing(12)  # 간격 조정
        
        # 타이틀 컨테이너
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(10)
        
        # 타이틀
        title = QLabel("로그인")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("TM Setter에 접속하세요")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #95a5a6; font-size: 12px;")
        title_layout.addWidget(subtitle)
        
        card_layout.addWidget(title_container)
        
        # Jira 인증 체크박스
        self.jira_checkbox = QCheckBox("Jira 인증 사용")
        self.jira_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ecf0f1;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #495057;
                border-radius: 3px;
                background-color: #34495e;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
        """)
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
        self.url_entry.setMinimumHeight(38)  # 최소 높이
        self.url_entry.setMaximumHeight(42)  # 최대 높이
        self.url_entry.setStyleSheet("""
            QLineEdit {
                background-color: #52575c;
                border: 1px solid #6c757d;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #5a6268;
            }
        """)
        url_layout.addWidget(self.url_entry)
        
        self.url_container.setVisible(False)
        card_layout.addWidget(self.url_container)
        
        # ID 입력
        id_container = QWidget()
        id_layout = QVBoxLayout(id_container)
        id_layout.setContentsMargins(0, 0, 0, 0)
        
        id_label = QLabel("사용자 ID")
        id_label.setStyleSheet("color: #ecf0f1; font-weight: bold; font-size: 12px;")
        id_layout.addWidget(id_label)
        
        self.id_entry = QLineEdit()
        self.id_entry.setPlaceholderText("ID를 입력하세요")
        self.id_entry.setMinimumHeight(38)  # 최소 높이
        self.id_entry.setMaximumHeight(42)  # 최대 높이
        self.id_entry.setStyleSheet("""
            QLineEdit {
                background-color: #52575c;
                border: 1px solid #6c757d;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #5a6268;
            }
        """)
        id_layout.addWidget(self.id_entry)
        
        card_layout.addWidget(id_container)
        
        # 비밀번호 입력
        pw_container = QWidget()
        pw_layout = QVBoxLayout(pw_container)
        pw_layout.setContentsMargins(0, 0, 0, 0)
        
        pw_label = QLabel("비밀번호")
        pw_label.setStyleSheet("color: #ecf0f1; font-weight: bold; font-size: 12px;")
        pw_layout.addWidget(pw_label)
        
        self.pw_entry = QLineEdit()
        self.pw_entry.setEchoMode(QLineEdit.Password)
        self.pw_entry.setPlaceholderText("비밀번호를 입력하세요")
        self.pw_entry.setMinimumHeight(38)  # 최소 높이
        self.pw_entry.setMaximumHeight(42)  # 최대 높이
        self.pw_entry.setStyleSheet("""
            QLineEdit {
                background-color: #52575c;
                border: 1px solid #6c757d;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #5a6268;
            }
        """)
        pw_layout.addWidget(self.pw_entry)
        
        card_layout.addWidget(pw_container)
        
        # 에러 메시지
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)
        
        # 버튼 컨테이너
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)  # 버튼 사이 간격
        
        # 로그인 버튼
        self.login_button = QPushButton("로그인")
        self.login_button.setMinimumHeight(38)
        self.login_button.setMaximumHeight(42)
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.login_button.clicked.connect(self.on_login)
        button_layout.addWidget(self.login_button)
        
        # 다음 버튼 (로그인 없이 진행)
        self.next_button = QPushButton("다음 →")
        self.next_button.setMinimumHeight(38)
        self.next_button.setMaximumHeight(42)
        self.next_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #495057;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #636e72;
            }
        """)
        self.next_button.clicked.connect(self.on_next)
        button_layout.addWidget(self.next_button)
        
        card_layout.addWidget(button_container)
        
        # 구분선
        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        card_layout.addWidget(line)
        
        # 힌트
        hint_container = QWidget()
        hint_layout = QVBoxLayout(hint_container)
        hint_layout.setAlignment(Qt.AlignCenter)
        hint_layout.setSpacing(2)
        
        # 아이콘과 첫 번째 줄
        hint_line1_container = QWidget()
        hint_line1_layout = QHBoxLayout(hint_line1_container)
        hint_line1_layout.setAlignment(Qt.AlignCenter)
        hint_line1_layout.setContentsMargins(0, 0, 0, 0)
        
        hint_icon = QLabel("ℹ")
        hint_icon.setStyleSheet(f"color: {PyQtDarkTheme.INFO};")
        hint_line1_layout.addWidget(hint_icon)
        
        hint_text1 = QLabel("로컬: ID='admin', PW='admin'")
        hint_text1.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_MUTED}; font-size: {PyQtDarkTheme.FONT_SIZE_XS}px;")
        hint_line1_layout.addWidget(hint_text1)
        
        # 두 번째 줄
        hint_text2 = QLabel("Jira: 실제 계정 사용")
        hint_text2.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_MUTED}; font-size: {PyQtDarkTheme.FONT_SIZE_XS}px;")
        hint_text2.setAlignment(Qt.AlignCenter)
        
        hint_layout.addWidget(hint_line1_container)
        hint_layout.addWidget(hint_text2)
        
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
        
    def on_next(self):
        """다음 버튼 클릭 (로그인 건너뛰기)"""
        # 게스트로 진행
        if self.parent_window:
            self.parent_window.session.login(
                user_id="guest",
                user_name="Guest User",
                token=None
            )
        # 다음 화면으로 이동
        self.login_success.emit()
        
    def show_error(self, message: str):
        """에러 메시지 표시"""
        self.error_label.setText(message)