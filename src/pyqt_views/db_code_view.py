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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 카드 컨테이너
        card = QFrame()
        card.setObjectName("dbCodeCard")
        card.setFixedSize(500, 480)
        card.setStyleSheet("""
            QFrame#dbCodeCard {
                background-color: #3e4547;
                border: 2px solid #5a6c73;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(card)
        
        # 카드 내부 레이아웃
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        # 타이틀
        title = QLabel("DB Code 선택")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        card_layout.addWidget(title)
        
        # 설명
        desc = QLabel("아래 세 가지 항목을 선택해주세요.")
        desc.setStyleSheet("color: #95a5a6; font-size: 13px;")
        desc.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(desc)
        
        # 작은 스페이서
        card_layout.addSpacing(10)
        
        # 선택 항목들
        # 첫 번째 항목
        item1_container = QWidget()
        item1_layout = QVBoxLayout(item1_container)
        item1_layout.setContentsMargins(0, 0, 0, 0)
        
        item1_label = QLabel("첫 번째 항목")
        item1_label.setStyleSheet("color: #ecf0f1; font-weight: bold; font-size: 12px;")
        item1_layout.addWidget(item1_label)
        
        self.item1_combo = QComboBox()
        self.item1_combo.setFixedHeight(38)
        self.item1_combo.setStyleSheet("""
            QComboBox {
                background-color: #52575c;
                border: 1px solid #6c757d;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #95a5a6;
            }
            QComboBox QAbstractItemView {
                background-color: #52575c;
                border: 1px solid #6c757d;
                selection-background-color: #3498db;
                color: white;
            }
        """)
        self.item1_combo.currentIndexChanged.connect(self.on_item1_changed)
        item1_layout.addWidget(self.item1_combo)
        
        card_layout.addWidget(item1_container)
        
        # 두 번째 항목
        item2_container = QWidget()
        item2_layout = QVBoxLayout(item2_container)
        item2_layout.setContentsMargins(0, 0, 0, 0)
        
        item2_label = QLabel("두 번째 항목")
        item2_label.setStyleSheet("color: #ecf0f1; font-weight: bold; font-size: 12px;")
        item2_layout.addWidget(item2_label)
        
        self.item2_combo = QComboBox()
        self.item2_combo.setFixedHeight(38)
        self.item2_combo.setEnabled(False)
        self.item2_combo.setStyleSheet("""
            QComboBox {
                background-color: #52575c;
                border: 1px solid #6c757d;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QComboBox:hover:enabled {
                border: 2px solid #3498db;
            }
            QComboBox:disabled {
                background-color: #3a3f44;
                color: #7f8c8d;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #95a5a6;
            }
            QComboBox QAbstractItemView {
                background-color: #52575c;
                border: 1px solid #6c757d;
                selection-background-color: #3498db;
                color: white;
            }
        """)
        self.item2_combo.currentIndexChanged.connect(self.on_item2_changed)
        item2_layout.addWidget(self.item2_combo)
        
        card_layout.addWidget(item2_container)
        
        # 세 번째 항목
        item3_container = QWidget()
        item3_layout = QVBoxLayout(item3_container)
        item3_layout.setContentsMargins(0, 0, 0, 0)
        
        item3_label = QLabel("세 번째 항목")
        item3_label.setStyleSheet("color: #ecf0f1; font-weight: bold; font-size: 12px;")
        item3_layout.addWidget(item3_label)
        
        self.item3_combo = QComboBox()
        self.item3_combo.setFixedHeight(38)
        self.item3_combo.setEnabled(False)
        self.item3_combo.setStyleSheet("""
            QComboBox {
                background-color: #52575c;
                border: 1px solid #6c757d;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QComboBox:hover:enabled {
                border: 2px solid #3498db;
            }
            QComboBox:disabled {
                background-color: #3a3f44;
                color: #7f8c8d;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #95a5a6;
            }
            QComboBox QAbstractItemView {
                background-color: #52575c;
                border: 1px solid #6c757d;
                selection-background-color: #3498db;
                color: white;
            }
        """)
        self.item3_combo.currentIndexChanged.connect(self.validate_selection)
        item3_layout.addWidget(self.item3_combo)
        
        card_layout.addWidget(item3_container)
        
        # 스페이서
        card_layout.addStretch()
        
        # 상태 메시지
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #1890ff; font-size: 11px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        card_layout.addWidget(self.status_label)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.back_button = QPushButton("← 이전")
        self.back_button.setFixedHeight(38)
        self.back_button.setStyleSheet("""
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
        self.back_button.clicked.connect(self.on_back)
        button_layout.addWidget(self.back_button)
        
        self.next_button = QPushButton("다음 →")
        self.next_button.setFixedHeight(38)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 90px;
            }
            QPushButton:hover:enabled {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #34495e;
                color: #7f8c8d;
            }
        """)
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
            self.status_label.setStyleSheet("color: #52c41a; font-size: 12px;")
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