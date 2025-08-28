"""PyQt5 Jira Issue 선택 화면 뷰"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QFrame,
    QMessageBox, QHeaderView, QAbstractItemView, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pyqt_theme import PyQtDarkTheme
from controllers.jira_controller import JiraController


class JiraLoadWorker(QThread):
    """Jira 이슈 로드 워커"""
    
    success = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, jira_controller, project_key=None, issue_type=None):
        super().__init__()
        self.jira_controller = jira_controller
        self.project_key = project_key
        self.issue_type = issue_type
        
    def run(self):
        """이슈 로드 실행"""
        try:
            self.progress.emit("Jira 이슈를 불러오는 중...")
            issues = self.jira_controller.get_issues(
                project_key=self.project_key,
                issue_type=self.issue_type
            )
            self.success.emit(issues)
        except Exception as e:
            self.error.emit(str(e))


class JiraIssueView(QWidget):
    """PyQt5 Jira Issue 선택 화면"""
    
    next_clicked = pyqtSignal()
    back_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.jira_controller = None
        self.load_worker = None
        self.selected_issues = []
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 상단 카드 (검색 영역)
        search_card = QFrame()
        search_card.setObjectName("searchCard")
        search_card.setStyleSheet(f"""
            QFrame#searchCard {{
                background-color: {PyQtDarkTheme.BG_CARD};
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        main_layout.addWidget(search_card)
        
        search_layout = QVBoxLayout(search_card)
        search_layout.setContentsMargins(30, 30, 30, 30)
        
        # 타이틀
        title = QLabel("Jira Issue 선택")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        search_layout.addWidget(title)
        
        # 설명
        desc = QLabel("연동할 Jira 이슈를 검색하고 선택해주세요.")
        desc.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_SECONDARY};")
        desc.setAlignment(Qt.AlignCenter)
        search_layout.addWidget(desc)
        
        # 검색 영역
        search_input_layout = QHBoxLayout()
        search_layout.addLayout(search_input_layout)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("프로젝트 키 또는 이슈 번호 입력 (예: PROJ-123)")
        self.search_input.setFixedHeight(40)
        self.search_input.returnPressed.connect(self.on_search)
        search_input_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("검색")
        self.search_button.setFixedHeight(40)
        self.search_button.setFixedWidth(100)
        self.search_button.clicked.connect(self.on_search)
        search_input_layout.addWidget(self.search_button)
        
        self.load_all_button = QPushButton("전체 불러오기")
        self.load_all_button.setFixedHeight(40)
        self.load_all_button.setFixedWidth(120)
        self.load_all_button.clicked.connect(self.load_all_issues)
        search_input_layout.addWidget(self.load_all_button)
        
        # 테이블 카드
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_card.setStyleSheet(f"""
            QFrame#tableCard {{
                background-color: {PyQtDarkTheme.BG_CARD};
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        main_layout.addWidget(table_card, 1)
        
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(20, 20, 20, 20)
        
        # 테이블 헤더
        table_header_layout = QHBoxLayout()
        table_layout.addLayout(table_header_layout)
        
        self.result_label = QLabel("이슈 목록")
        self.result_label.setStyleSheet(f"""
            font-weight: bold;
            font-size: {PyQtDarkTheme.FONT_SIZE_MD}px;
            color: {PyQtDarkTheme.TEXT_PRIMARY};
        """)
        table_header_layout.addWidget(self.result_label)
        
        table_header_layout.addStretch()
        
        self.select_all_checkbox = QCheckBox("전체 선택")
        self.select_all_checkbox.toggled.connect(self.toggle_select_all)
        table_header_layout.addWidget(self.select_all_checkbox)
        
        # 테이블 위젯
        self.issues_table = QTableWidget()
        self.issues_table.setColumnCount(6)
        self.issues_table.setHorizontalHeaderLabels([
            "선택", "이슈 번호", "제목", "유형", "상태", "담당자"
        ])
        
        # 테이블 스타일 설정
        self.issues_table.setAlternatingRowColors(True)
        self.issues_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.issues_table.horizontalHeader().setStretchLastSection(False)
        self.issues_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.issues_table.setColumnWidth(0, 50)
        self.issues_table.setColumnWidth(1, 100)
        self.issues_table.setColumnWidth(3, 80)
        self.issues_table.setColumnWidth(4, 80)
        self.issues_table.setColumnWidth(5, 100)
        
        table_layout.addWidget(self.issues_table)
        
        # 상태 메시지
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"""
            color: {PyQtDarkTheme.INFO};
            font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(self.status_label)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        self.back_button = QPushButton("이전")
        self.back_button.setObjectName("secondaryButton")
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.on_back)
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch()
        
        self.selected_count_label = QLabel("0개 선택됨")
        self.selected_count_label.setStyleSheet(f"""
            color: {PyQtDarkTheme.TEXT_SECONDARY};
            font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;
        """)
        button_layout.addWidget(self.selected_count_label)
        
        button_layout.addStretch()
        
        self.next_button = QPushButton("다음")
        self.next_button.setFixedHeight(40)
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.on_next)
        button_layout.addWidget(self.next_button)
        
        # 초기 샘플 데이터 로드
        self.load_sample_data()
        
    def load_sample_data(self):
        """샘플 데이터 로드"""
        sample_issues = [
            {"key": "PROJ-001", "title": "로그인 기능 구현", "type": "Task", "status": "진행중", "assignee": "김철수"},
            {"key": "PROJ-002", "title": "데이터베이스 최적화", "type": "Story", "status": "대기", "assignee": "이영희"},
            {"key": "PROJ-003", "title": "UI 개선 작업", "type": "Task", "status": "완료", "assignee": "박민수"},
            {"key": "PROJ-004", "title": "보안 패치 적용", "type": "Bug", "status": "진행중", "assignee": "정수진"},
            {"key": "PROJ-005", "title": "성능 테스트", "type": "Task", "status": "대기", "assignee": "김철수"},
        ]
        
        self.populate_table(sample_issues)
        
    def populate_table(self, issues):
        """테이블에 이슈 데이터 채우기"""
        self.issues_table.setRowCount(len(issues))
        
        for row, issue in enumerate(issues):
            # 체크박스
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_selection)
            self.issues_table.setCellWidget(row, 0, checkbox)
            
            # 이슈 정보
            self.issues_table.setItem(row, 1, QTableWidgetItem(issue.get("key", "")))
            self.issues_table.setItem(row, 2, QTableWidgetItem(issue.get("title", "")))
            self.issues_table.setItem(row, 3, QTableWidgetItem(issue.get("type", "")))
            self.issues_table.setItem(row, 4, QTableWidgetItem(issue.get("status", "")))
            self.issues_table.setItem(row, 5, QTableWidgetItem(issue.get("assignee", "")))
            
        self.result_label.setText(f"이슈 목록 ({len(issues)}개)")
        
    def toggle_select_all(self, checked):
        """전체 선택/해제"""
        for row in range(self.issues_table.rowCount()):
            checkbox = self.issues_table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(checked)
                
    def update_selection(self):
        """선택 상태 업데이트"""
        selected_count = 0
        self.selected_issues = []
        
        for row in range(self.issues_table.rowCount()):
            checkbox = self.issues_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_count += 1
                issue_key = self.issues_table.item(row, 1).text()
                self.selected_issues.append(issue_key)
                
        self.selected_count_label.setText(f"{selected_count}개 선택됨")
        self.next_button.setEnabled(selected_count > 0)
        
    def on_search(self):
        """검색 실행"""
        search_text = self.search_input.text().strip()
        if not search_text:
            self.status_label.setText("검색어를 입력해주세요.")
            return
            
        self.status_label.setText(f"'{search_text}' 검색 중...")
        self.search_button.setEnabled(False)
        
        # 실제로는 Jira API 호출
        # 여기서는 샘플 데이터 필터링
        QThread.msleep(500)  # 시뮬레이션
        
        filtered_issues = [
            {"key": search_text, "title": f"{search_text} 관련 이슈", 
             "type": "Task", "status": "진행중", "assignee": "담당자"}
        ]
        
        self.populate_table(filtered_issues)
        self.status_label.setText(f"검색 완료: {len(filtered_issues)}개 이슈")
        self.search_button.setEnabled(True)
        
    def load_all_issues(self):
        """전체 이슈 로드"""
        self.status_label.setText("전체 이슈를 불러오는 중...")
        self.load_all_button.setEnabled(False)
        
        # 실제로는 Jira API 호출
        QThread.msleep(1000)  # 시뮬레이션
        
        self.load_sample_data()
        self.status_label.setText("이슈 로드 완료")
        self.load_all_button.setEnabled(True)
        
    def on_back(self):
        """이전 버튼 클릭"""
        self.back_clicked.emit()
        
    def on_next(self):
        """다음 버튼 클릭"""
        # 선택된 이슈 저장
        if self.parent_window:
            self.parent_window.selected_issues = self.selected_issues
            
        self.next_clicked.emit()