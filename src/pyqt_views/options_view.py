"""PyQt5 옵션 설정 화면 뷰"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QPushButton, QFrame, QTextEdit, QGroupBox, QSpinBox,
    QComboBox, QSlider, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pyqt_theme import PyQtDarkTheme


class OptionsView(QWidget):
    """PyQt5 옵션 설정 화면"""
    
    finish_clicked = pyqtSignal()
    back_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 타이틀 카드
        title_card = QFrame()
        title_card.setObjectName("titleCard")
        title_card.setFixedHeight(100)
        title_card.setStyleSheet(f"""
            QFrame#titleCard {{
                background-color: {PyQtDarkTheme.BG_CARD};
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        main_layout.addWidget(title_card)
        
        title_layout = QVBoxLayout(title_card)
        title_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("옵션 설정")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        
        desc = QLabel("추가 설정을 구성하고 최종 확인해주세요.")
        desc.setStyleSheet(f"color: {PyQtDarkTheme.TEXT_SECONDARY};")
        desc.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(desc)
        
        # 옵션 카드들을 담을 레이아웃
        options_layout = QHBoxLayout()
        main_layout.addLayout(options_layout)
        
        # 왼쪽 컬럼
        left_column = QVBoxLayout()
        options_layout.addLayout(left_column)
        
        # 일반 설정 그룹
        general_group = QGroupBox("일반 설정")
        general_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: {PyQtDarkTheme.BG_CARD};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: {PyQtDarkTheme.TEXT_PRIMARY};
            }}
        """)
        left_column.addWidget(general_group)
        
        general_layout = QVBoxLayout(general_group)
        general_layout.setContentsMargins(20, 20, 20, 20)
        
        self.auto_sync_checkbox = QCheckBox("자동 동기화 활성화")
        self.auto_sync_checkbox.setChecked(True)
        general_layout.addWidget(self.auto_sync_checkbox)
        
        self.notification_checkbox = QCheckBox("알림 표시")
        self.notification_checkbox.setChecked(True)
        general_layout.addWidget(self.notification_checkbox)
        
        self.auto_backup_checkbox = QCheckBox("자동 백업")
        general_layout.addWidget(self.auto_backup_checkbox)
        
        # 동기화 간격 설정
        sync_layout = QHBoxLayout()
        general_layout.addLayout(sync_layout)
        
        sync_label = QLabel("동기화 간격 (분):")
        sync_layout.addWidget(sync_label)
        
        self.sync_interval_spin = QSpinBox()
        self.sync_interval_spin.setMinimum(1)
        self.sync_interval_spin.setMaximum(60)
        self.sync_interval_spin.setValue(15)
        self.sync_interval_spin.setSuffix(" 분")
        sync_layout.addWidget(self.sync_interval_spin)
        
        sync_layout.addStretch()
        
        # 데이터 설정 그룹
        data_group = QGroupBox("데이터 설정")
        data_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: {PyQtDarkTheme.BG_CARD};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: {PyQtDarkTheme.TEXT_PRIMARY};
            }}
        """)
        left_column.addWidget(data_group)
        
        data_layout = QVBoxLayout(data_group)
        data_layout.setContentsMargins(20, 20, 20, 20)
        
        # 캐시 크기 설정
        cache_layout = QHBoxLayout()
        data_layout.addLayout(cache_layout)
        
        cache_label = QLabel("캐시 크기:")
        cache_layout.addWidget(cache_label)
        
        self.cache_slider = QSlider(Qt.Horizontal)
        self.cache_slider.setMinimum(10)
        self.cache_slider.setMaximum(500)
        self.cache_slider.setValue(100)
        self.cache_slider.setTickPosition(QSlider.TicksBelow)
        self.cache_slider.setTickInterval(50)
        cache_layout.addWidget(self.cache_slider)
        
        self.cache_value_label = QLabel("100 MB")
        cache_layout.addWidget(self.cache_value_label)
        
        self.cache_slider.valueChanged.connect(
            lambda v: self.cache_value_label.setText(f"{v} MB")
        )
        
        # 로그 레벨 설정
        log_layout = QHBoxLayout()
        data_layout.addLayout(log_layout)
        
        log_label = QLabel("로그 레벨:")
        log_layout.addWidget(log_label)
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText("INFO")
        log_layout.addWidget(self.log_level_combo)
        
        log_layout.addStretch()
        
        left_column.addStretch()
        
        # 오른쪽 컬럼
        right_column = QVBoxLayout()
        options_layout.addLayout(right_column)
        
        # 요약 정보 그룹
        summary_group = QGroupBox("설정 요약")
        summary_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: {PyQtDarkTheme.BG_CARD};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: {PyQtDarkTheme.TEXT_PRIMARY};
            }}
        """)
        right_column.addWidget(summary_group)
        
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(300)
        self.summary_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {PyQtDarkTheme.BG_INPUT};
                border: 1px solid {PyQtDarkTheme.BORDER_COLOR};
                border-radius: 4px;
                color: {PyQtDarkTheme.TEXT_PRIMARY};
                padding: 10px;
            }}
        """)
        summary_layout.addWidget(self.summary_text)
        
        # 설정 요약 업데이트
        self.update_summary()
        
        # 고급 설정 버튼
        advanced_button = QPushButton("고급 설정...")
        advanced_button.setObjectName("secondaryButton")
        advanced_button.clicked.connect(self.show_advanced_settings)
        summary_layout.addWidget(advanced_button)
        
        right_column.addStretch()
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        
        self.back_button = QPushButton("이전")
        self.back_button.setObjectName("secondaryButton")
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.on_back)
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch()
        
        self.save_button = QPushButton("설정 저장")
        self.save_button.setObjectName("secondaryButton")
        self.save_button.setFixedHeight(40)
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        self.finish_button = QPushButton("완료")
        self.finish_button.setFixedHeight(40)
        self.finish_button.clicked.connect(self.on_finish)
        button_layout.addWidget(self.finish_button)
        
        # 이벤트 연결
        self.auto_sync_checkbox.toggled.connect(self.update_summary)
        self.notification_checkbox.toggled.connect(self.update_summary)
        self.auto_backup_checkbox.toggled.connect(self.update_summary)
        self.sync_interval_spin.valueChanged.connect(self.update_summary)
        self.cache_slider.valueChanged.connect(self.update_summary)
        self.log_level_combo.currentTextChanged.connect(self.update_summary)
        
    def update_summary(self):
        """설정 요약 업데이트"""
        summary_lines = []
        
        # 로그인 정보
        if self.parent_window and hasattr(self.parent_window, 'session'):
            user_info = self.parent_window.session.get_user_info()
            if user_info:
                summary_lines.append(f"사용자: {user_info.get('user_name', '알 수 없음')}")
                
        # DB 선택 정보
        if self.parent_window and hasattr(self.parent_window, 'db_selections'):
            db_sel = self.parent_window.db_selections
            summary_lines.append(f"\n[DB 선택]")
            summary_lines.append(f"• 항목 1: {db_sel.get('item1', '미선택')}")
            summary_lines.append(f"• 항목 2: {db_sel.get('item2', '미선택')}")
            summary_lines.append(f"• 항목 3: {db_sel.get('item3', '미선택')}")
            
        # Jira 이슈 정보
        if self.parent_window and hasattr(self.parent_window, 'selected_issues'):
            issues = self.parent_window.selected_issues
            summary_lines.append(f"\n[Jira 이슈]")
            summary_lines.append(f"• 선택된 이슈: {len(issues)}개")
            if issues:
                summary_lines.append(f"• 이슈 번호: {', '.join(issues[:3])}{'...' if len(issues) > 3 else ''}")
                
        # 현재 설정
        summary_lines.append(f"\n[옵션 설정]")
        summary_lines.append(f"• 자동 동기화: {'활성화' if self.auto_sync_checkbox.isChecked() else '비활성화'}")
        summary_lines.append(f"• 동기화 간격: {self.sync_interval_spin.value()}분")
        summary_lines.append(f"• 알림: {'활성화' if self.notification_checkbox.isChecked() else '비활성화'}")
        summary_lines.append(f"• 자동 백업: {'활성화' if self.auto_backup_checkbox.isChecked() else '비활성화'}")
        summary_lines.append(f"• 캐시 크기: {self.cache_slider.value()} MB")
        summary_lines.append(f"• 로그 레벨: {self.log_level_combo.currentText()}")
        
        self.summary_text.setText("\n".join(summary_lines))
        
    def show_advanced_settings(self):
        """고급 설정 다이얼로그 표시"""
        QMessageBox.information(
            self,
            "고급 설정",
            "고급 설정 기능은 준비 중입니다."
        )
        
    def save_settings(self):
        """설정 저장"""
        # 설정 값 수집
        settings = {
            'auto_sync': self.auto_sync_checkbox.isChecked(),
            'sync_interval': self.sync_interval_spin.value(),
            'notification': self.notification_checkbox.isChecked(),
            'auto_backup': self.auto_backup_checkbox.isChecked(),
            'cache_size': self.cache_slider.value(),
            'log_level': self.log_level_combo.currentText()
        }
        
        # 설정 저장 (실제로는 config 파일에 저장)
        if self.parent_window:
            for key, value in settings.items():
                self.parent_window.config.set(f'options.{key}', value)
            
        QMessageBox.information(
            self,
            "설정 저장",
            "설정이 성공적으로 저장되었습니다."
        )
        
    def on_back(self):
        """이전 버튼 클릭"""
        self.back_clicked.emit()
        
    def on_finish(self):
        """완료 버튼 클릭"""
        # 설정 저장
        self.save_settings()
        
        # 완료 시그널 발생
        self.finish_clicked.emit()