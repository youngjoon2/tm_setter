"""개선된 로딩 인디케이터 위젯"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


class CircularProgress(QWidget):
    """원형 프로그레스 바"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.setFixedSize(50, 50)
        
        # 애니메이션 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        
    def start(self):
        """애니메이션 시작"""
        self.timer.start(20)  # 20ms마다 업데이트
        
    def stop(self):
        """애니메이션 중지"""
        self.timer.stop()
        
    def rotate(self):
        """회전 각도 업데이트"""
        self.angle = (self.angle + 5) % 360
        self.update()
        
    def paintEvent(self, event):
        """원형 프로그레스 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 배경 원
        pen = QPen(QColor(60, 60, 60), 3)
        painter.setPen(pen)
        painter.drawEllipse(5, 5, 40, 40)
        
        # 프로그레스 호
        pen = QPen(QColor(52, 152, 219), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(5, 5, 40, 40, -self.angle * 16, -90 * 16)


class LoadingIndicator(QWidget):
    """개선된 로딩 인디케이터"""
    
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        self.setObjectName("loadingIndicator")
        self.setFixedSize(200, 150)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # 원형 프로그레스
        self.progress = CircularProgress()
        layout.addWidget(self.progress, alignment=Qt.AlignCenter)
        
        # 텍스트 레이블
        self.text_label = QLabel("로딩 중...")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setObjectName("loadingText")
        layout.addWidget(self.text_label)
        
        # 상세 텍스트
        self.detail_label = QLabel("")
        self.detail_label.setAlignment(Qt.AlignCenter)
        self.detail_label.setObjectName("loadingDetail")
        self.detail_label.setWordWrap(True)
        layout.addWidget(self.detail_label)
        
        # 스타일 설정
        self.setStyleSheet("""
            #loadingIndicator {
                background-color: rgba(30, 30, 30, 0.95);
                border-radius: 10px;
                border: 1px solid #3498db;
            }
            #loadingText {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            #loadingDetail {
                color: #888;
                font-size: 12px;
            }
        """)
        
    def show_loading(self, text: str = "로딩 중...", detail: str = ""):
        """로딩 표시"""
        self.text_label.setText(text)
        self.detail_label.setText(detail)
        self.progress.start()
        self.show()
        
        # 중앙 위치로 이동
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = (parent_rect.height() - self.height()) // 2
            self.move(x, y)
        
    def hide_loading(self):
        """로딩 숨김"""
        self.progress.stop()
        self.hide()
        self.finished.emit()
        
    def set_text(self, text: str):
        """텍스트 변경"""
        self.text_label.setText(text)
        
    def set_detail(self, detail: str):
        """상세 텍스트 변경"""
        self.detail_label.setText(detail)


class ModernSpinner(QWidget):
    """모던한 스피너 위젯"""
    
    def __init__(self, parent=None, size: int = 40):
        super().__init__(parent)
        self.size = size
        self.angle = 0
        self.setFixedSize(size, size)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)
        
    def rotate(self):
        """회전"""
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        """스피너 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.size // 2, self.size // 2)
        painter.rotate(self.angle)
        
        # 여러 개의 원을 그려서 회전 효과
        for i in range(8):
            painter.rotate(45)
            opacity = (i + 1) / 8.0
            color = QColor(52, 152, 219, int(255 * opacity))
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(-2, -self.size // 2 + 5, 4, 4)