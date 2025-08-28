"""PyQt5 DB Code 선택 화면 뷰"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFrame, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pyqt_theme import PyQtDarkTheme
from controllers.db_controller import DBController


class DBLoadWorker(QThread):
    """DB 데이터 로드 워커"""
    
    success = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, load_func, *args, **kwargs):
        super().__init__()
        self.load_func = load_func
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        """데이터 로드 실행"""
        try:
            result = self.load_func(*self.args, **self.kwargs)
            self.success.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class DBCodeView(QWidget):
    """PyQt5 DB Code 선택 화면"""
    
    next_clicked = pyqtSignal()
    back_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.db_controller = DBController()
        self.load_worker = None
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
        """UI 설정"""
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 카드 컨테이너
        card = QFrame()
        card.setObjectName("dbCodeCard")
        card.setFixedSize(600, 500)
        card.setStyleSheet(f"""
            QFrame#dbCodeCard {{
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
        
        # 타이틀
        title = QLabel("DB Code 선택")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        # 설명
        desc = QLabel("아래 세 가지 항목을 선택해주세요.")
        desc.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_SECONDARY};")
        desc.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(desc)
        
        # 스페이서
        card_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 선택 항목들
        # 첫 번째 항목
        item1_container = QWidget()
        item1_layout = QVBoxLayout(item1_container)
        item1_layout.setContentsMargins(0, 0, 0, 0)
        
        item1_label = QLabel("첫 번째 항목")
        item1_label.setStyleSheet(f"""
            color: {PyQtDarkTheme.TEXT_SECONDARY}; 
            font-weight: bold;
            font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;
        """)
        item1_layout.addWidget(item1_label)
        
        self.item1_combo = QComboBox()
        self.item1_combo.setFixedHeight(40)
        self.item1_combo.currentIndexChanged.connect(self.on_item1_changed)
        item1_layout.addWidget(self.item1_combo)
        
        card_layout.addWidget(item1_container)
        
        # 두 번째 항목
        item2_container = QWidget()
        item2_layout = QVBoxLayout(item2_container)
        item2_layout.setContentsMargins(0, 0, 0, 0)
        
        item2_label = QLabel("두 번째 항목")
        item2_label.setStyleSheet(f"""
            color: {PyQtDarkTheme.TEXT_SECONDARY};
            font-weight: bold;
            font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;
        """)
        item2_layout.addWidget(item2_label)
        
        self.item2_combo = QComboBox()
        self.item2_combo.setFixedHeight(40)
        self.item2_combo.setEnabled(False)
        self.item2_combo.currentIndexChanged.connect(self.on_item2_changed)
        item2_layout.addWidget(self.item2_combo)
        
        card_layout.addWidget(item2_container)
        
        # 세 번째 항목
        item3_container = QWidget()
        item3_layout = QVBoxLayout(item3_container)
        item3_layout.setContentsMargins(0, 0, 0, 0)
        
        item3_label = QLabel("세 번째 항목")
        item3_label.setStyleSheet(f"""
            color: {PyQtDarkTheme.TEXT_SECONDARY};
            font-weight: bold;
            font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;
        """)
        item3_layout.addWidget(item3_label)
        
        self.item3_combo = QComboBox()
        self.item3_combo.setFixedHeight(40)
        self.item3_combo.setEnabled(False)
        self.item3_combo.currentIndexChanged.connect(self.validate_selection)
        item3_layout.addWidget(self.item3_combo)
        
        card_layout.addWidget(item3_container)
        
        # 스페이서
        card_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 상태 메시지
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {PyQtDarkTheme.INFO}; font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        card_layout.addWidget(self.status_label)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.back_button = QPushButton("이전")
        self.back_button.setObjectName("secondaryButton")
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.on_back)
        button_layout.addWidget(self.back_button)
        
        self.next_button = QPushButton("다음")
        self.next_button.setFixedHeight(40)
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.on_next)
        button_layout.addWidget(self.next_button)
        
        card_layout.addLayout(button_layout)
        
    def load_initial_data(self):
        """초기 데이터 로드"""
        # 임시 데이터 (실제로는 DB에서 로드)
        sample_data = [
            "옵션 A",
            "옵션 B",
            "옵션 C",
            "옵션 D",
            "옵션 E"
        ]
        
        self.item1_combo.addItem("선택하세요...")
        self.item1_combo.addItems(sample_data)
        
    def on_item1_changed(self, index):
        """첫 번째 항목 변경 시"""
        if index > 0:
            # 두 번째 항목 활성화 및 데이터 로드
            self.item2_combo.setEnabled(True)
            self.item2_combo.clear()
            self.item2_combo.addItem("선택하세요...")
            
            # 임시 데이터 (실제로는 첫 번째 선택에 따라 동적 로드)
            sample_data2 = [
                f"{self.item1_combo.currentText()} - 하위 1",
                f"{self.item1_combo.currentText()} - 하위 2",
                f"{self.item1_combo.currentText()} - 하위 3"
            ]
            self.item2_combo.addItems(sample_data2)
            
            # 세 번째 항목과 다음 버튼 비활성화
            self.item3_combo.setEnabled(False)
            self.item3_combo.clear()
            self.next_button.setEnabled(False)
        else:
            self.item2_combo.setEnabled(False)
            self.item2_combo.clear()
            self.item3_combo.setEnabled(False)
            self.item3_combo.clear()
            self.next_button.setEnabled(False)
            
    def on_item2_changed(self, index):
        """두 번째 항목 변경 시"""
        if index > 0:
            # 세 번째 항목 활성화 및 데이터 로드
            self.item3_combo.setEnabled(True)
            self.item3_combo.clear()
            self.item3_combo.addItem("선택하세요...")
            
            # 임시 데이터 (실제로는 두 번째 선택에 따라 동적 로드)
            sample_data3 = [
                f"{self.item2_combo.currentText()} - 상세 1",
                f"{self.item2_combo.currentText()} - 상세 2",
                f"{self.item2_combo.currentText()} - 상세 3"
            ]
            self.item3_combo.addItems(sample_data3)
            
            self.next_button.setEnabled(False)
        else:
            self.item3_combo.setEnabled(False)
            self.item3_combo.clear()
            self.next_button.setEnabled(False)
            
    def validate_selection(self):
        """선택 검증"""
        if (self.item1_combo.currentIndex() > 0 and
            self.item2_combo.currentIndex() > 0 and
            self.item3_combo.currentIndex() > 0):
            self.next_button.setEnabled(True)
            self.status_label.setText("✓ 모든 항목이 선택되었습니다.")
            self.status_label.setStyleSheet(f"color: {PyQtDarkTheme.SUCCESS}; font-size: {PyQtDarkTheme.FONT_SIZE_SM}px;")
        else:
            self.next_button.setEnabled(False)
            self.status_label.setText("")
            
    def on_back(self):
        """이전 버튼 클릭"""
        self.back_clicked.emit()
        
    def on_next(self):
        """다음 버튼 클릭"""
        # 선택된 값들 저장
        if self.parent_window:
            if not hasattr(self.parent_window, 'db_selections'):
                self.parent_window.db_selections = {}
                
            self.parent_window.db_selections = {
                'item1': self.item1_combo.currentText(),
                'item2': self.item2_combo.currentText(),
                'item3': self.item3_combo.currentText()
            }
            
        self.next_clicked.emit()